import os, shutil, sys
from linux_oper import *

SSR_giturl = 'https://github.com/shadowsocksr-backup/shadowsocksr.git'
BBR_url = 'https://raw.githubusercontent.com/ToyoDAdoubi/doubi/master/bbr.sh'
work_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
comper = ('git', 'python-pip', 'python3-pip', 'python-build',
          'gcc', 'nginx', 'sysv-rc-conf',
          'make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget', 
          'curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev')

def SSR_install(install_path = '/root'):
    global SSR_giturl
    global BBR_url
    if os.path.exists(os.path.join(work_path, 'ssr_config.json')):
        config_url = os.path.join(work_path, 'ssr_config.json')
        trprint('Config file had found.')
        
        if not os.path.exists(install_path): os.makedirs(install_path)
        os.chdir(install_path)

        ShellRun('git clone -b manyuser ' + SSR_giturl)
        os.chdir(os.path.join(install_path, 'shadowsocksr'))

        with open('update.sh', 'w') as f:
            f.write('cd ' + os.path.join(install_path, 'shadowsocksr') + '\n')
            f.write('git pull\n')        
        reg_setup('00 00 * * *', 'bash ' + os.path.abspath('update.sh'))
        
        ShellRun('bash %s' % (os.path.join(install_path, 'shadowsocksr', 'initcfg.sh')))
        shutil.move(config_url, os.path.join(install_path, 'shadowsocksr', 'user-config.json'))
        ShellRun('chmod +x *.sh')
    
        os.chdir(os.path.join(install_path, 'shadowsocksr', 'shadowsocks'))
        ShellRun('chmod +x *.sh')
        ShellRun('sysv-rc-conf ' + os.path.abspath('logrun.sh') + ' on', hint = 'Adding the auto-start task successfully. ')
        try:
            ShellRun('wget -N --no-check-certificate %s && chmod +x bbr.sh && bash bbr.sh' % (BBR_url))
        except:
            trprint('Installed the BBR Failed.')
        else:
            trprint('Installed the BBR Successfully.')
    else:
        trprint('Config file NOT found. ')

def pyenv_install():
    try:
        ShellRun('curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash')
    except:
        print('pyenv_install' + ' error')
    else:
        print('pyenv_install ' + 'success')

    with open('/root/.bash_profile', 'w') as f:
            f.write('export PYENV_ROOT="$HOME/.pyenv"\n')
            f.write('export PATH="$PYENV_ROOT/bin:$PATH"\n')
            f.write('eval "$(pyenv init -)"\n')

def SSH_config():
    try:
        with open('/etc/ssh/sshd_config', 'w+') as f:
            f.append('ClientAliveInterval 300\n')
            f.append('ClientAliveCountMax 10000\n')
    except IOError:
        trprint('ssh_config NOT found. ')
    else:
        trprint('Setting the ssh_config successfully. ')
        ShellRun('sevice ssh restart')

#init
trprint("Now the file is in %s" % (work_path))
ShellRun('apt-get update')
ShellRun('apt-get -y upgrade')
for app in comper: apt_install(app)

step = {
    'ssh_config' : SSH_config,
    'ssr_install' : SSR_install,
    'pyenv_install' : pyenv_install
    }

#install
for i in step.keys(): step[i]()
