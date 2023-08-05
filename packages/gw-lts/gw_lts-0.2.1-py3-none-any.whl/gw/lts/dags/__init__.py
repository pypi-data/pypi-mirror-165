#!/usr/bin/env python

import htcondor
import itertools
import yaml
from yaml.loader import SafeLoader

def add_job_opts(job):

	opts = {'executable': f'env/bin/{job}',
		'error':f'logs/{job}-$(cluster)-$(process).err',
		'output':f'logs/{job}-$(cluster)-$(process).out',
		}
	return opts

def add_job_args(opts):
	args = ''
	for (k, v) in opts.items():
		if isinstance(v, list):
			for vv in v:
				args += f'--{k.replace("_", "-")} {vv} '
		elif type(v) == bool and v:
			args += f'--{k.replace("_", "-")} '
		elif type(v) == bool:
			continue
		else:
			args += f'--{k.replace("_", "-")} {v} '
	return {'arguments': args}

def get_topics(datasource, topic_suffix, tag):
	topics = []
	if len(datasource) >= len(topic_suffix):
		combinations = [list(zip(p, topic_suffix)) for p in itertools.permutations(datasource, len(topic_suffix))]
	else:
		combinations = [list(zip(datasource, p)) for p in itertools.permutations(topic_suffix, len(datasource))]
	for c in combinations:
		for pipeline, topic in c:
			topics.append(f'{pipeline}.{tag}.{topic}')
	return topics

def add_common_args(config, job):
	job_args = {}
	job_args.update({
				'tag': config['tag'],
				'kafka_server': config['kafka_server'],
	})

	for arg, val in config['jobs'][job].items():
		# input topic arg is handled differently
		if arg == 'input_topic':
			continue
		job_args.update({arg: val})

	return job_args

def send_inj_stream_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('send-inj-stream'))

	job_args = {}
	
	# add job arguments
	job_args.update(add_common_args(config, 'send_inj_stream'))
	job_args.update({'data_source': config['data-source']})
	job_args.update({'inj-file': config['injections']})
	job_args.update({'ifo': [ifo for ifo in config['ifos'].split(',')]})
	if 'track-psd' in config['jobs']['send_inj_stream'] or 'track-segments' in config['jobs']['send_inj_stream']:
		job_args.update({'input-topic': [topic for topic in config['jobs']['send_inj_stream']['input_topic']]})

	opts.update(add_job_args(job_args))

	# add job to the dag
	dag.layer(name='send_inj_stream', submit_description = htcondor.Submit(opts), retries = '3')
	return dag

def inspinjmsg_find_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('inspinjmsg-find'))

	job_args = {}
	
	# add job arguments
	job_args.update(add_common_args(config, 'inspinjmsg_find'))
	tag = config['tag']
	topics = get_topics(config['data-source'], config['jobs']['inspinjmsg_find']['input_topic'], tag)
	job_args.update({'input_topic': topics})
	opts.update(add_job_args(job_args))

	# add job to the dag
	dag.layer(name='inspinjmsg_find', submit_description = htcondor.Submit(opts), retries = '3')
	return dag

def igwn_alert_listener_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('igwn-alert-listener'))

	job_args = {}
	
	# add job arguments
	job_args.update(add_common_args(config, 'igwn_alert_listener'))
	job_args.update({'group': config['group']})
	opts.update(add_job_args(job_args))

	# add job to the dag
	dag.layer(name='igwn_alert_listener', submit_description = htcondor.Submit(opts), retries = '3')
	return dag

def inj_missed_found_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('inj-missed-found'))
	for i, source in enumerate(config['data-source']):
		job_args = {}
		
		# add job arguments
		job_args.update(add_common_args(config, 'inj_missed_found'))
		tag = config['tag']
		topics = get_topics([source], config['jobs']['inj_missed_found']['input_topic'], f'{tag}.testsuite')
		job_args.update({'input_topic': topics})
		job_args.update({'scald_config': config['metrics'][source]['config']})
		opts.update(add_job_args(job_args))

		# add job to the dag
		dag.layer(name=f'inj_missed_found_{int(i):04d}', submit_description = htcondor.Submit(opts), retries = '3')
	return dag

def vt_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('vt'))

	for i, source in enumerate(config['data-source']):
		job_args = {}

		# add job arguments
		job_args.update(add_common_args(config, 'vt'))
		job_args.update({'data_source': source})
		tag = config['tag']
		topics = get_topics([source], config['jobs']['vt']['input_topic'], f'{tag}.testsuite')
		job_args.update({'input_topic': topics})
		job_args.update({'inj-file': config['injections']})

		if 'bootstrap-vt' in job_args.keys():
			job_args.update({'scald-config': f'{config["metrics"][source]["config"]}'})

		opts.update(add_job_args(job_args))

		if 'calculate-expected' in job_args.keys():
			# add the expected VT job
			dag.layer(name=f'vt_{(2 * int(i)):04d}', submit_description = htcondor.Submit(opts), retries = '3')

			# remove the options for expected VT calculation
			# and add the regular VT job to dag
			job_args.pop('calculate-expected')
			input_topics = [x for x in job_args['input_topic'] if not 'missed_inj' in x]
			job_args.update({'input_topic': input_topics})
			opts.update(add_job_args(job_args))
			dag.layer(name=f'vt_{(2 * int(i) + 1):04d}', submit_description = htcondor.Submit(opts), retries = '3')

		else:
			dag.layer(name=f'vt_{int(i):04d}', submit_description = htcondor.Submit(opts), retries = '3')

	return dag

