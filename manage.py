import os, sys, json
from linux_oper import *
work_path = os.path.split(os.path.abspath(sys.argv[0]))[0]

def receive():
    trprint(os.path.join(work_path, 'setup_config.dat'))
    config = None
    try:
        with open(os.path.join(work_path, 'setup_config.dat'), 'r') as f: json.load(config, f)
    except IOError:
        trprint('Error ! Config file not found. ')
    else:
        return config

def gunicorn_start(config):
    ShellRun('nohup gunicorn -w 4 --threads=4 --chdir=%s %s:%s -b %s:%s \&' % (
            os.path.join(config['path'], config['project']), 
            config['main_file'], config['main_route'], 
            config['host'], config['local_port']))

def stop(config):
    try:
        port_unlocker(config['port'])
    except:
        trprint('error ! Config file NOT found. ')
    else:
        trprint('Web Service stopped.')
        if input('Stop the nginx service ? (y/n)').lower() in ('y', 'yes'):
            ShellRun('nginx -s stop')

def start(config):
    try:
        port_unlocker(config['port'])
        gunicorn_start(config)
    except:
        trprint('error !')
    else:  
        try:
            ShellRun('service nginx start')
        except:
            trprint('error !')
        else:
            trprint('Task Started. ')

def reload(config):
    try:
        ShellRun('git pull -f')
        port_unlocker(config['port'])
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
