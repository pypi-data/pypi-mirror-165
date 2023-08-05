#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import logging
import copy

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse
from io import BytesIO

from ligo.lw import lsctables
from ligo.lw.utils import load_fileobj

from lal import GPSTimeNow

from ligo.skymap.bayestar import localize
from ligo.skymap.io import events as LIGOSkymapEvents
from ligo.skymap.io import read_sky_map
from ligo.skymap.postprocess import crossmatch

from astropy.coordinates import SkyCoord
from astropy.table import Table

from ligo.scald.io import kafka

from gw.lts import utils
from gw.lts.utils.gracedb_helper import GraceDbHelper

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--output', help = 'Output directory to write skymap fits files to.')
	parser.add_option('--gdb-skymaps', action='store_true', default = False, help = 'Use skymaps from GraceDB instead of calculating them manually.')
	opts, args = parser.parse_args()

	return opts, args

class Skymap(object):
	def __init__(self, options):
		self.tag = options.tag
		self.kafka_server = options.kafka_server
		self.topics = options.input_topic
		self.output_dir = options.output

		self.gdb_skymaps = options.gdb_skymaps

		if self.gdb_skymaps:
			self.gracedb_helper = GraceDbHelper(options.group)
		
		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{self.kafka_server}')

		self.events = deque(maxlen=10)
	
		# create a job service using cronut
		self.app = App('skymap', broker=f'kafka://{self.tag}_skymap@{self.kafka_server}')
		
		# subscribes to a topic
		@self.app.process(self.topics)
		def process(message): 
			mtopic = message.topic().split('.')[-1]
			mpipeline = message.topic().split('.')[0]
			mkey = utils.parse_msg_key(message)
			logging.info(f'Read message from {mpipeline} {mtopic}.')
		
			# parse event info
			event = json.loads(message.value())
			time = event['time'] + event['time_ns'] * 10**-9.
			event.update({'pipeline': mpipeline})
		
			# process the eventt - get a skymap and calculate
			# searched area and probability, send messages to
			# kafka
			response = self.process_event(event)
			if not response:
				# keep track of events that failed
				# to get a skymap on the first try
				# when getting skymaps from gracedb, this
				# can happen if the skymap isnt uploaded
				# immediately
				times = [e["time"] for e in self.events]
				if not event["time"] in times:
					self.events.append(event)
		
			# iterate over events and try again to grab a
			# skymap for each one. On success, remove the
			# event from the deque
			for e in copy.deepcopy(self.events):
				response = self.process_event(e)
				if response:
					self.events.remove(e)


	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


	def process_event(self, event):
		# either download skymap from gracedb or
		# generate one with bayestar
		if self.gdb_skymaps:
			file = self.gracedb_helper.query_file(event['uid'], 'bayestar.multiorder.fits', outpath = self.output_dir, tag = self.tag)
			if file:
				skymap = Table.read(os.path.join(self.output_dir, f'{self.tag}-{event["uid"]}.fits'))
			else:
				skymap = None
		else:
			skymap = self.make_skymap(event)
	
		if skymap:
			output = {}
			time = event['time']
			pipeline = event['pipeline']

			# get right ascension and declination
			# from sim inspiral table
			coinc = utils.load_xml(event['coinc'])
			simtable = lsctables.SimInspiralTable.get_table(coinc)
			ra, dec = simtable[0].ra_dec
	
			# use SkyCoord and crossmatch to get pvalues
			loc = SkyCoord(ra=ra, dec=dec, unit="rad")
			p = crossmatch(skymap, loc).searched_prob
			deg2 = crossmatch(skymap, loc).searched_area
	
			logging.debug(f'Searched probability: {p} | searched area: {deg2}')
	
			# construct output dict and send messages to kafka
			output['searched_prob'] = {
				'time': [ time ],
				'data': [ p ]
			}
			output['searched_area'] = {
				'time': [ time ],
				'data': [ deg2 ]
			}
	
			for key, value in output.items():
				self.client.write(f'{pipeline}.{self.tag}.testsuite.{key}', value, tags = key)
				logging.info(f'Sent msg to: {pipeline}.{self.tag}.testsuite.{key}')
	
			return True
	
		else:
			return False
	
	def make_skymap(self, event):
		skymap = None
		coinc_obj = BytesIO(event['coinc'].encode())
		# make a copy of coinc file to avoid I/O error in events.ligolw.open()
		psd_obj = copy.copy(coinc_obj)
	
		event_source = LIGOSkymapEvents.ligolw.open(coinc_obj, psd_file=psd_obj, coinc_def=None)
	
		if len(event_source) > 1:
			logging.info('Warning: len(event_source) > 1, defaulting to use the first event.')
	
		# produce the skymap
		for event_id, event in event_source.items():
			skymap = localize(event)
			# break out of the loop after computing just one skymap
			# in case there are multiple rows in coinc inspiral we just
			# go with the first one
			break
	
		return skymap
	

def main():
	opts, args = parse_command_line()

	# set up logging
	utils.set_up_logger(opts.verbose)

	# make a dir for skymaps
	if not os.path.exists(opts.output):
		os.makedirs(opts.output)

	# start up the processor
	processor = Skymap(opts)
	processor.start()

if __name__ == '__main__':
	main()
