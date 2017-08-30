import os, json, sys, shutil
from linux_oper import *
version = "3.6.2"

app = ('build-essential', 'python3-dev', 'nginx', 'git', )
module = ('gunicorn', )
safe_command = ('apt-get', 'pip', 'git')

def receive():
    global work_path
    global config_path
    global manage_path
    global oper_path
    
    work_path = os.path.join(config['path'], config['project'])
    manage_path = os.path.join(work_path, 'manage.py')
    oper_path = os.path.join(work_path, 'linux_oper.py')
    config_path = os.path.join(work_path, 'setup_config.dat')
    
    try:
        with open(config_path, 'r') as f: config = json.load(f)
    except IOError:
        trprint('Config file does not exists.')
    else:
        trprint('Found the config file. ')
        return config

def builder():
    config = {}
    config.update({'path' : input('Enter the root path : ')})
    config.update({'git_URL' : input('Enter the URL of the git : ')})
    config.update({'project' : os.path.split(config['git_URL'])[-1].split('.')[0]})
    config.update({'main_file' : input('Enter the name of the main file : ')})
    config.update({'main_route' : input('Enter the name of the main route : ')})
    config.update({'ip' : get_ip()})
    config.update({'host' : '127.0.0.1'})
    config.update({'local_port' : input('Enter the local port : ')})
    config.update({'public_port' : input('Enter the public port : ')})
    
    try:
        trprint('Creating the config file....')
        with open('setup_config.dat', 'w') as f:
            json.dump(config, f)
    except:
        trprint('Error ! Building the config file failed. ')
    else:
        trprint('The config file created. ')

def nginx_config(config):
    tab = 4
    try:
        with open(os.path.join('/etc/nginx/sites-enabled/', 'default'), 'a+') as f:
            f.write('server {\n')
            f.write(''.center(tab));f.write('listen %s;\n' % (config['public_port']))
            f.write(''.center(tab));f.write('server_name %s;\n' % (config['ip']))
            f.write(''.center(tab));f.write('location / {\n')
            f.write(''.center(tab * 2));f.write('proxy_pass http://%s:%s;\n' & (config['localhost'], config['local_port']))
            f.write(''.center(tab * 2));f.write('proxy_redirect     off;\n')
            f.write(''.center(tab * 2));f.write('proxy_set_header   X-Real-IP            $remote_addr;\n')
            f.write(''.center(tab * 2));f.write('proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;\n')
            f.write(''.center(tab * 2));f.write('proxy_set_header   X-Forwarded-Proto    $scheme;\n')
            f.write(''.center(tab));f.write('}\n')
            f.write('}\n')
    except IOError:
        print('Building the nginx config file error. ')
    else:
        info_trprint('Config the nginx successfully.')
        if not os.path.exists('/etc/nginx/sites-available/default'):
            ShellRun('mklink -d /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default')

def pyenv_install(version):
    for i in ShellRun('pyenv versions').read().split('\n').strip():
        if i == version:
            trprint('Python %s has been installed. ' % (version))
            return
    ShellRun('pyenv install %s' % (version))

def setup():
    config = receive()
    global work_path
    global config_path
    global manage_path
    global oper_path
    global app
    global module
    global safe_command
    
    for i in safe_command: task_kill(i)
    for i in app: apt_install(i)
    for i in module: pip_install(i)

    #create
    if not os.path.exists(config['path']): os.makedirs(config['path'])
    os.chdir(config['path'])

    pyenv_install(version)
    os.system('git clone %s' % (config['git_URL']))
    os.chdir(os.path.join(config['path'], config['project']))

    ShellRun('pyenv local %s' % (version))
    ShellRun('pyenv virtualenv ENV_%s' % (config['project']))
    ShellRun('pyenv local ENV_%s' % (config['project']))
    pip_install('-r requirements.txt')
    
    #Nginx config
    nginx_config(config)
    
    #manage
    shutil.copy(manage_path, os.path.join(config['path'], config['project'], 'manage.py'))
    shutil.copy(oper_path, os.path.join(config['path'], config['project'], 'linux_oper.py'))
    shutil.copy(config_path, os.path.join(config['path'], config['project'], 'setup_config.dat'))
    
    #start
    if input('Starting the service now ? (y/n)').lower() in ('y', 'yes'):
        os.chdir(os.path.join(config['path'], config['project']))
        ShellRun('python3 %s start' % (os.path.join(config['path'], config['project'], 'manage.py')))

switch = {'install' : setup, 'build' : builder}
try:
    switch[sys.argv[1]]()
except KeyError:
    trprint('A command does not exists. ')
