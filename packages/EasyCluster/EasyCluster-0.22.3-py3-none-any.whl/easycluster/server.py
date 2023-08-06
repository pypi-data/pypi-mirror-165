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

"""Server class and functions for EasyCluster"""
from __future__ import print_function

import sys

MIN_CLIENT_VERSION = '0.16'

# A little bit of magic to allow running python -m easycluster.server. This
# allows the user to use '-m' with Python 2.6, which fails when '-m' is used on
# a package.
_is_main = __name__ == '__main__'
if _is_main:
    __name__ = 'easycluster.server'
    sys.modules[__name__] = sys.modules['__main__']

import os
import traceback
import time
import socket
import errno
import threading
import select
import cProfile
import easycluster as _core
from weakref import WeakKeyDictionary
from collections import deque
from types import ModuleType, BuiltinMethodType, MethodType, FunctionType


## Stolen from multiprocessing. We can't just use multiprocessing -- it has way
## too many weird bugs on Windows.

WINSERVICE = sys.executable.lower().endswith("pythonservice.exe")

if WINSERVICE:
    _python_exe = os.path.join(sys.exec_prefix, 'python.exe')
else:
    _python_exe = sys.executable

__all__ = ['Server', 'QuietServer', 'run_server', 'spawn_local']
__metaclass__ = type

try:
    from socket import socketpair
except ImportError:
    def socketpair():
        '''Emulate socketpair() using a locally-bound TCP socket'''
        socka = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socka.setblocking(0)

        svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr.bind(('127.0.0.1', 0))

        svr.listen(1)
        try:
            socka.connect(svr.getsockname())
        except socket.error as e:
            if e.errno not in _core._nonblocking_errors:
                raise

        socka.setblocking(1)
        while True:
            sockb, addr = svr.accept()

            ## There is a short window in which another local application may
            ## connect to the listening socket we just opened. If the address
            ## returned by accept() does not match our socket, close it and try
            ## again.
            if addr == socka.getsockname():
                svr.close()
                return socka, sockb
            sockb.close()

_method_types = BuiltinMethodType, MethodType, FunctionType, type(_core.set_global.__call__)

class RootObject(object):
    '''Utility class instantiated automatically on the server as OID 0.'''
    def __init__(self):
        self._defmod = None

    def eval(self, code, mode):
        cb = compile(code, '<remote code>', mode, dont_inherit=True)
        try:
            return eval(cb, self._defmod.__dict__)
        except _core._ExecReturn as e:
            return e.val

    def get_global(self, name):
        return _core.get_global(name, self._defmod, True)

    def set_global(self, name, value):
        return _core.set_global(name, value, self._defmod)

    def update_definitions(self, code):
        for c in code:
            self._defmod.define(c)

    def call(self, func, args, kwargs={}):
        f = _core.get_global(func, self._defmod, True)
        return f(*args, **kwargs)

    def getattr(self, obj, attr):
        return getattr(obj, attr)

    def getmethod(self, obj, attr):
        val = getattr(obj, attr)
        if isinstance(val, _method_types):
            return True, None
        return False, val

    def setattr(self, obj, attr, val):
        return setattr(obj, attr, val)

    def delattr(self, obj, attr):
        return delattr(obj, attr)

    def import_modules(self, names):
        for n in names:
            setattr(self._defmod, n, __import__(n))

    def do_easycluster_upgrade(self, code, data):
        cb = compile(code, 'upgrade', 'exec')
        eval(cb, data)
        new = data['upgrade'](self._defmod.running_server, self._defmod)
        raise _Replace(new)

def profile_request(func, args):
    '''Profile a function call and write the results to the user's
    home directory. Used only for debugging.'''
    import cProfile, pstats
    ctime = time.time()
    itime = int(ctime)
    frac = ctime - itime
    strtime = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(itime)) + '.%08d' % int(frac * 10000000)
    fn = 'profile_%s.txt' % strtime
    prof = cProfile.Profile()
    prof.runcall(func, *args)

    with open(os.path.join(os.getenv('HOME'), fn), 'w') as fp:
        fp.write('Profile of %r:\n' % (args,))
        pstats.Stats(prof, stream=fp).sort_stats('time').print_stats()

