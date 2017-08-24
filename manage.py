import os, sys, json
from linux_oper import *

def gunicorn_start(config):
    ShellRun('nohup gunicorn -w 4 --threads=4 --chdir=%s %s:%s -b %s:%s &' % (
            os.path.join(config['path'], config['project']), 
            config['main_file'], config['main_route'], 
            config['host'], config['local_port']))
def stop():
    try:
        with open('setup_config.dat', 'r') as f:
            json.load(config, f)
        port_unlocker(config['port'])
    except:
        trprint('error ! Config file NOT found. ')
    else:
        trprint('Web Service stopped.')
        if input('Stop the nginx service ? (y/n)').lower() in ('y', 'yes'):
            ShellRun('nginx -s stop')

def start():
    global config
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

def reload():
    global config
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
try:
    try:
        with open('setup_config.dat', 'r') as f: json.load(config, f)
    except:
        trprint('Error ! Config file not found. ')
    else:
        trprint('Found the config file. ')
    switch[sys.argv[1]]()
except:
    print('Cannot find this command.')
