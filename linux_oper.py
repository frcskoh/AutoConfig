import os

def trprint(content):
    os.system('echo ' + content + '\n')
    
def ShellRun(command, hint = None, output = False):
    trprint(command)
    try:
        if output:
            output_text = os.popen(command)
            if hint: trprint(hint)
            return(output_text)
        else:
            os.system(command)
            if hint: trprint(hint)
            return(output_text)
    except:
        trprint('Error. Try to excute "%s" but failed. ', command)

def get_ip():
    from requests import get as Get
    try:
        return Get('http://checkip.dyndns.org/').text.split(':')[1].strip().split('<')[0]
    except:
        trprint('Network error. ')

def task_kill(name):
    k = os.popen('ps -aux').read().split('\n')[1:]

    for i in k:
        try:
            if i.split()[10] == name:
                os.system('kill -9 ' + i.split()[1])
                trprint("Found and kill the %s." & (i.split()[10]))
        except OSError:
            trprint("System Error.")
            
    trprint("Task %s has been kill. " % (name))
    
def reg_setup(cof, command):
    try:
        with open('/etc/crontab', 'a+') as f:
            f.write("%s %s \n" % (cof, command))
    except IOError:
        trprint("reg_setup Error.")
    else:
        trprint("Added %s successfully." % (command))

def pip_install(app_name, cof = ''):
    ShellRun("%spip3 install %s" % (cof, app_name))

def apt_install(app):
    try:
        trprint('Installing ' + app.split()[0])
        ShellRun('apt-get install -y ' + app)
    except OSError:
        trprint('apt installation Error !')
    else:
        trprint("Installed %s successfully." % (app.split()[0]))

def port_unlocker(port):
    for j in [i.split()[1] for i in os.popen("".join(['lsof -i :', port])).read().split('\n')[1:-1]]:
        try:
            ShellRun("kill -9 %s" % (j))
        except OSError:
            trprint('port_unlocker Error !')
        else:
            trprint("Killed task : PID %s" % (j))
