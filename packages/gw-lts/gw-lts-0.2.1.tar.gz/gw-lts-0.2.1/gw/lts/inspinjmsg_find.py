#!/usr/bin/env python3

from optparse import OptionParser
import os
import io
import sys
import json
import copy
import logging

from collections import defaultdict, deque, OrderedDict

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils

from lal import GPSTimeNow

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--preferred-event', metavar = 'func:param', default = 'max:snr', help = 'Parameter and function to use to determine preferred events in the case that multiple event messages are found for a single injection. ' +
		'Supported options are min:combined_far, max:snr, latest:msg_time, or first:msg_time')
	opts, args = parser.parse_args()

	return opts, args

class InspInjMsgFind(object):
	def __init__(self, options):
		self.tag = options.tag
		self.kafka_server = options.kafka_server
		self.topics = options.input_topic
		self.preferred_func = utils.preferred_event_func(options.preferred_event.split(':')[0])
		self.preferred_param = options.preferred_event.split(':')[1]
		self.verbose = options.verbose

		# initialize data deques
		# if injections come every ~20 seconds this should correspond 
		# to keeping messages for about 3-4 minutes.
		self.maxlen = 10
		self.event_msgs = defaultdict(lambda: deque(maxlen=self.maxlen))
		self.inj_msgs = defaultdict(lambda: deque(maxlen=self.maxlen))
		self.msgs_sent = defaultdict(lambda: OrderedDict())

		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{self.kafka_server}')

		# create a job service using cronut
		self.app = App('inspinjmsg_find', broker=f'kafka://{self.tag}_inspinjmsg_find@{self.kafka_server}')

		@self.app.process(self.topics)
		def process(message):
			mtopic = message.topic().split('.')[-1]
			mpipeline = message.topic().split('.')[0]

			# unpack data from the message
			if mtopic == 'inj_events':
				# parse event info
				event = json.loads(message.value())

				# load the coinc table
				coinc_file = utils.load_xml(event['coinc'])
				coinctable = lsctables.CoincInspiralTable.get_table(coinc_file)

				# get event coalescence time
				coinctime = coinctable[0].end_time + 10.**-9. * coinctable[0].end_time_ns
				logging.info(f'received {mpipeline} event with coalescence time: {coinctime}')

				dict = {
					'time': coinctime,
					'coinc': coinc_file,
					'msg_time': int(GPSTimeNow()),
				}

				# add optional keys - these may or may not
				# already be present depending on the data
				# source configuration
				for key in ['latency', 'p_astro', 'uid']:
					if key in event.keys():
						dict.update({key: event[key]})
					else:
						dict.update({key: None})

				# store event data
				self.event_msgs[mpipeline].append(dict)

				self.process_events(mpipeline)
				self.process_stale_msgs(mtopic, mpipeline)

			elif mtopic == 'inj_stream':
				# parse inj info
				injection = json.loads(message.value())
				ifos = injection['onIFOs']

				# load the sim table
				simfile = utils.load_xml(injection['sim'])
				simtable = lsctables.SimInspiralTable.get_table(simfile)

				# get injection coalescence time
				coinctime = simtable[0].geocent_end_time + 10.**-9 * simtable[0].geocent_end_time_ns
				logging.info(f'received {mpipeline} injection with coalescence time: {coinctime}')

				# store inj data
				self.inj_msgs[mpipeline].append({
								'time': coinctime,
								'sim': simfile,
								'ifos': ifos
				})

				self.process_events(mpipeline)
				self.process_stale_msgs(mtopic, mpipeline)

			else:
				# break
				logging.debug(f'Error: Found unexpected message from topic {mtopic}.')


	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


	def append_sim_table(self, coinc_file, sim_file):
		# init a new sim inspiral table
		this_sim_table = lsctables.SimInspiralTable.get_table(sim_file)
		coinc_file.childNodes[-1].appendChild(this_sim_table)

		return coinc_file


	def write_sim_file(self, sim, xmldoc):
		# open a new xml doc
		sim_msg = io.BytesIO()
		ligolw_elem = xmldoc.appendChild(ligolw.LIGO_LW())

		output_simtable = ligolw_elem.appendChild(lsctables.New(lsctables.SimInspiralTable))
		this_sim_table = lsctables.SimInspiralTable.get_table(sim)
		output_simtable.extend(this_sim_table)
		ligolw_utils.write_fileobj(xmldoc, sim_msg, gz = False)

		return sim_msg


	def construct_event_ouput(self, xmldoc, event, injection, key=None):
		filename = f'coinc-{int(event["time"])}.xml' if not key else f'{key}-coinc-{int(event["time"])}.xml'

		coinctable = lsctables.CoincInspiralTable.get_table(event['coinc'])

		ligolw_utils.write_filename(xmldoc, os.path.join('coincs', filename), verbose = self.verbose)
		coinc_msg = io.BytesIO()
		ligolw_utils.write_fileobj(xmldoc, coinc_msg, gz = False)

		output = {
			'time': coinctable[0].end_time,
			'time_ns': coinctable[0].end_time_ns,
			'snr': coinctable[0].snr,
			'far': coinctable[0].combined_far,
			'p_astro': event['p_astro'],
			'coinc': coinc_msg.getvalue().decode(),
			'latency': event['latency'],
			'uid': event['uid'],
			'onIFOs': injection['ifos']
			}

		return output


	def process_events(self, pipeline):
		# for each event in the event_msgs deque, find the nearest injection in inj_msgs
		# within +/- delta_t (1 second) of the event coalescence time.
		# when an association is made, remove both messages from the deques,
		# add the sim inspiral table from injection to the event's coinc xml and 
		# send a message to the testsuite.events topic for all the other jobs to consume
		events_copy = copy.copy(self.event_msgs[pipeline])
		injections = copy.deepcopy(self.inj_msgs[pipeline])
		for event in events_copy:
			event_time = event['time']

			nearest_inj = utils.find_nearest_msg(injections, event_time)

			# if no associated injection was found, pass
			if not nearest_inj:
				continue

			inj_time = nearest_inj['time']
			sim_file = nearest_inj['sim']

			# remove the event from the deque and unpack info
			self.event_msgs[pipeline].remove(event)
			coinc_file = event['coinc']
			this_coinc = lsctables.CoincInspiralTable.get_table(coinc_file)

			time_now = int(GPSTimeNow())
			if self.preferred_param == 'combined_far' or self.preferred_param == 'snr':
				val = this_coinc.getColumnByName(self.preferred_param)[0]
			elif self.preferred_param == 'msg_time':
				val = event['msg_time']
			else:
				raise NotImplementedError

			# Note: this requires that aggregate by "latest" works the way we would hope
			if inj_time in self.msgs_sent[pipeline].keys():
				vals = list(self.msgs_sent[pipeline][inj_time].values()) + [val]
				if not val is self.preferred_func(vals):
					logging.debug(f'New event for injection: {inj_time}. This {self.preferred_param} {val} not preferred to send an update msg, continuing.')
					continue
				# wait some time before sending an update message
				if not time_now - max(self.msgs_sent[pipeline][inj_time].keys()) >= 10.:
					continue
				logging.debug(f'New event for injection {inj_time}. This {self.preferred_param} {val} is preferred, sending an update msg')
				self.msgs_sent[pipeline][inj_time].update({time_now: val})
			else:
				logging.debug(f'Initial event found for injection {inj_time} with {self.preferred_param} {val}.')
				self.msgs_sent[pipeline][inj_time] = {time_now: val}

			# proceed with sending event
			# add sim table to coinc file and write to disk
			newxmldoc = self.append_sim_table(coinc_file, sim_file)

			output = self.construct_event_ouput(newxmldoc, event, nearest_inj)

			self.client.write(f'{pipeline}.{self.tag}.testsuite.events', output)
			logging.info(f'Sent msg to: {pipeline}.{self.tag}.testsuite.events')
			newxmldoc.unlink()


	def process_stale_msgs(self, topic, pipeline):
		# process old messages: either messages that are about to be 
		# removed from the left of the deque, or have been in the deque
		# for 2 hours, and send a message with the necessary info
		# this is necessary in the case that:
			# 1) we receive an event from the search which is not
			# associated with an injection, ie a glitch or real gw 
			# candidate.
			# 2) there is an injection for which we never receive
			# an associated event from the search. ie the injection
			# was not recovered at even the GDB far threshold.
		# FIXME dont hardcode wait time
		if self.inj_msgs[pipeline] and ((len(self.inj_msgs[pipeline]) == self.maxlen) or (float(GPSTimeNow()) - self.inj_msgs[pipeline][0]['time'] >= 7200.)):
			stale_msg = self.inj_msgs[pipeline][0]

			if topic == 'inj_events':
				logging.debug(f'{pipeline} event from time {stale_msg["time"]} to be removed from the queue - no associated injection found')

			elif topic == 'inj_stream':
				sim_inspiral = stale_msg['sim']

				if not stale_msg['time'] in self.msgs_sent[pipeline].keys():
					logging.debug(f'Sending {pipeline} missed injection msg for injection {stale_msg["time"]}')
					simtable = lsctables.SimInspiralTable.get_table(sim_inspiral)
					newxmldoc = ligolw.Document()
					sim_msg = self.write_sim_file(sim_inspiral, newxmldoc)

					output = {
						'time': simtable[0].geocent_end_time,
						'time_ns': simtable[0].geocent_end_time_ns,
						'sim': sim_msg.getvalue().decode(),
						'onIFOs': stale_msg['ifos'],
					}

					self.client.write(f'{pipeline}.{self.tag}.testsuite.missed_inj', output)
					logging.info(f'Sent msg to: {pipeline}.{self.tag}.testsuite.missed_inj')
					newxmldoc.unlink()


def main():
	# parse options from command line
	opts, args = parse_command_line()

	# set up logging
	utils.set_up_logger(opts.verbose)

	# set up dir for output coincs
	try:
		os.mkdir('coincs')
	except OSError as error:
		pass

	# initialize the processor
	processor = InspInjMsgFind(opts)
	processor.start()

if __name__ == '__main__':
	main()
