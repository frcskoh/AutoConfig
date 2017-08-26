import os, sys, json
from linux_oper import *
work_path = os.path.split(os.path.abspath(sys.argv[0]))[0]

def receive():
    trprint(os.path.join(work_path, 'setup_config.dat'))
    try:
        with open(os.path.join(work_path, 'setup_config.dat'), 'r') as f: config = json.load(f)
    except IOError:
        trprint('Error ! Config file not found. ')
    else:
        print(config)
        return config

def gunicorn_start(config, thread = '4', worker = '4'):
    os.chdir(os.path.join(config['path'], config['project']))
    ShellRun('nohup gunicorn -w %s --threads %s -b %s:%s %s:%s \&' % (
            worker, thread, config['host'], config['local_port'], 
            config['main_file'].split('.')[0], config['main_route']))

def stop(config):
    try:
        port_unlocker(config['local_port'])
    except:
        trprint('OS Error ! ')
    else:
        trprint('Web Service stopped.')
        if input('Stop the nginx service ? (y/n)').lower() in ('y', 'yes'):
            ShellRun('nginx -s stop')

def start(config):
    try:
        port_unlocker(config['local_port'])
    except:
        trprint('OS Error !')
    else:
        gunicorn_start(config)
        try:
            ShellRun('service nginx start')
        except:
            trprint('Starting the nginx Error !')
        else:
            trprint('Task Started. ')

def reload(config):
    try:
        ShellRun('git pull -f')
        port_unlocker(config['local_port'])
    except:
        trprint('Error !')
    else:
        print('Updated the file and Killed the task')
        try:
            os.system('nginx -s restart')
            gunicorn_start(config)
        except:
            trprint('Error !')
        else:
            print('Started the task successfullly. ')

switch = {'start' : start, 'restart' : reload, 'stop' : stop}
switch[sys.argv[1]](receive())