class ServerThread(threading.Thread):
    '''A thread that runs code on behalf of the client.'''
    def __init__(self, svr, tid, profile=None):
        threading.Thread.__init__(self)
        self.tid = tid
        self.lock = threading.Lock()
        self.queue = _core.queue.Queue()
        self.svr = svr
        self.profile = profile
        self.daemon = True

    def run(self):
        if self.profile:
            cProfile.runctx('f()', {'f': self.real_run}, {}, self.profile)
        else:
            return self.real_run()

    def real_run(self):
        '''Runs the server request thread.'''
        queue = self.queue
        svr = self.svr
        self.svr = None

        while True:
            rid, obj, meth, args, kw = queue.get()
            if obj is None:
                return
            #profile_request(svr.run_request, (rid, obj, meth, args, kw))
            svr.run_request(rid, obj, meth, args, kw)

class _Replace(BaseException):
    def __init__(self, new):
        self.new = new

class Server(_core.Connection):
    '''Represents the server side of a remote connection.'''

    _sendiv = b'SRVR'
    _recviv = b'CLNT'

    def __init__(self, key, sock, peername, verbosity=0, profile=None, repl=None):
        _core.Connection.__init__(self, key, True)
        self._next_object_id = 1
        self._next_type_id = 1

        # Local object that our peer has proxies for
        root = RootObject()
        self._root = root
        self._local_object_by_id = {0: root}
        self._local_id_by_object = {id(root): 0}
        self._local_id_by_typedat = {}

        self._pending_responses = deque()
        self._keep_alive_interval = None

        self._threads = {}
        self._verbosity = verbosity
        self._sent_challenge = False
        self._profile = profile
        if repl:
            self._sent_challenge = True

        self.set_socket(sock, peername)
        if repl:
            self._verified = True
            self._recv_hmac = repl._recv_hmac
            self._send_hmac = repl._send_hmac
            self._remote_host = repl._remote_host
            self._remote_port = repl._remote_port
            self._got_init(repl._peer_init_data)

    def report_connection(self):
        '''Report that a connection was received.'''
        if self._verbosity >= 1:
            print('New connection from %s' % (self._peername))

    def report_disconnection(self):
        '''Report that a client disconnected.'''
        if self._verbosity >= 1:
            print('Connection to %s terminated' % (self._peername))

    def report_request(self, rid, garbage, tid, oid, meth, args, kw):
        '''Report a request from the client.'''
        if self._verbosity >= 2 and rid is not None:
            print('<%s> Request %d: <%s> %d.%s g=%s' % (self._peername, rid, tid, oid, meth, garbage))

    def _after_connect(self):
        self._sock.setblocking(1)
        self.send_challenge()

    def _check_version(self, pv):
        if _core._version_compare(pv, MIN_CLIENT_VERSION) < 0:
            raise ValueError('Incompatible EasyCluster version: client has version %s, server has version %s; '
                             'server requires client to have at least version %s' % (pv, VERSION, MIN_CLIENT_VERSION))

    def send_challenge(self):
        if not self._sent_challenge:
            if self._key is not None:
                self.send_message(_core.CHALLENGE, self._my_nonce, True)
            else:
                self.send_message(_core.INIT, self.make_pickle(self._init_data))

            self._sent_challenge = True

    def run_request(self, rid, oid, meth, args, kw):
        '''Processes a single request.'''
        try:
            obj = self._local_object_by_id[oid]
            rval = getattr(obj, meth)(*args, **kw)
            with self._lock:
                rpickle = self.make_pickle((rid, rval))
        except _Replace:
            rpickle = self.make_pickle((rid, None))
            self.send_message(_core.RESPONSE, rpickle)
            raise
        except Exception:
            typ, val, tb = sys.exc_info()
            text = traceback.format_exception(typ, val, tb)
            rval = _core.RemoteException(val, text)
            with self._lock:
                rpickle = self.make_pickle((rid, rval))
        self.send_message(_core.RESPONSE, rpickle)

    def _got_request(self, p):
        rid, garbage, tid, oid, meth, args, kw = p
        if garbage:
            with self._lock:
                for deloid in garbage:
                    obj = self._local_object_by_id.get(deloid)
                    if obj is not None:
                        del self._local_object_by_id[deloid]
                        del self._local_id_by_object[id(obj)]

        self.report_request(rid, garbage, tid, oid, meth, args, kw)
        if tid == _core.SINGLE:
            t = threading.Thread(target=self.run_request, args=(rid, oid, meth, args, kw))
            t.start()
            return True

        t = self._threads.get(tid)
        if oid is None:
            ## request to end thread
            if t is not None:
                del self._threads[tid]
        elif t is None:
            if tid is None:
                self.run_request(rid, oid, meth, args, kw)
            else:
                pf = (self._profile % tid if self._profile else None)
                self._threads[tid] = t = ServerThread(self, tid, pf)
                t.start()

        if t is not None:
            t.queue.put((rid, oid, meth, args, kw))
        return True


    def _got_init(self, args):
        super(Server, self)._got_init(args)
        self._root._defmod = _core.definitions_module(args['definitions_module'], False)
        self._keep_alive_interval = args.get('keep_alive_interval')
        if self._keep_alive_interval:
            self._sock.setblocking(0)

        self._root._defmod.running_server = self
        return True

    def run(self):
        '''Runs the main server thread.'''
        self.report_connection()
        next_keep_alive = 0
        try:
            while True:
                if self._keep_alive_interval:
                    ctime = time.time()
                    rtime = next_keep_alive - ctime
                    if rtime <= 0:
                        next_keep_alive = ctime + self._keep_alive_interval
                        self.send_message(_core.KEEPALIVE, b'')
                        continue
                    r, w, e = select.select([self._sock], (), (), rtime)
                    if self._sock in r:
                        self._read_data(False)
                else:
                    self._read_data(True)
        except socket.error as e:
            if e.errno != errno.ECONNRESET:
                raise
        except EOFError:
            pass
        except _Replace as r:
            return r.new

        self.report_disconnection()

        threads = self._threads.values()
        for t in threads:
            t.queue.put((None, None, None, None, None))
        for t in threads:
            t.join()

    def _persistent_load(self, id):
        '''Implements Unpickler.persistent_load.'''
        return self._local_object_by_id.get(int(id))

    def _persistent_id(self, obj):
        '''Implements Unpickler.persistent_id.'''
        oid = self._local_id_by_object.get(id(obj))
        if oid is not None:
            return str(oid)

        ## Find out if the object is a server object or not
        typ = obj.__class__
        typedat = _core._get_typedat(obj, typ)
        if typedat is None:
            return None

        tid = self._local_id_by_typedat.get(typedat)
        oid = self._next_object_id
        self._next_object_id = oid + 1
        self._local_id_by_object[id(obj)] = oid
        self._local_object_by_id[oid] = obj

        if tid is not None:
            return '%d\n%d' % (oid, tid)

        tid = self._next_type_id
        self._next_type_id = tid + 1
        self._local_id_by_typedat[typedat] = tid
        return '%d\n%d\n%s' % (oid, tid, typedat)

