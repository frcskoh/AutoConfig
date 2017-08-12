import os

def trprint(sp):
    os.system('echo ' + sp + '\n')
    return None

def info_trprint(sp):
    os.system('echo ' + sp.center(100, '*') + '\n')
    return None

def task_kill(name):
    k = os.popen('ps -aux').read().split('\n')

    for i in k:
        if i.split()[:-1] in name:
            os.system('kill -9 ' + i.split()[1])
            trprint("Found and kill the task.")
    return None

def reg_setup(cof, command):
    try:
        f = open('/etc/crontab' ,'w+')
        f.writeline(cof + ' ' + command)
        f.close()
    except:
        trprint("Error.")
    else:
        trprint("Added regual task successfully.")
    finally:
        return None

def auto_start_setup(url):
    try:
        f = open('/etc/rc.local' , 'w+')
        f.writeline(url)
        f.close()
    except:
        trprint("Error.")
    else:
        trprint("Added auto start task successfully.")
    finally:
        return None

def pip_install(name, cof = ''):
    for app in name:
        os.system(cof + 'pip3 install ' + app)
    return None

def apt_install(name):
    os.system('apt-get update -y')
    os.system('apt-get upgrade -y')
    for app in name:
        trprint('')
        info_trprint('installing ' + app.split()[0])
        trprint('')
        os.system('apt-get install ' + app)
    return None
