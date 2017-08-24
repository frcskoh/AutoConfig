import os, json, sys, shutil
from linux_oper import *
work_path = os.path.split(os.path.abspath(sys.argv[0]))[0]

def builder():
    global work_path
    config = {}
    config.update({'path' : input('Enter the root path : ')})
    config.update({'project' : input('Enter the name of the project : ')})
    config.update({'git_URL' : input('Enter the URL of the git : ')})
    config.update({'main_file' : input('Enter the name of the main file : ')})
    config.update({'main_route' : input('Enter the name of the main route : ')})
    config.update({'ip' : input('Enter the ip address of the service : ')})
    config.update({'host' : input('Enter the address of the localhost : ')})
    config.update({'local_port' : input('Enter the local port : ')})
    config.update({'public_port' : input('Enter the public port : ')})
    
    try:
        info_trprint('Creating the config file.')
        global config_path
        config_path = os.path.join(work_path, 'setup_config.dat')
        with open(config_path, 'w') as f:
            json.dump(config, f)
        f.close()
    except:
        trprint('error ! Please retry. ')
    else:
        if input('Starting the setup now ? (y/n)').lower() in ('y', 'yes'): setup(config)
    
    return None

def uwsgi_config(path, project, main_file, main_route, local_port, processes = '1', threads = '4'):
    os.chdir(os.path.join(path, project))

    try:
        with open('config.ini', 'w') as f:
            f.write('[uwsgi]\n')
            f.write('master = true\n')
            f.write('home = ENV\n')
            f.write('wsgi-file = ' + main_file + '\n')
            f.write('callable = ' + main_route + '\n')
            f.write('socket = :' + local_port + '\n')
            f.write('processes = ' + processes + '\n')
            f.write('threads = ' + threads + '\n')
            f.write('buffer-size = 32768\n')
    except:
        print('error')
    return None
    
def nginx_config(project, ip, public_port, path, localhost, local_port, main_file, main_route):
    work_path = os.path.join(path, project)
    tab = 4
    try:
        with open(os.path.join('/etc/nginx/sites-enabled/', 'default'), 'w+') as f:
            f.write('server {\n')
            f.write(''.center(tab));f.write('listen ' + public_port + ';\n')
            f.write(''.center(tab));f.write('server_name ' + ip + ';\n')
            f.write(''.center(tab));f.write('location / {\n')
            f.write(''.center(tab * 2));f.write('include ' + 'uwsgi_params;\n')
            f.write(''.center(tab * 2));f.write('uwsgi_pass ' + localhost + ':' + local_port + ';\n')
            f.write(''.center(tab * 2));f.write('uwsgi_param UWSGI_PYHOME ' + work_path + '/ENV;\n')
            f.write(''.center(tab * 2));f.write('uwsgi_param UWSGI_CHDIR ' + work_path + ';\n')
            f.write(''.center(tab * 2));f.write('uwsgi_param UWSGI_SCRIPT ' + main_file + ':' + main_route + ';\n')
            f.write(''.center(tab));f.write('}\n')
            f.write('}\n')
    except:
        print('error !')
    else:
        info_trprint('Config the nginx successfully.')
        if not os.path.exists(os.path.join('/etc/nginx/sites-available/default')):
            os.symlink(os.path.join('/etc/nginx/sites-enabled/default'),
                       os.path.join('/etc/nginx/sites-available/default'))
    return

def uWSGI_install():
    global work_path
    os.chidr(os.path.join('usr', 'lib'))
    try:
        os.system('git clone https://github.com/unbit/uwsgi.git')
        os.chidr('uwsgi')
        with open('buildconf/core.ini', 'rw') as f:
            data = f.read().split('\n')
            for i in data:
                if i.find('plugin_dir'):
                    i = i.split('=')[0] + '= /usr/lib/uwsgi'
                if i.find('bin_name'):
                    i = i.split('=')[0] + '= /usr/bin/uwsgi'
            for i in data:
                f.write(i + '\n')
    except:
        trprint('Write Error')
    else:
        os.system('python uwsgiconfig.py --build core')
        os.system('python3.6 uwsgiconfig.py --plugin plugins/python core python36')
                    
def setup(config):
    safe_command = ('apt-get', 'pip', 'git')
    
    #init
    for i in ('build-essential -y', 'python3-dev -y', 'nginx -y', 'git -y'):
        apt_install(i)
    for i in ('virtualenv', ):
        pip_install(i)
    
    #create
    os.chdir(config['path'])
    os.system('git clone ' + config['git_URL'])

    os.chdir(os.path.join(config['path'], config['project']))
    print(os.getcwd())
    os.system('pyenv virtualenv 3.6.2 ENV')

    #install
    os.chdir(os.path.join(config['path'], config['project']))
    pip_install('-r requirements.txt', 'ENV/bin/')
    pip_install('uwsgi')
    uwsgi_config(config['path'], config['project'], config['main_file'], config['main_route'], config['local_port'])

    #Nginx config
    nginx_config(config['project'], config['ip'], config['public_port'], config['path'], config['host'], config['local_port'], config['main_file'], config['main_route'])

    shutil.copy(config_path, os.path.join(config['path'], config['project'], 'setup_config.dat'))
    if input('Starting the service now ? (y/n)').lower() in ('y', 'yes'):
        import manage
        manage.start()

def reader():
    global work_path
    if os.path.exists(os.path.join(work_path, 'setup_config.dat')):
        global config_path
        config_path = os.path.join(work_path, 'setup_config.dat')
        with open(config_path, 'r') as f:
            config = json.load(f)

        apt_install('python3-pip -y')
        setup(config)
    else:
        trprint('Config file does not exists.')    

switch = {'install' : reader, 'build' : builder}
switch[sys.argv[1]]()