## For compatibility
QuietServer = Server

class IPAddress(object):
    '''Represents an IP address with optional network mask length'''
    def __init__(self, txt):
        maskbits = None
        lst = txt.split('/', 1)
        addr = lst[0]
        if len(lst) == 2:
            maskbits = int(lst[1])

        if ':' in addr:
            components = addr.split(':')

            if '.' in components[-1]:
                v4part = IPAddress(components.pop()).aslong
                components.append('%04x' % (v4part >> 16))
                components.append('%04x' % (v4part & 0xFFFF))

            if not 2 <= len(components) <= 8:
                raise ValueError('Invalid IPv6 address %r' % addr)

            val = 0
            curword = 0
            for i, part in enumerate(components):
                if part == '':
                    if i == 0:
                        curword += 1
                    else:
                        curword += 9 - len(components)
                else:
                    cval = int(part, 16)
                    if not 0 <= cval <= 65535:
                        raise ValueError('Invalid component %r in IPv6 address %r' % (part, addr))
                    val |= cval << (16 * (7 - curword))
                    curword += 1

            if val & ~0xFFFFFFFF == 0xFFFF00000000:
                val &= 0xFFFFFFFF
                self.family = socket.AF_INET
                numbits = 32
            else:
                self.family = socket.AF_INET6
                numbits = 128
            self.aslong = val
        else:
            components = addr.split('.')
            if len(components) != 4:
                raise ValueError('Invalid IPv4 address: %r' % addr)

            self.family = socket.AF_INET
            shift = 24
            val = 0
            for part in components:
                cval = int(part)
                if not 0 <= cval <= 255:
                    raise ValueError('Invalid component %r in IPv4 address %r' % (part, addr))
                val |= cval << shift
                shift -= 8
            self.aslong = sum(int(v) << (24 - i * 8) for i, v in enumerate(components))
            numbits = 32

        if maskbits is None:
            maskbits = numbits
        elif not 0 <= maskbits <= numbits:
            raise ValueError('Invalid value for mask length %r in address %r: '
                             'must be between 0 and %d' % (maskbits, txt, numbits))
        self.maskbits = maskbits
        self.mask = (1 << numbits) - (1 << (numbits - maskbits))
        self.aslong &= self.mask

    def in_network(self, net):
        return (self.family == net.family and
                (self.aslong & net.mask) == net.aslong)

