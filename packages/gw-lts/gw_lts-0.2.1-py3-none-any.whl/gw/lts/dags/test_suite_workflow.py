#!/usr/bin/env python

import logging
import sys
import os
import tempfile
import itertools
from optparse import OptionParser

import yaml
from yaml.loader import SafeLoader

import htcondor
from htcondor import dags

from gw.lts import utils
from gw.lts import dags

def parse_command_line():
	parser = OptionParser()
	parser.add_option('-v', '--verbose', action='store_true', help='Be verbose.')
	parser.add_option('-c', '--config', help = 'Path to config.yml.')
	parser.add_option('-n', '--name', default = 'test_suite', help = 'Name for the DAG file.')
	opts, args = parser.parse_args()

	return opts, args


class DAG(object):
	def __init__(self, config_path, name, verbose):
		self.jobs = {
				'send_inj_stream': dags.send_inj_stream_layer,
				'inspinjmsg_find': dags.inspinjmsg_find_layer,
				'igwn_alert_listener': dags.igwn_alert_listener_layer,
				'inj_missed_found': dags.inj_missed_found_layer,
				'vt': dags.vt_layer,
				'latency': dags.latency_layer,
				'p_astro': dags.p_astro_layer,
				'skymap': dags.skymap_layer,
				'snr_consistency': dags.snr_consistency_layer,
				'inj_accuracy': dags.inj_accuracy_layer,
				'likelihood': dags.likelihood_layer,
				'scald_metric_collector': dags.collect_metrics_layer,
		}

		self.config_path = config_path
		self.config = self.load_config(self.config_path)
		self.retries = '3'

		self.dag_name = name
		self.dag = htcondor.dags.DAG()

		self.verbose = verbose

	def load_config(self, config_path):
		config = {}
	
		with open(config_path, 'r') as f:
			config = yaml.load(f, Loader=SafeLoader)
	
		return config

	def create_dag(self):
		if self.verbose: print('Building DAG...')
		opts = self.condor_opts()

		# add jobs
		for job in self.config['jobs']:
			self.dag = self.jobs[job](self.dag, self.config, opts)

		# add a scald metric collector job for each datasource
		self.dag = self.jobs['scald_metric_collector'](self.dag, self.config, self.config_path, opts)

		if self.verbose: print(f'Writing DAG out to file: {self.dag_name}.dag')
		htcondor.dags.write_dag(self.dag, os.getcwd(), dag_file_name=f'{self.dag_name}.dag')

		return self.dag

	def write_script(self):
		if self.verbose: print(f'Writing script out to file: {self.dag_name}.sh')
		with open(f'{self.dag_name}.sh', 'w') as f:
			jobnames = []
			for layer in self.dag.walk():
				executable = layer.submit_description['executable']
				args = layer.submit_description['arguments']
				jobname = executable.split('/')[-1]
	
				jobnames.extend([jobname])
				if jobname in jobnames:
					jobname = jobname + f'_{int(jobnames.count(jobname)):04d}'
	
				print(f'# Job {jobname}', file=f)
				print(executable + ' ' + args + '\n', file=f)

	def condor_opts(self):
		# set up condor logging
		tempfile.tempdir = os.environ['TMPDIR']
		fd, logfile = tempfile.mkstemp()
		with os.fdopen(fd, 'w') as f:
			pass
	
		# set up general condor options across all jobs
		opts = {
			'want_graceful_removal': True,
			'getenv': True,
			'kill_sig': 15,
			'log': logfile,
			'notification': 'never',
			}
		if self.config["singularity-image"]:
			opts.update({
				'MY.SingularityImage': f'\"{self.config["singularity-image"]}\"'
			})
		opts.update(self.config['condor'])

		return opts

def main():
	# parse command line options
	opts, args = parse_command_line()

	if not opts.config: 
		raise Exception('You need to specify a config file.')

	# build the dag
	dag_generator = DAG(opts.config, opts.name, opts.verbose)

	dag = dag_generator.create_dag()
	dag_generator.write_script()
	
	# make a directory for logs
	if not os.path.exists('logs'): os.mkdir('logs')

if __name__ == '__main__':
	main()
