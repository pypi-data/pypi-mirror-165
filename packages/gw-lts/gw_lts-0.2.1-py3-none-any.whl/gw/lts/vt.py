#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import logging
import math
import yaml

from collections import defaultdict, deque

from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils

from lal import GPSTimeNow

from ligo.scald.io import kafka, influx

from gw.lts import utils
from gw.lts.utils import cosmology_utils as cutils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--far-threshold', default=2.314e-5,  help = 'far threshold for missed vs found injections. Default is 2 per day.')
	parser.add_option('--calculate-injected-vt', action='store_true', help='If the injection file doesnt already have an injected VT calculated and stored in Process Params Table , calculate it here on the fly.' + 
		'In this case, max_redshift is required.')
	parser.add_option('--max-redshift', metavar = 'SOURCE:float', action = 'append', help='The max redshift used when generating the injection set.' +
		'Required if --calculate-injected-vt is set. Can be given multiple times.')
	parser.add_option('--bootstrap-vt', action='store_true', default=False, help = 'Whether to load counts for previous found injections from the injection set.' + 
		'This is used to calculate a cumulative VT even if the job is re-started.')
	parser.add_option('--calculate-expected', action='store_true', default=False, help = 'If this is option is set, calculate the expected VT based on assumption that injection with decisive SNR = 8 should be found.' +
		'In this case, the real VT (based on FAR of the recovered injections) is not calculated')

	parser.add_option("--scald-config", metavar = "file", help = "sets ligo-scald options based on yaml configuration.")
	opts, args = parser.parse_args()

	return opts, args

def query_influx(filename, measurement, hostname, db, auth, https, check_certs, num_points = 1, tag = None, dt = None):
	# init consumer
	consumer = influx.Consumer(hostname=hostname, db=db, auth=auth, https=https, check_certs=check_certs)

	# load config
	consumer.load(filename)

	response = consumer.retrieve_timeseries_latest(measurement, 'data', tags=[(tag_name, tag_val) for tag_name, tag_val in tag.items()] if tag else None, dt=dt, num_latest = num_points)

	time, value = response
	if time and value:
		if num_points > 1:
			return time, value
		else:
			return time[0], value[0]
	else:
		logging.debug(f'Could not retrieve last {num_points} data points from {measurement}.')
		return None, None


def injected_VT(pptable, options):
	# parse process params table
	ppdict = {}
	for r in pptable:
		try:
			ppdict.setdefault(str(r.param).strip('--'), []).append(float(r.value))
		except:
			ppdict.setdefault(str(r.param).strip('--'), []).append(r.value)

	# First get total number of injections
	if 'accept' in ppdict and 'reject' in ppdict:
		num_total_injections = sum(ppdict['accept']) + sum(ppdict['reject'])
	elif 'total-generated' in ppdict:
		num_total_injections = sum(ppdict['total-generated'])
	else:
		raise Exception('Could not find total number of attempted injections in file, exiting')

	# try to calculate VT myself
	if num_total_injections and options.calculate_injected_vt and options.max_redshift:
		try:
			omega = cutils.get_cosmo_params()
			gps_start = ppdict['gps-start'][0]
			gps_end = ppdict['gps-end'][0]

			VT = {}
			for z in options.max_redshift:
				source = z.split(':')[0].upper()
				val = float(z.split(':')[1])
			
				VT.update({source: cutils.surveyed_spacetime_volume(gps_start, gps_end, val, omega)})
				logging.debug(f'{source} VT: {VT[source]}')
			VT.update({'VT': sum(VT[source] for source in VT.keys())})

			return VT, num_total_injections
		except:
			 raise Exception('Could not calculate the injected VT, exiting')

	# try getting VT from the injection file
	else:
		try:
			VT = {}
			for item in ['bns-vt', 'nsbh-vt', 'bbh-vt', 'VT']:
				if item in ppdict:
					key = item.split('-')[0].upper()
					VT.setdefault(key, sum(ppdict[item]))
					logging.debug(f'{key} VT: {sum(ppdict[item])}')

			return VT, num_total_injections

		except:
			 raise Exception('Could not get VT from the Process Params Table, exiting')

def parse_msg_value(event, topic):
	time = event['time'] + event['time_ns'] * 10**-9.
	onIFOs = event['onIFOs']

	if topic == 'events':
		far = event['far']
		snr = event['snr']
		file = utils.load_xml(event['coinc'])

	elif topic == 'missed_inj':
		far = None
		snr = None
		file = utils.load_xml(event['sim'])

	simtable = lsctables.SimInspiralTable.get_table(file)

	inj_snrs = defaultdict(lambda: None)
	inj_snrs['H1'] = simtable[0].alpha4
	inj_snrs['L1'] = simtable[0].alpha5
	inj_snrs['V1'] = simtable[0].alpha6

	return time, far, snr, onIFOs, inj_snrs, simtable