def latency_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('latency'))

	job_args = {}
	
	# add job arguments
	job_args.update(add_common_args(config, 'latency'))
	tag = config['tag']
	topics = get_topics(config['data-source'], config['jobs']['latency']['input_topic'], f'{tag}.testsuite')
	job_args.update({'input_topic': topics})
	opts.update(add_job_args(job_args))

	# add job to the dag
	dag.layer(name='latency', submit_description = htcondor.Submit(opts), retries = '3')
	return dag

def likelihood_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('likelihood'))

	job_args = {}

	# add job arguments
	job_args.update(add_common_args(config, 'likelihood'))
	tag = config['tag']
	topics = get_topics(config['data-source'], config['jobs']['likelihood']['input_topic'], f'{tag}.testsuite')
	job_args.update({'input_topic': topics})
	opts.update(add_job_args(job_args))

	# add job to the dag
	dag.layer(name='likelihood', submit_description = htcondor.Submit(opts), retries = '3')
	return dag

def p_astro_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('p-astro'))

	job_args = {}
	
	# add job arguments
	job_args.update(add_common_args(config, 'p_astro'))
	tag = config['tag']
	topics = get_topics(config['data-source'], config['jobs']['p_astro']['input_topic'], f'{tag}.testsuite')
	job_args.update({'input_topic': topics})
	if 'gdb-skymaps' in job_args.keys():
		job_args.update({'group': config['group']})
	opts.update(add_job_args(job_args))

	# add job to the dag
	dag.layer(name='p_astro', submit_description = htcondor.Submit(opts), retries = '3')
	return dag

def skymap_layer(dag, config, opts):
	# add job options
	opts.update(add_job_opts('skymap'))

	job_args = {}
	
	# add job arguments
	job_args.update(add_common_args(config, 'skymap'))
	tag = config['tag']
	topics = get_topics(config['data-source'], config['jobs']['skymap']['input_topic'], f'{tag}.testsuite')
	job_args.update({'input_topic': topics})
	if 'gdb-skymaps' in job_args.keys():
		job_args.update({'group': config['group']})
	opts.update(add_job_args(job_args))

	# add job to the dag
	dag.layer(name='skymap', submit_description = htcondor.Submit(opts), retries = '3')
	return dag

def snr_consistency_layer(dag, config, opts):
	for i, ifo in enumerate(config['ifos'].split(',')):
		# add job options
		opts.update(add_job_opts('snr-consistency'))
	
		job_args = {}

		# add job arguments
		job_args.update(add_common_args(config, 'snr_consistency'))
		tag = config['tag']
		topics = get_topics(config['data-source'], [f'{ifo}_{t}' for t in config['jobs']['snr_consistency']['input_topic']], f'{tag}.testsuite')

		job_args.update({'input_topic': topics})
		job_args.update({'ifo': ifo})
		opts.update(add_job_args(job_args))

		# add job to the dag
		dag.layer(name=f'snr_consistency_{int(i):04d}', submit_description = htcondor.Submit(opts), retries = '3')

	return dag

def inj_accuracy_layer(dag, config, opts):
	for i, ifo in enumerate(config['ifos'].split(',')):
		# add job options
		opts.update(add_job_opts('inj-accuracy'))

		job_args = {}

		# add job arguments
		job_args.update(add_common_args(config, 'inj_accuracy'))
		tag = config['tag']
		topics = get_topics(config['data-source'], config['jobs']['inj_accuracy']['input_topic'], f'{tag}.testsuite')
		job_args.update({'input_topic': topics})
		job_args.update({'ifo': ifo})
		opts.update(add_job_args(job_args))

		# add job to the dag
		dag.layer(name=f'inj_accuracy_{int(i):04d}', submit_description = htcondor.Submit(opts), retries = '3')

	return dag

def collect_metrics_layer(dag, config, config_path, opts):
	# load options from the config

	kafka_server = config['kafka_server']
	tag = config['tag']

	for i, source in enumerate(config['data-source']):
		web_config_path = config['metrics'][source]['config']
		# grab the web config
		with open(web_config_path, 'r') as f:
			web_config = yaml.load(f, Loader=SafeLoader)

		# add job options
		opts.update({'executable': 'env/bin/scald',
			'error':'logs/scald_metric_collector-$(cluster)-$(process).err',
			'output':'logs/scald_metric_collector-$(cluster)-$(process).out',
			})
		arguments = f'aggregate --config {web_config_path} --uri kafka://{tag}@{kafka_server} --data-type timeseries'

		metrics = [metric for metric in web_config['schemas']]

		# these metrics are special, they dont get aggregated
		# by the metric collector
		for metric in ['triggers', 'missed_triggers', 'analysis_start']:
			if metric in metrics:
				metrics.remove(metric)

		for metric in metrics:
			arguments += f' --topic {source}.{tag}.testsuite.{metric} --schema {metric}'

		opts.update(opts)
		opts.update({'arguments': arguments})

		dag.layer(name=f'scald_metric_collector_{i:04d}', submit_description = htcondor.Submit(opts), retries = '3')

	return dag
