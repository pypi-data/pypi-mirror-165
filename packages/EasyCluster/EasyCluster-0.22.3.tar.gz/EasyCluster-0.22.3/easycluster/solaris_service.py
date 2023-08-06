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
import signal
import subprocess
import traceback
import tempfile
import easycluster as _core

from easycluster import linux_service

if _core.PYTHON3:
    NAME = 'EasyCluster-Py3'
    SUFFIX = '-py3'
else:
    NAME = 'EasyCluster'
    SUFFIX = ''

KEY_PATH = '/etc/easycluster_service%s.key' % SUFFIX
SVC_NAME='network/easycluster%s' % SUFFIX

SERVICE_XML = '''\
<?xml version="1.0"?>
<!DOCTYPE service_bundle SYSTEM "/usr/share/lib/xml/dtd/service_bundle.dtd.1">
<service_bundle type='manifest' name='easycluster%(suffix)s'>
  <service name='network/easycluster%(suffix)s' type='service' version='1'>
    <create_default_instance enabled='false' />

    <single_instance />

    <dependency name='fs-local'
		grouping='require_all'
		restart_on='none'
		type='service'>
      <service_fmri
          value='svc:/system/filesystem/local' />
    </dependency>

    <dependency name='fs-autofs'
		grouping='optional_all'
		restart_on='none'
		type='service'>
      <service_fmri value='svc:/system/filesystem/autofs' />
    </dependency>

    <dependency name='net-loopback'
		grouping='require_all'
		restart_on='none'
		type='service'>
      <service_fmri value='svc:/network/loopback' />
    </dependency>

    <dependency name='net-physical'
		grouping='require_all'
		restart_on='none'
		type='service'>
      <service_fmri value='svc:/network/physical:default' />
    </dependency>

    <dependency name='utmp'
		grouping='require_all'
		restart_on='none'
		type='service'>
      <service_fmri value='svc:/system/utmp' />
    </dependency>

    <exec_method
        type='method'
        name='start'
        exec='%(exe)s -m %(mod)s start'
        timeout_seconds='60'/>

    <exec_method
        type='method'
        name='stop'
        exec='%(exe)s -m %(mod)s stop'
        timeout_seconds='60' />

    <exec_method
        type='method'
        name='refresh'
        exec='%(exe)s -m %(mod)s restart'
        timeout_seconds='60' />

    <property_group name='sysconfig' type='application'>
      <stability value='Unstable' />
      <propval name='group' type='astring' value='network' />
      <propval name='reconfigurable' type='boolean' value='true' />
    </property_group>

    <stability value='Evolving' />
    <template>
      <common_name>
        <loctext xml:lang='C'>
          EasyCluster%(suffix)s
        </loctext>
      </common_name>
    </template>
  </service>
</service_bundle>
'''

def check_call(prog):
    rc = subprocess.call(prog)
    if rc != 0:
        raise OSError('%s exited with code %d' % (prog[0], rc))

def install_service():
    xml = SERVICE_XML % dict(exe=sys.executable, mod=__name__, suffix=SUFFIX)
    if query_service_installed():
        return

    fd, temp_path = tempfile.mkstemp(suffix='.xml')
    os.write(fd, xml)
    os.close(fd)
    try:
        os.chmod(temp_path, 0o755)
        for prog in (['svccfg', 'validate', temp_path],
                     ['svccfg', 'import', temp_path]):
            check_call(prog)
    finally:
        try:
            os.unlink(temp_path)
        except EnvironmentError:
            pass

def uninstall_service():
    if query_service_installed():
        check_call(['svcadm', 'disable', '-s', SVC_NAME])
        check_call(['svccfg', 'delete', SVC_NAME])

def start_service():
    rc, txt = _service_status()
    if rc == 0:
        if txt.startswith('online'):
            return
        elif txt.startswith('maintenance'):
            check_call(['svcadm', 'clear', SVC_NAME])
        check_call(['svcadm', 'enable', '-s', SVC_NAME])
    else:
        raise OSError('EasyCluster service not installed')

def stop_service():
    if query_service_installed():
        check_call(['svcadm', 'disable', '-s', SVC_NAME])

def _service_status():
    proc = subprocess.Popen(['svcs', SVC_NAME], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    rc = proc.wait()
    return rc, out.splitlines()[-1]

def query_service_installed():
    rc, out = _service_status()
    return rc == 0

if __name__ == '__main__':
    sys.exit(linux_service.init_main())