def main():
	# parse input options
	opts, args = parse_command_line()
	
	tag = opts.tag
	topic_prefix = 'exp_' if opts.calculate_expected else ''
	far_threshold = float(opts.far_threshold)
	#FIXME this only supports one pipeline source
	pipeline = opts.data_source[0]
	if opts.bootstrap_vt and not opts.scald_config:
		raise Exception('Must specify a scald configuration file if option bootstrap-vt is used')

	# set up producer
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	# load and parse injection file for injected VT and total injections
	inj_file = utils.load_filename(opts.inj_file, gz=True)
	ProcessParamsTable = lsctables.ProcessParamsTable.get_table(inj_file)
	
	inj_VT, total_inj = injected_VT(ProcessParamsTable, opts)
	
	if not inj_VT:
		raise Exception('Injected VT dict is empty, exiting')
	
	# initialize dicts to store data
	num_found = defaultdict(lambda: defaultdict(lambda: deque(maxlen=300)))
	output = defaultdict(lambda: defaultdict(lambda: deque(maxlen = 300)))
	VT_data = defaultdict(lambda: defaultdict(lambda: deque(maxlen = 300)))
	
	startup_time = float(GPSTimeNow())
	
	# load the previous VT data
	if opts.bootstrap_vt:
		# load scald config
		with open(opts.scald_config, 'r') as f:
			config = yaml.safe_load(f)

		# get db name and hostname
		backend = config['backends']['default']
		db = backend['db']
		hostname = backend['hostname']
		auth =  backend['auth']
		https = backend['https']
		check_certs = backend['check_certs']
	
		# get the analysis start time
		_, analysis_start  = query_influx(opts.scald_config, 'analysis_start', hostname, db, auth, https, check_certs)
		if analysis_start:
			startup_time = analysis_start
		else:
			# write analysis start time to influx
			influx_sink = influx.Aggregator(**backend)
			influx_sink.load(path=opts.scald_config)
			influx_sink.store_columns('analysis_start', {'analysis_start': {'time': [ startup_time ], 'fields': {'data': [ startup_time ]}}}, aggregate = None)

		# get number of found injection counts from the last VT data
		for source in inj_VT.keys():
			time, VT = query_influx(opts.scald_config, f'{topic_prefix}vt', hostname, db, auth, https, check_certs, tag = {'source': source}, dt = 1)

			# if there's no previous measurement, start from 0
			if not time or not VT:
				time = startup_time
				VT = 0
	
			# calculate the count of found injections from
			# the VT value and add to num_found deque
			count = int(VT * total_inj / inj_VT[source])
			num_found[pipeline][source].append((float(time), count))
	
			logging.debug(f'Bootstrapping VT for {pipeline} {source} from time: {time}, count: {count}')

	# if not bootstrapping the VT, start the calculation from now and the VTs from 0
	else:
		for source in inj_VT.keys():
			 num_found[pipeline][source].append((startup_time, 0))


	# create a job service using cronut
	app = App('vt', broker=f'kafka://{tag}_{topic_prefix}vt@{opts.kafka_server}')
	
	# subscribes to a topic
	@app.process(opts.input_topic)
	def process(message): 
		mtopic = message.topic().split('.')[-1]
		mpipeline = message.topic().split('.')[0]
		mkey = utils.parse_msg_key(message)
		logging.debug(f'Read message from {mpipeline} {mtopic}')

		# parse message value
		time, far, snr, onIFOs, inj_snrs, simtable = parse_msg_value(json.loads(message.value()), mtopic)

		# dont process old messages and make sure not to double count
		if time > startup_time and not utils.find_nearest_msg(output[mpipeline][f'{topic_prefix}vt'], time):
			source = utils.source_tag(simtable)

			# try calculating source specific VTs, otherwise just calculalte overall VT
			if source in inj_VT:
				key = source
			else:
				key = 'VT'
	
			# determine missed or found
			if opts.calculate_expected:
				decisive_snr = utils.decisive_snr(inj_snrs, onIFOs)
				if decisive_snr:
					is_found = decisive_snr >= 8.
				else:
					logging.warning(f"No decisive SNR, marking this injection as missed")
					is_found = False
			else:
				is_found = far <= far_threshold

			# Count the actual  number of found injections so far
			prev_num_found = num_found[mpipeline][key][-1][1]
			this_num_found = prev_num_found + 1 if is_found else prev_num_found
			num_found[mpipeline][key].append((time, this_num_found))

			# Calculate the current VT
			VT = (this_num_found / total_inj) * inj_VT[key]
			if VT_data[mpipeline][key]:
				assert VT >= VT_data[mpipeline][key][-1], f'Assertion failed: current VT {VT} < prev VT {VT_data[-1]}, which is impossible.'
			VT_data[mpipeline][key].append(VT)
	
			output[mpipeline][f'{topic_prefix}vt'].append({
				'time': time,
				'data': VT
			})
	
			# Calculate the current sensitive volume (scaled for time)
			dt = abs(time - startup_time) / 60. / 60. / 24. / 365.25 # yr
			V = VT / dt
	
			output[mpipeline][f'{topic_prefix}sensitive_vol'].append({
				'time': time,
				'data': V
			})
	
			# Calculate the current range, assuming V is a sphere
			R = (V / (4. * math.pi / 3.))**(1./3.)
	
			output[mpipeline][f'{topic_prefix}range'].append({
				'time': time,
				'data': R
			})
	
			logging.info(f'{mpipeline}: {source} current VT: {VT} Gpc3 yr | V: {V} Gpc3 | range: {R} Gpc')
			for topic, data in output[mpipeline].items():
				out = {
					'time': [ data[-1]['time'] ],
					'data': [ data[-1]['data'] ]
				}
				client.write(f'{mpipeline}.{tag}.testsuite.{topic}', out, tags = key)
				logging.info(f'Sent msg to: {mpipeline}.{tag}.testsuite.{topic}')

	
	# start up
	logging.info('Starting up...')
	app.start()

if __name__ == '__main__':
	main()