def spawn_local(clientclass=_core.Client, **kw):
    '''Create a private server instance and connect to it.'''
    global _local_id
    csock, ssock = socketpair()
    _core._mark_non_inheritable(csock.fileno())

    spawn_runner_process(ssock, 'local:%d' % _local_id, b'', kw, (csock,))
    ssock.close()

    rc = clientclass(b'')
    rc.set_socket(csock, 'local:%d' % _local_id)
    _local_id += 1
    return rc

def server_main(args=None):
    '''Run by the easycluster script.'''
    server_check_runner()

    if sys.platform.startswith('win'):
        from easycluster import windows_service as servmod
    elif sys.platform.startswith('linux'):
        from easycluster import linux_service as servmod
    elif sys.platform.startswith('sun'):
        from easycluster import solaris_service as servmod
    else:
        servmod = None

    from optparse import OptionParser, SUPPRESS_HELP
    if args is None:
        args = sys.argv[1:]

    key = ''
    options = OptionParser(description="Runs the EasyCluster service and generates keyfiles", version=_core.VERSION)
    _core.add_key_options(options)
    options.add_option('-v', '--verbose', default=0, action='count', help='Increase the verbosity of the server.')
    options.add_option('-S', '--serve', metavar='FILE', action='store_true', help='Run the server on the specified port')
    options.add_option('-g', '--generate', metavar='FILE', help='Generate random HMAC key and '
                       'write it to FILE. The file will be created with read access only for the owner.')
    options.add_option('-O', '--overwrite', action='store_true', help='Allow --generate to overwrite existing keyfile')
    options.add_option('-p', '--port', type='int', default=_core.DEFAULT_PORT, help='TCP port to listen on. Default: %d' % _core.DEFAULT_PORT)
    options.add_option('-b', '--bind', default=None, help='Bind the server to a specific IP address')
    options.add_option('-N', '--no-ipv6', action='store_true', help='Disable IPv6 support')
    options.add_option('--profile', action='store', help='Enable server profiling')
    options.add_option('-a', '--allow', action='append', default=[], help='Allow only a specific address or subnet to connect '
                       '(e.g. 192.168.0.0/24). Specify more than once to allow multiple addresses.')

    ## Deprecated. Generally used only to specify QuietServer - quiet operation is now the default.
    options.add_option('-c', '--class', dest='svrclass', default=None, help=SUPPRESS_HELP)

    if _daemonize:
        options.add_option('-d', '--daemonize', action='store_true',
                           help='Detach from current terminal and run in the background')
        options.add_option("-P", "--pidfile", action="store",
                           dest="pidfile", metavar="FILE",
                           help="write daemon process ID to a file")

    if servmod:
        options.add_option('-i', '--install', action='store_true',
                           help='Install EasyCluster as a service. The keyfile '
                           'for this service is located at %s. If a keyfile is '
                           'specified, it will be copied there; if no key exists '
                           'currently, or if -O is given, a new key file will be '
                           'written.' % servmod.KEY_PATH)
        options.add_option('-u', '--uninstall', action='store_true',
                           help='Uninstall the service.')
        options.add_option('--start', action='store_true', help='Start the service.')
        options.add_option('--stop', action='store_true', help='Stop the service, but don\'t uninstall it.')
        options.add_option('--query-installed', action='store_true',
                           help='Exits with code 0 if the service is installed, '
                           'or code 1 if it is not.')

    opts, args = options.parse_args(args)

    if servmod:
        if opts.query_installed:
            if servmod.query_service_installed():
                return 0
            else:
                return 1

        try:
            if opts.install:
                key = _core.key_from_options(opts, False)
                if key:
                    _core.write_key_file(servmod.KEY_PATH, key, True)
                else:
                    _core.write_key_file(servmod.KEY_PATH, _core.generate_key(), opts.overwrite)

                servmod.install_service()
                if opts.start:
                    servmod.start_service()
                return 0

            if opts.uninstall:
                servmod.stop_service()
                servmod.uninstall_service()
                return 0

            if opts.start:
                servmod.start_service()
                return 0

            if opts.stop:
                servmod.stop_service()
                return 0
        except EnvironmentError as e:
            print(str(e), file=sys.stderr)
            return 1

    if opts.generate:
        if not _core.write_key_file(opts.generate, _core.generate_key(), opts.overwrite):
            print('Key file already exists (use --overwrite to overwrite it)', file=sys.stderr)
        return

    elif opts.serve:
        key = _core.key_from_options(opts)
        if key == b'':
            print('SECURITY WARNING: running with blank key.', file=sys.stderr)

        run_server(opts.port, key, opts.bind, opts.allow, opts.verbose,
                   getattr(opts, 'daemonize', False),
                   getattr(opts, 'pidfile', None),
                   opts.no_ipv6, opts.profile)
    else:
        options.print_help()

