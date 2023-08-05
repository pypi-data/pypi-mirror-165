#!/usr/bin/env python3

from optparse import OptionParser
import json
import logging
import copy

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from gw.lts import utils
from gw.lts.utils.gracedb_helper import GraceDbHelper

from ligo.scald.io import kafka

from ligo.lw import lsctables

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--pastro-file', metavar = 'name=file', action = 'append', help = 'Name of the p(astro) method (ex. fgmc or mchirp) and filename to download from GraceDB, given as name=file. Can be given multiple times.')
	parser.add_option('--gdb-pastros', action = 'store_true', default = False, help = 'Download p(astro) files from GraceDB. This will fail if the data source is fake-data.')
	opts, args = parser.parse_args()

	return opts, args

class PAstro(object):
	def __init__(self, options):
		self.tag = options.tag
		self.kafka_server = options.kafka_server
		self.gdb_pastros = options.gdb_pastros

		self.pastro_files = {}
		for option in options.pastro_file:
			name, file = option.split('=')
			self.pastro_files.update({name: file})

		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{options.kafka_server}')

		if self.gdb_pastros:
			self.gracedb_helper = GraceDbHelper(options.group)

		# initialize output dict
		self.events = {name: deque(maxlen=10) for name in self.pastro_files.keys()}

		# create a job service using cronut
		self.app = App('pastro', broker=f'kafka://{self.tag}_pastro@{self.kafka_server}')

		# subscribes to a topic
		@self.app.process(options.input_topic)
		def process(message):
			mtopic = message.topic().split('.')[-1]
			mpipeline = message.topic().split('.')[0]
			mkey = utils.parse_msg_key(message)
			logging.info(f'Read message from {mpipeline} {mtopic}.')

			# parse message value
			event = json.loads(message.value())
			event.update({'pipeline': mpipeline})

			for name, file in self.pastro_files.items():
				response = self.process_event(event, name, file)
				if not response:
					# keep track of events that failed
					# to get a p(astro) on the first try
					# when getting p(astro)s from gracedb, this
					# can happen if the p(astro) isnt uploaded
					# immediately
					times = [e["time"] for e in self.events[name]]
					if not event["time"] in times:
						self.events[name].append(event)

			# iterate over events and try again to grab a
			# p(astro) for each one. On success, remove the
			# event from the deque
			for name, file in self.pastro_files.items():
				for e in copy.deepcopy(self.events[name]):
					response = self.process_event(e, name, file)
					if response:
						self.events[name].remove(e)

	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


	def process_event(self, event, pastro_name, filename):
		if self.gdb_pastros:
			file = self.gracedb_helper.query_file(event['uid'], filename = filename)
			if file:
				p_astro_dict = json.loads(file.read())
			else:
				p_astro_dict = None

		else:
			try:
				p_astro_dict = json.loads(event['p_astro'])
			except KeyError:
				raise KeyError("Event message does not include p(astro) and --gdb-pastros is not given. There is no way to retrieve the p(astro) in this case.")

		if p_astro_dict:
			output = {}
			time = event["time"]
			pipeline = event["pipeline"]

			p_astro_dict['astro'] = 1 - p_astro_dict['Terrestrial']

			# determine source from inspiral table
			coinc_file = utils.load_xml(event['coinc'])
			simtable = lsctables.SimInspiralTable.get_table(coinc_file)
			source = utils.source_tag(simtable)

			for key, value in p_astro_dict.items():
				output['p_' + key] = {
					'time': [ float(time) ],
					'data': [ float(value) ]
				}

			logging.debug(f'{source} event: {pastro_name}: {p_astro_dict}')

			# send message to output topics
			for topic, data in output.items():
				self.client.write(f'{pipeline}.{self.tag}.testsuite.{topic}', data, tags = [pastro_name, source])
				logging.info(f'Sent output message to output topic: {pipeline}.{self.tag}.testsuite.{topic}.')

			return True

		else:
			return False


def main():
	opts, args = parse_command_line()

	# set up logging
	utils.set_up_logger(opts.verbose)

	processor = PAstro(opts)
	processor.start()

if __name__ == '__main__':
	main()
