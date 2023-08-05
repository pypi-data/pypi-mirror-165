#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import yaml
import logging

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables

from lal import GPSTimeNow

from ligo.scald.io import influx, kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()

	parser.add_option('--far-threshold', default=2.314e-5, help = 'far threshold for missed vs found injections. Default is 2 per day.')
	parser.add_option("--scald-config", metavar = "file", help = "sets ligo-scald options based on yaml configuration.")
	opts, args = parser.parse_args()

	return opts, args


class InjMissedFound(object):
	def __init__(self, options):
		self.tag = options.tag
		self.kafka_server = options.kafka_server
		self.topics = options.input_topic
		self.datasource = options.data_source
		self.far_threshold = float(options.far_threshold)

		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{self.kafka_server}')

		# set up dicts to store trigger information
		self.routes = ['triggers', 'missed_triggers']
		self.triggers = {route: defaultdict(lambda: {'time': deque(maxlen = 1000), 'fields': defaultdict(lambda: deque(maxlen=1000))}) for route in self.routes}
		self.last_trigger_snapshot = None

		# set up influx configuration
		with open(options.scald_config, 'r') as f:
			config = yaml.safe_load(f)

		self.influx_sink = influx.Aggregator(**config["backends"]["default"])
		self.influx_sink.load(path=options.scald_config)

		# create a job service using cronut
		self.app = App('inj_missed_found', broker=f'kafka://{self.tag}_inj_missed_found@{self.kafka_server}')

		# subscribes to a topic
		@self.app.process(self.topics)
		def process(message): 
			mtopic = message.topic().split('.')[-1]
			mpipeline = message.topic().split('.')[0]
			mkey = utils.parse_msg_key(message)

			if mtopic == 'missed_inj':
				# these are injections that never got an event from the search
				# so they are automatically missed
				is_recovered = 'missed'

				injection = json.loads(message.value())
				sim_file = utils.load_xml(injection['sim'])
				on_ifos = self.sort_ifos(injection['onIFOs'])
				part_ifos = 'None'

				time, inj_snrs, dec_snr, source, trigger_dict = self.process_injection(sim_file, on_ifos)

				logging.info(f'{mpipeline}: {source} injection from time {time} {is_recovered.upper()}: no associated event message received.')

				# send data to kafka
				output = self.construct_output(injected_snrs = inj_snrs, time = time, decisive_snr = dec_snr)
				for topic in output:
					self.client.write(f'{mpipeline}.{self.tag}.testsuite.{topic}', output[topic], tags = [source, is_recovered])
					logging.info(f'Sent msg to: {mpipeline}.{self.tag}.testsuite.{topic} with tags: {source}, {is_recovered}')

				# store trigger data
				self.store_triggers(time, trigger_dict, route='missed_triggers', tags = (on_ifos, part_ifos))

			# otherwise, grab the coinc file, far, snr and time from the message
			# unpack data from the message, parse event info, and produce an output message
			elif mtopic == 'events':
				event = json.loads(message.value())

				coinc_file = utils.load_xml(event['coinc'])
				far = event['far']
				time = event['time'] + event['time_ns'] * 10**-9.
				on_ifos = self.sort_ifos(event['onIFOs'])

				# determine missed or found by getting the far of the recovered event
				is_recovered = 'found' if far < self.far_threshold else 'missed'

				snrs, inj_snrs, dec_snr, source, inj_time, trigger_dict, part_ifos = self.process_event(coinc_file, on_ifos)
				logging.info(f'{mpipeline}: {source} event from time {time} {is_recovered.upper()}: far = {far}.')

				# send messages to output topics
				output = self.construct_output(injected_snrs = inj_snrs, recovered_snrs = snrs, time = time, decisive_snr = dec_snr)
				for topic in output:
					self.client.write(f'{mpipeline}.{self.tag}.testsuite.{topic}', output[topic], tags = [source, is_recovered])
					logging.info(f'Sent msg to: {topic} with tags: {source}, {is_recovered}')

				# store trigger data
				self.store_triggers(time, trigger_dict, route='triggers', tags = (on_ifos, part_ifos))


	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


	def construct_output(self, injected_snrs = {}, recovered_snrs = {}, time = None, decisive_snr = None):
		output = defaultdict(lambda: {'time': [], 'data': []})

		for ifo, value in injected_snrs.items():
			if not value:
				continue
			output[f'{ifo}_injsnr'] = {
				'time': [ time ],
				'data': [ value ]
			}

		for ifo, value in recovered_snrs.items():
			if not value:
				continue
			output[f'{ifo}_recsnr'] = {
				'time': [ time ],
				'data': [ value ]
			}

		output['decisive_snr'] = {
				'time': [ time ],
				'data': [decisive_snr]
		}

		return output


	def process_injection(self, xmldoc, on_ifos):
		trigger_dict = defaultdict(lambda: None)
		inj_snrs = defaultdict(lambda: None)

		simtable = lsctables.SimInspiralTable.get_table(xmldoc)

		# get info from sim table
		time = simtable[0].geocent_end_time + 10.**-9 * simtable[0].geocent_end_time_ns
		inj_snrs['H1'] = simtable[0].alpha4
		inj_snrs['L1'] = simtable[0].alpha5
		inj_snrs['V1'] = simtable[0].alpha6

		# add injection parameters to trigger dict
		for attr in ("mass1", "mass2", "spin1z", "spin2z"):
			try:
				trigger_dict[f'sim_{attr}'] = float(simtable.getColumnByName(attr)[0])
			except TypeError:
				trigger_dict[f'sim_{attr}'] = None

		source = utils.source_tag(simtable)

		# add decisive snr to trigger dict
		dec_snr = utils.decisive_snr(inj_snrs, on_ifos)
		if dec_snr:
			trigger_dict['dec_snr'] = dec_snr
		else:
			trigger_dict['dec_snr'] = None

		return time, inj_snrs, dec_snr, source, trigger_dict


	def process_event(self, coinc_file, on_ifos):
		part_ifos = ''
		snrs = defaultdict(lambda: 0)

		# get inj SNR information
		inj_time, inj_snrs, dec_snr, source, trigger_dict = self.process_injection(coinc_file, on_ifos)

		# load tables
		coinctable = lsctables.CoincInspiralTable.get_table(coinc_file)
		sngltable = lsctables.SnglInspiralTable.get_table(coinc_file)
		coinceventtable = lsctables.CoincTable.get_table(coinc_file)

		# get info from coinc table
		coinc_time = coinctable[0].end_time + 10.**-9 * coinctable[0].end_time_ns
		trigger_dict["end"] = coinc_time
		for attr in ("combined_far", "snr", "false_alarm_rate"):
			try:
				trigger_dict[attr] = float(coinctable.getColumnByName(attr)[0])
			except TypeError:
				trigger_dict[attr] = None

		# get likelihood from coinc event table
		try:
			trigger_dict["likelihood"] = float(coinceventtable.getColumnByName("likelihood")[0])
		except TypeError:
			trigger_dict["likelihood"] = None

		# get info from sngl inspiral table
		for r in sngltable:
			snrs[r.ifo] = r.snr

			if r.snr:
				trigger_dict[f'{r.ifo}_snr'] = float(r.snr)
			else:
				trigger_dict[f'{r.ifo}_snr'] = None

			# keep track of participating IFOs
			if r.snr >= 4.:
				part_ifos += r.ifo

			for attr in ("chisq", "mass1", "mass2", "spin1z", "spin2z", "coa_phase"):
				if getattr(r, attr):
					if not trigger_dict[f'sngl_{attr}']:
						trigger_dict[f'sngl_{attr}'] = float(getattr(r, attr))
				else:
					trigger_dict[f'sngl_{attr}'] = None

		part_ifos = self.sort_ifos(part_ifos)

		return snrs, inj_snrs, dec_snr, source, inj_time, trigger_dict, part_ifos

	def store_triggers(self, time, data, route=None, tags=None):
		self.triggers[route][tags]['time'].append(time)
		for key, value in data.items():
			self.triggers[route][tags]['fields'][key].append(value)

		# output data to influx every 100 seconds
		if not self.last_trigger_snapshot or (float(GPSTimeNow()) - self.last_trigger_snapshot >= 100.):
			self.last_reduce_time = float(GPSTimeNow())

			# cast data from deques to lists to output
			outdata = {}
			for key in self.triggers:
				outdata[key] = {}
				for tag in self.triggers[key]:
					outdata[key][tag] = {
						'time': list(self.triggers[key][tag]['time']),
						'fields': {
							dataname: list(datadeq) for dataname, datadeq in self.triggers[key][tag]['fields'].items()
						}
					}

			## First store triggers, these get aggregated by combined_far
			if outdata["triggers"]:
				logging.debug("Writing triggers to influx...")
				self.influx_sink.store_columns("triggers", outdata["triggers"], aggregate = "min")

			## Then store missed_triggers, these do not get aggregated
			if outdata["missed_triggers"]:
				logging.debug("Writing missed triggers to influx...")
				self.influx_sink.store_columns("missed_triggers", outdata["missed_triggers"], aggregate = None)

	def sort_ifos(self, string):
		if not string:
			return 'None'
		else:
			# return the sorted string of IFOs in alphabetical order
			list = string.split(',')
			list.sort()
			return ','.join(list)



def main():
	# parse options from command line
	opts, args = parse_command_line()

	# set up logging
	utils.set_up_logger(opts.verbose)

	# initialize the processor
	processor = InjMissedFound(opts)
	processor.start()

if __name__ == '__main__':
	main()
