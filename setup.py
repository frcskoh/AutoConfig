import os, json, sys
from linux_oper import *
from pprint import pprint

def builder():
    config = {}
    
    config.update({'path' : input('Enter the root path : ')})
    config.update({'project' : input('Enter the name of the project : ')})
    config.update({'git_URL' : input('Enter the URL of the git : ')})
    config.update({'main_file' : input('Enter the name of the main file : ')})
    config.update({'main_route' : input('Enter the name of the main route : ')})
    config.update({'ip' : input('Enter the ip address of the service : ')})
    config.update({'host' : input('Enter the address of the localhost : ')})
    config.update({'local_port' : input('Enter the local port : ')})
    config.update({'public port' : input('Enter the public port : ')})
    
    info_trprint('Creating the config file.')
    try:
        pprint(config)
        f = open('setup_config.dat', 'w')
        json.dump(config, f)
        f.close()
    except:
        trprint('error !')
    else:
        if input('Starting the setup now ? (y/n)').lower() in ('y', 'yes'): setup(config)
    
    return f

def uwsgi_config(path, project, main_file, main_route, local_port, processes = '1', threads = '4'):
    os.chdir(path)
    os.chdir(project)

    f = open('config.ini', 'w')

    f.write('[uwsgi]\n')
    f.write('master = true\n')
    f.write('home = ENV\n')
    f.write('wsgi-file = ' + main_file + '\n')
    f.write('callable = ' + main_route + '\n')
    f.write('socket = :' + local_port + '\n')
    f.write('processes = ' + processes + '\n')
    f.write('threads = ' + threads + '\n')
    
    f.write('buffer-size = 32768\n')
      
    f.close()

    info_trprint('Config the uwsgi successfully.')
    return 
    
def nginx_config(project, ip, public_port, path, localhost, main_file, main_route):
    os.chdir('/etc/nginx/sites-enabled/')
    if os.path.exists('default'): os.remove('default')

    f = open(project + '.conf', 'w')
    tab = 4
    
    f.write('server {\n')
    f.write(''.center(tab));f.write('listen ' + public_port + ';\n')
    f.write(''.center(tab));f.write('server_name ' + ip + ';\n')
    f.write(''.center(tab));f.write('access_log ' + path + '/logs/access.log;\n')
    f.write(''.center(tab));f.write('error_log ' + path + '/logs/error.log;\n')
    f.write(''.center(tab));f.write('location / {\n')
    f.write(''.center(tab * 2));f.write('include ' + 'uwsgi_params;\n')
    f.write(''.center(tab * 2));f.write('uwsgi_pass ' + localhost + ';\n')
    f.write(''.center(tab * 2));f.write('uwsgi_param UWSGI_PYHOME ' + path + '/ENV;\n')
    f.write(''.center(tab * 2));f.write('uwsgi_param UWSGI_CHDIR ' + path + ';\n')
    f.write(''.center(tab * 2));f.write('uwsgi_param UWSGI_SCRIPT ' + main_file + ':' + main_route + ';\n')
    f.write(''.center(tab));f.write('}\n')
    f.write('}\n')

    f.close()
    info_trprint('Config the nginx successfully.')
    if not os.path.exists(os.path.join('/etc/nginx/sites-available/', project + '.conf')):
        os.symlink(os.path.join('/etc/nginx/sites-enabled/', project + '.conf'),
                   os.path.join('/etc/nginx/sites-available/', project + '.conf'))
    return

def setup(config):
    safe_command = ('apt-get', 'pip', 'git')
    
    #init
    task_kill(safe_command)
    apt_install(('build-essential -y', 'python3-dev -y', 'virtualenv -y', 'nginx -y', 'git -y'))

    #create
    if not os.path.exists('app'): os.mkdir('app')
    os.chdir(config['path'])

    os.system('git clone ' + config['git_URL'])

    os.chdir(config['project'])
    os.system('virtualenv -p /usr/bin/python3 ENV')

    #install
    os.chdir(os.path.join(config['path'], config['project']))
    pip_install(('-r requirements.txt', 'uwsgi'), 'ENV/bin/')
    uwsgi_config(config['path'], config['project'], config['main_file'], config['main_route'], config['local_port'])

    #Nginx config
    nginx_config(config['project'], config['ip'], config['port'], config['path'], config['host'], config['main_file'], config['main_route'])

    
    if input('Starting the service now ? (y/n)').lower() in ('y', 'yes'):
        import manage
        manage.start()
    
def reader():
    if os.path.exists('setup_config.dat'):
        f = open('setup_config.dat')
        config = json.load(f)
        f.close()

        apt_install(('pip3 -y', ))
        pip_install(('pprint', ))
        
        info_trprint(' ')
        pprint(config)
        info_trprint(' ')
        
        setup(config)
    else:
        trprint('Config file does not exists.')

switch = {'install' : reader, 'build' : builder}
switch[sys.argv[1]]()
