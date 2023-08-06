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

import sys
import os
import traceback
import win32serviceutil
import win32service
import pywintypes
import easycluster as _core

sysroot = os.environ.get('SYSTEMROOT', r'c:\windows')
sysdir = os.path.join(sysroot, 'sysnative')
if not os.path.isdir(sysdir):
    sysdir = os.path.join(sysroot, 'system32')
KEY_PATH = os.path.join(sysdir, 'easycluster_service.key')
del sysdir, sysroot

class EasyClusterService(win32serviceutil.ServiceFramework):
    if _core.PYTHON3:
        _svc_name_ = 'EasyCluster-Py3'
        _svc_display_name_ = 'EasyCluster remote execution service (Python 3)'
    else:
        _svc_name_ = 'EasyCluster'
        _svc_display_name_ = 'EasyCluster remote execution service'

    server = None

    def SvcDoRun(self):
        '''Start and run the service.'''
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            import easycluster.server
            import servicemanager
            servicemanager.LogInfoMsg('%s - Starting (%r)' % (self._svc_name_, sys.executable))
            easycluster.server.server_main(['-S', '-k', KEY_PATH])
        except Exception:
            import servicemanager
            servicemanager.LogErrorMsg(traceback.format_exc())

    def SvcStop(self):
        '''Stop the service.'''

        import easycluster.server
        import servicemanager
        servicemanager.LogInfoMsg('%s - Shutting down' % self._svc_name_)
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        easycluster.server.stop_server()

def _service_action(*args):
    return win32serviceutil.HandleCommandLine(EasyClusterService, argv=[''] + list(args))

def install_service():
    return _service_action('--startup', 'auto', 'install')

def uninstall_service():
    return _service_action('remove')

def start_service():
    return _service_action('start')

def stop_service():
    return _service_action('stop')

def query_service_installed():
    hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    try:
        try:
            hs = win32serviceutil.SmartOpenService(hscm, EasyClusterService._svc_name_, win32service.SERVICE_ALL_ACCESS)
            win32service.CloseServiceHandle(hs)
            return True
        except pywintypes.error:
            return False
    finally:
        win32service.CloseServiceHandle(hscm)

daemonize = None

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(EasyClusterService)
