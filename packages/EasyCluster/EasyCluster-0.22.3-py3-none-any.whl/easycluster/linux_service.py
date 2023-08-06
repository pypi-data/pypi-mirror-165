# Copyright (C) 2013 Katie Rust (katie@ktpanda.org)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import sys
import os
import signal
import subprocess
import traceback
import time
import easycluster as _core

if _core.PYTHON3:
    NAME = 'EasyCluster-Py3'
    SUFFIX = '-py3'
else:
    NAME = 'EasyCluster'
    SUFFIX = ''

MODULE = 'easycluster'
MAIN_MODULE = MODULE + '.__main__'

PIDFILE = '/var/run/easycluster%s.pid' % SUFFIX
KEY_PATH = '/etc/easycluster_service%s.key' % SUFFIX
INIT_PATH = '/etc/init.d/easycluster%s' % SUFFIX
SERVICE_NAME = 'easycluster%s' % SUFFIX

INIT_SCRIPT = '''\
#!/bin/sh
# chkconfig: 345 99 01
# description: EasyCluster remote service
# processname: easycluster%(suffix)s

### BEGIN INIT INFO
# Provides:          easycluster%(suffix)s
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Control the EasyCluster service.
### END INIT INFO

# Author: Katie Rust <katie@ktpanda.org>

PATH=/sbin:/usr/sbin:/bin:/usr/bin

exec '%(exe)s' -m %(name)s "$@"
'''

def install_service():
    temp_path = INIT_PATH + '~'

    with open(temp_path, 'w') as fp:
        fp.write(INIT_SCRIPT %  dict(exe=sys.executable, name=__name__, suffix=SUFFIX))

    os.chmod(temp_path, 0o755)
    os.rename(temp_path, INIT_PATH)

    for prog in (['update-rc.d', SERVICE_NAME, 'defaults'],
                 ['chkconfig', '--add', SERVICE_NAME],
                 ['/usr/lib/lsb/install_initd', SERVICE_NAME]):

        try:
            subprocess.call(prog)
        except OSError:
            pass
        else:
            break
    else:
        raise OSError("No method of installing initscripts found (tried Debian, Redhat, LSB)")

def uninstall_service():
    for prog in (['update-rc.d', '-f', SERVICE_NAME, 'remove'],
                 ['chkconfig', '--del', SERVICE_NAME],
                 ['/usr/lib/lsb/remove_initd', SERVICE_NAME]):
        try:
            subprocess.call(prog)
        except OSError:
            pass
        else:
            break
    else:
        raise OSError("No method of uninstalling initscripts found (tried Debian, Redhat, LSB)")

    try:
        os.unlink(INIT_PATH)
    except (IOError, OSError):
        pass

    return 0

def start_service():
    return start_daemon()

def stop_service():
    return stop_daemon()

def query_service_installed():
    return os.path.exists(INIT_PATH)

def is_daemon(pid, name):
    try:
        os.kill(pid, 0)
    except OSError:
        return False

    try:
        cmdf = '/proc/%d/cmdline' % pid
        if not os.path.exists(cmdf):
            ## Proc not mounted or not Linux - just assume pidfile is valid
            return True

        with open(cmdf, 'r') as fp:
            cmdline = fp.read().split('\0')
        if cmdline[1] == '-m' and cmdline[2] == name:
            return True
    except (EnvironmentError, ValueError):
        pass
    return False

def read_pidfile(fil):
    try:
        with open(fil, 'r') as fp:
            return int(fp.read().strip())
    except (EnvironmentError, ValueError):
        return 0

def getpid():
    pid = read_pidfile(PIDFILE)
    if not pid:
        return

    if not is_daemon(pid, MAIN_MODULE):
        try:
            os.unlink(PIDFILE)
        except Exception:
            pass
        return 0

    return pid

def start_daemon():
    opid = getpid()
    if opid:
        print("%s is already running." % NAME)
        return 1

    print("Starting %s: " % NAME, end='')
    exitstat = subprocess.call([sys.executable, '-m', MAIN_MODULE, '-S', '-k', KEY_PATH, '-d', '-P', PIDFILE])
    if exitstat:
        print('failed.')
        return 2
    print("ok.")
    return 0

def stop_daemon():
    pid = getpid()
    if not pid:
        print("%s is not running." % NAME)
        return 1
    try:
        print("Stopping %s: " % NAME, end='')

        os.kill(pid, signal.SIGTERM)
        try:
            os.unlink(PIDFILE)
        except Exception:
            pass
        print("success.")
        return 0
    except Exception:
        print("failed.")
        return 2


def init_main():
    exitstat = 0

    cmd = sys.argv[1]
    if cmd == "start":
        exitstat = start_daemon()

    elif cmd == "stop":
        exitstat = stop_daemon()

    elif cmd == "reload" or cmd == "force-reload":
        pid = getpid()
        if pid:
            os.kill(pid, signal.SIGHUP)
            exitstat = 1
        else:
            print("%s is not running." % NAME)

    elif cmd == "status":
        pid = getpid()
        if pid:
            print("%s is running." % NAME)
        else:
            exitstat = 1
            print("%s is not running." % NAME)

    elif cmd == "restart":
        stop_daemon()
        time.sleep(2)
        exitstat = start_daemon()
    else:

        print("Usage: %s {start|stop|restart|reload|force-reload}" % sys.argv[0], file=sys.stderr)
        exitstat = 1
    return exitstat

if __name__ == '__main__':
    sys.exit(init_main())
