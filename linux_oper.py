import os

def trprint(sp):
    os.system('echo ' + sp + '\n')
    return None

def info_trprint(sp):
    os.system('echo ' + sp.center(100, '*') + '\n')
    return None

def task_kill(name):
    k = os.popen('ps -aux').read().split('\n')[1:]

    for i in k:
        if i.split()[-1] in name:
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
        with open('/etc/rc.d/rc.local' , 'w+') as f:
            f.write(url + '\n')
    except:
        trprint("Error.")
    else:
        trprint("Added auto start task successfully.")
    finally:
        return None

def pip_install(app, cof = ''):
    os.system("".join([cof, 'pip3 install ', app]))
    return None

def apt_install(app):
    trprint('')
    info_trprint('installing ' + app.split()[0])
    trprint('')
    try:
        os.system('apt-get install ' + app)
    except:
        trprint('error !')
    else:
        trprint("Installed successfully.")
    return None

def port_unlocker(port):
    for j in [i.split()[1] for i in os.popen("".join(['lsof -i :', port])).read().split('\n')[1:-1]]:
        try:
            os.system("".join(['kill -9 ', j]))
        except:
            trprint('error !')
        else:
            trprint("".join(["Killed task : PID ", j]))
