import os, sys, json
from linux_oper import *

def stop():
    try:
        with open('setup_config.dat', 'r') as f:
            json.load(config, f)
        port_unlocker(config['port'])
    except:
        trprint('error !')
    else:
        trprint('uWSGI service stopped.')
        if input('Stop the nginx service now ? (y/n)').lower() in ('y', 'yes'):
            os.system('nginx -s stop')
    return None

def start():
    try:
        port_unlocker(config['port'])
        os.system("".join('nohup gunicorn --workers=4 ', config['main_file'], ':', config['main_route'], '-b',
                          config['host:config'], ':', config['local_port'], '&')) 
    except:
        trprint('error !')
    else:  
        try:
            os.system('service nginx start')
        except:
            trprint('error !')
        else:
            print('Task Started. ')
    return None

def reload():
    try:
        os.system('git pull -a')
        port_unlocker(config['port'])
    except:
        trprint('Error !')
    else:
        print('Update the file and Killed the task')
        try:
            os.system('nginx -s restart')

switch = {'start' : start, 'restart' : restart, 'stop' : stop}

try:
    switch[sys.argv[1]]()
    try:
        with open('setup_config.dat', 'r') as f: json.load(config, f)
    except:
        trprint('Error ! Config file not found. ')
    else:
        trprint('Found the config file. ')     
except:
    print('Cannot find this command.')
