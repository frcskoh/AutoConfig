import os, sys, json
from linux_oper import *

def stop():
    try:
        f = open('setup_config.dat', 'r')
        json.load(config, f)
        port_unlocker(config['port'])
    except:
        trprint('error !')
    else:
        trprint('uWSGI service stopped.')
        if input('Stop the nginx service now ? (y/n)').lower() in ('y', 'yes'): os.system('nginx -s stop')

    return None

def start():
    try:
        f = open('setup_config.dat', 'r')
        json.load(config, f)
        port_unlocker(config['port'])
    except:
        trprint('error !')
        
    try:
        os.system('service nginx start')
        os.system('nohup uwsgi config.ini &')
    except:
        trprint('error !')

    return None

def restart():
    try:
        f = open('setup_config.dat', 'r')
        json.load(config, f)
        port_unlocker(config['port'])
    except:
        trprint('error !')

    try:
        os.system('service nginx start')
        os.system('nohup uwsgi config.ini &')
    except:
        trprint('error !')

    os.system('nginx -s restart')

switch = {'start' : start, 'restart' : restart, 'stop' : stop}
switch[sys.argv[1]]()
