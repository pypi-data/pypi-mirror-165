#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import numpy
import copy
import logging

from time import sleep
from collections import defaultdict, deque
from confluent_kafka import Producer

from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables
from lal import GPSTimeNow
from lal import LIGOTimeGPS

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--ifo', help = 'Interferometer to get data from')
	opts, args = parser.parse_args()

	return opts, args

class SNRConsistency(object):
	def __init__(self, options):
		self.ifo = options.ifo
		self.tag = options.tag
		self.kafka_server = options.kafka_server
		self.topics = options.input_topic

		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{self.kafka_server}')

		# initialize data deque and output dict
		self.data = defaultdict(lambda: defaultdict(lambda: deque(maxlen=300)))
		
		# create a job service using cronut
		self.app = App('snr_consistency', broker=f'kafka://{self.tag}_{self.ifo}_snr_consistency@{self.kafka_server}')

		# subscribes to a topic
		@self.app.process(self.topics)
		def process(message):
			mifo, mtopic = message.topic().split('.')[-1].split('_')
			mpipeline = message.topic().split('.')[0]
			mkey = message.key().decode('utf-8')
		
			source, is_recovered = mkey.split('.')
			logging.info(f'Read message from input {mpipeline} {mtopic}: {source} {is_recovered}')

			# unpack data from the message 
			# store SNRs in a dictionary keyed by event time
			m = json.loads(message.value())
			val = m['data'][-1]
			time = m['time'][-1]

			if is_recovered == 'missed':
				logging.debug(f"Injection at {time} missed, skipping.")
			else:
				time_window = utils.event_window(time)

				self.data[mpipeline][mtopic].append({
								'time': time,
								'snr': val
				})

				self.process_msgs(mpipeline)


	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


	def process_msgs(self, pipeline):
		# for each reecovered msg time in the deque
		# find the nearest injection in injected msgs deque
		# within +/- delta_t (1 second) of the recovered msg
		# time. When an association is made, remove the recovered
		# msg from the deque, calculate the snr accuracy and
		# send a message to the output topic
		recovered = copy.copy(self.data[pipeline]['recsnr'])
		for rec in recovered:

			rec_time = rec['time']
			rec_snr = rec['snr']

			nearest_inj = utils.find_nearest_msg(self.data[pipeline]['injsnr'], rec_time)

			if not nearest_inj:
				continue

			inj_time = nearest_inj['time']
			inj_snr = nearest_inj['snr']

			self.data[pipeline]['recsnr'].remove(rec)

			accuracy = 1. - (inj_snr - rec_snr) / inj_snr

			output = {
					'time': [ inj_time ],
					'data': [ accuracy ]
			}

			self.client.write(f'{pipeline}.{self.tag}.testsuite.{self.ifo}_snr_accuracy', output)
			logging.info(f'Sent msg to: {pipeline}.{self.tag}.testsuite.{self.ifo}_snr_accuracy')

def main():
	opts, args = parse_command_line()

	# sanity check input options
	required_opts = ['ifo', 'tag', 'input_topic', 'kafka_server']
	for r in required_opts:
		if not getattr(opts, r):
			raise ValueError(f'Missing option: {r}.')

	# set up logging
	utils.set_up_logger(opts.verbose)

	# start up processor
	processor = SNRConsistency(opts)
	processor.start()

if __name__ == '__main__':
	main()