def create_socket(family, bindaddr, port):

    sockaddr = ('', port)
    if bindaddr is not None:
        gai_family = 0 if family == socket.AF_INET6 else family
        addrs = socket.getaddrinfo(bindaddr, port, gai_family)
        family, socktype, proto, canonname, sockaddr = addrs[0]

    try:
        sock = socket.socket(family, socket.SOCK_STREAM)
        if family == socket.AF_INET6 and socket.has_ipv6:
            # Windows needs this socket option set to listen on both IPV4 and
            # IPV6. However, IPPROTO_IPV6 is missing from the socket module on Windows.
            # Since the value is likely to never change, just include it here.
            IPPROTO_IPV6 = 41
            sock.setsockopt(IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        _core._mark_non_inheritable(sock.fileno())

        sock.bind(sockaddr)
        return sock

    except socket.error as e:
        print(family, sockaddr)
        # Fall back to IPv4
        if family == socket.AF_INET6 and e.args[0] in (97, 10047):
            return create_socket(socket.AF_INET, bindaddr, port)
        raise

def run_server(port, key, bindaddr=None, allow=(),
               verbosity=0, daemonize=False, pidfile=None, disable_ipv6=False, profile=None):
    '''Runs a server on the specified port.

    @type  port: int
    @param port: The TCP port to listen on.

    @type  key: bytes
    @param key: Binary HMAC key to use.

    @type  bindaddr: str
    @param bindaddr: Interface address to bind on, or None to bind on all
    interfaces.

    @type  allow: sequence
    @param allow: Sequence of IP networks to allow connections from, or empty
    list to allow connections from all IP addresses.

    @type  verbosity: int
    @param verbosity: Level of reporting: 0 = no reporting, 1 = report
    connections, 2 = report connections and requests.

    @type  daemonize: bool
    @param daemonize: If True, on POSIX systems, become a daemon after starting
    server. Not supported on Windows

    @type  pidfile: str
    @param pidfile: Path to file to write process ID to when daemonizing.

    @type  profile: str
    @param profile: If not None, specifies a filename pattern to write server thread profiles
    '''
    global _server_socket

    allow = [IPAddress(v) for v in allow]

    server_init()

    if socket.has_ipv6 and not disable_ipv6:
        family = socket.AF_INET6
    else:
        family = socket.AF_INET

    sock = create_socket(family, bindaddr, port)

    sock.listen(1)

    _server_socket = sock

    print('Listening on port %d' % port)

    if daemonize:
        _daemonize(pidfile)

    while _server_socket:
        try:
            r, w, e = select.select([sock], (), (), 2)
        except (EnvironmentError, select.error) as e:
            if e.args[0] not in _core._nonblocking_errors:
                raise

        if not r:
            continue
        try:
            csock, addr = sock.accept()
        except EnvironmentError as e:
            if e.args[0] in _core._nonblocking_errors:
                continue
            else:
                raise
        try:
            if allow:
                ipaddr = IPAddress(addr[0])
                for net in allow:
                    if ipaddr.in_network(net):
                        break
                else:
                    print('Connection from %s not allowed' % addr[0])
                    continue

            spawn_runner_process(csock, _core._get_peer_name(addr), key,
                                 dict(verbosity=verbosity, profile=profile), (sock,))
        except Exception:
            traceback.print_exc()
        finally:
            csock.close()


def stop_server():
    global _server_socket
    if _server_socket:
        _server_socket.close()
        _server_socket = None

_local_id = 0

if sys.platform.startswith('win'):
    from ctypes import (windll, Structure, Union, c_size_t, c_int,
                        py_object, POINTER, pythonapi, create_string_buffer, WinError)

    import subprocess

    # Windows does not support "inheriting" sockets; the only way to
    # pass an open socket to another process is to use the
    # WSADuplicateSocket function, send the WSAPROTOCOL_INFO over a
    # pipe, then call WSASocket in the receiving process.
    #
    # Python 3.3 implements this as share() and fromshare().
    if hasattr(socket, 'fromshare'):
        def dupsock(sock, pid):
            return sock.share(pid)

        def make_socket(af, stype, proto, protoinfo):
            return socket.fromshare(protoinfo)
    else:

        winsock = windll.ws2_32
        WSASocket = winsock.WSASocketA
        WSADuplicateSocket = winsock.WSADuplicateSocketA
        WSAGetLastError = winsock.WSAGetLastError
        WSASetLastError = winsock.WSASetLastError
        WSAclose = winsock.closesocket
        PyErr_SetExcFromWindowsErr = pythonapi.PyErr_SetExcFromWindowsErr
        PyErr_SetExcFromWindowsErr.argtypes = [py_object, c_int]

        def _raise_socket_error():
            ec = WSAGetLastError()
            WSASetLastError(0)
            PyErr_SetExcFromWindowsErr(socket.error, ec)

        def dupsock(sock, pid):
            pinfo = create_string_buffer(512)
            rv = WSADuplicateSocket(sock.fileno(), pid, pinfo)
            if rv != 0:
                _raise_socket_error()
            return pinfo.raw

        ## Replicate the relevant fields from socketmodule.h. This has been
        ## consistent through CPython 2.5 (the first to support ctypes)
        ## through 2.7.3, and for CPython 3.0 to 3.3, where it is
        ## unnecessary. It is unlikely to change, since 2.7 is the last
        ## major version of Python 2.x.
        class _socketobject(Structure):
            _fields_ = [("refcount", c_size_t),
                        ("classptr", py_object),
                        ("fd", c_int)]

        class _socketunion(Union):
            _fields_ = [('pyo', py_object),
                       ('sock', POINTER(_socketobject))]

        ## This function hacks a socket object to change its descriptor to the
        ## one returned by WSASocket.
        def make_socket(af, stype, proto, protoinfo):
            ## Get a socket handle for the socket we want to create
            newfd = WSASocket(af, stype, proto, protoinfo, 0, 0)
            if newfd < 0:
                _raise_socket_error()

            ## Create a new socket object
            sock = socket.socket(af, stype, proto)

            ## Get the original file descriptor so we can close it
            rfd = sock.fileno()

            try:
                sobj = sock._sock
            except AttributeError:
                sobj = sock
            sobj = _socketunion(sobj).sock.contents
            assert sobj.fd == rfd, 'socket structure mismatch'

            ## Replace the descriptor with the new value
            sobj.fd = newfd

            ## Close the original descriptor
            WSAclose(rfd)
            return sock

    MAGIC_ARG = '--easycluster-run-server'

    def spawn_runner_process(csock, peername, key, kwargs, close=()):
        args = [_python_exe, '-m', 'easycluster.__main__', MAGIC_ARG]
        p = subprocess.Popen(args, stdin=subprocess.PIPE)
        pinfo = dupsock(csock, p.pid)
        p.stdin.write(_core.b2a_hex(
                _core.pickle.dumps((pinfo, csock.family, csock.type,
                                    csock.proto, peername, key, kwargs),
                                   protocol=_core.pickle.HIGHEST_PROTOCOL)) + b'\r\n')
        p.stdin.close()

    def server_check_runner():
        if len(sys.argv) == 2 and sys.argv[1] == MAGIC_ARG:
            pinfo, family, type, proto, peername, key, args = _core.pickle.loads(_core._hexdec(sys.stdin.readline().strip()))
            sys.stdin.close()
            sock = make_socket(family, type, proto, pinfo)
            try:
                svr = Server(key, sock, peername, **args)
                while svr:
                    svr = svr.run()
            except Exception:
                traceback.print_exc()
            sys.exit(0)

    def server_init():
        pass

    _daemonize = None

else:
    import signal

    try:
        _max_fd = os.sysconf('SC_OPEN_MAX')
    except Exception:
        _max_fd = 1024

    def server_check_runner():
        pass

    def spawn_runner_process(csock, peername, key, args, close=()):
        cpid = os.fork()
        if cpid == 0:
            for sock in close:
                sock.close()
            # This fucks up os.urandom()
            #fd = csock.fileno()
            #os.closerange(3, fd)
            #os.closerange(fd + 1, _max_fd)
            try:
                svr = Server(key, csock, peername, **args)
                while svr:
                    svr = svr.run()
            except Exception:
                traceback.print_exc()
            sys.exit(0)

    def _sigcld(signal, frame):
        try:
            while True:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if not pid:
                    return
        except OSError:
            pass

    def server_init():
        signal.signal(signal.SIGCLD, _sigcld)

    def _daemonize(pidfile=None):
        """Makes the process into a daemon."""

        cpid = os.fork()
        if cpid != 0:
            if pidfile is not None:
                try:
                    with open(pidfile, 'w') as fp:
                        fp.write('%d\n' % cpid)
                except Exception:
                    os.kill(cpid, signal.SIGTERM)
                    raise
            os._exit(0)

        closefd = True
        fd = os.open(os.devnull, os.O_RDWR)
        for tfd in (0, 1, 2):
            if tfd == fd:
                closefd = False
            else:
                os.dup2(fd, tfd)
        if closefd:
            os.close(fd)

        os.setsid()

if _is_main:
    sys.exit(server_main())
