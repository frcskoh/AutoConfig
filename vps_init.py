import os, shutil, sys
from linux_oper import *

SSR_giturl = 'https://github.com/shadowsocksr-backup/shadowsocksr.git'
linux_oper_url = 'https://github.com/frcskoh/python_hosting.git'
script_url = os.path.split(os.path.abspath(sys.argv[0]))[0]

def ssr_install():
    #check
    inst_path = '/root'
    
    if os.path.exists(os.path.join(script_url, 'ssr_config.json')):
        config_url = os.path.join(script_url, 'ssr_config.json')
        trprint('Config  file found.')
    else:
        trprint('Config file does not exist.')
        return None

    if not os.path.exists(inst_path):
        os.mkdir(inst_path)
    os.chdir(inst_path)

    os.system('git clone -b manyuser ' + SSR_giturl)
    os.chdir('shadowsocksr')

    with open('update.sh', 'w') as f:
        f.write('cd ' + inst_path + '\n ')
        f.write('git pull\n')
        
    reg_setup('00 00 * * *', 'bash ' + os.path.abspath('update.sh'))
    os.system('bash initcfg.sh')

    shutil.move(config_url, os.path.join(inst_path, 'shadowsocksr', 'user-config.json'))
    os.system('chmod +x *.sh')
    
    os.chdir('shadowsocks')
    os.system('chmod +x *.sh')
    try:
        os.system('sysv-rc-conf' + os.path.abspath('shadowsocks/logrun.sh') + 'on')
    except:
        print('ssr_install error')
    else:
        trprint('ssr_install Successful.')

    try:
        os.system('wget -N --no-check-certificate https://raw.githubusercontent.com/ToyoDAdoubi/doubi/master/bbr.sh && chmod +x bbr.sh && bash bbr.sh')
    except:
        pass
    else:
        return trprint('Successful.')
    
    return None

def pyenv_install():
    try:
        os.system('curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash')
        os.system("echo 'export PYENV_ROOT=\"$HOME/.pyenv\"' >> ~/.bashrc")
        os.system("echo 'export PATH=\"$PYENV_ROOT/bin:$PATH\"' >> ~/.bashrc")
        os.system("echo 'eval \"$(pyenv init -)\"' >> ~/.bashrc")
        os.system("source ~/.bashrc")
    except:
        print('pyenv_install' + 'error')
    else:
        print('pyenv_install' + 'success')
    os.system("pyenv install 3.6.2")

def ssh_config():
    try:
        with open('/etc/ssh/sshd_config', 'w'):
            f.write('ClientAliveInterval 30\n')
            f.write('ClientAliveCountMax 10000\n')
    except:
        print('ssh_config error')
    else:
        print('ssh_config Successful')
    return None
#init
#task_kill('apt-get')
trprint(script_url)
os.system('apt-get update')
os.system('apt-get -y upgrade')

comper = ('git -y', 'python-pip -y', 'python3-pip -y', 'python-build -y',
          'gcc -y', 'nginx -y', 'sysv-rc-conf -y')
for app in comper: apt_install(app)

pip_install('zlib')
#install
#ssh_config
pyenv_install()
ssr_install()
