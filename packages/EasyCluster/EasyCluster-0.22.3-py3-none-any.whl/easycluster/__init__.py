# Copyright (C) 2022 Katie Rust (katie@ktpanda.org)
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

"""\
EasyCluster
===========

EasyCluster is a remote execution / clustering module for Python.

The latest version of this module is available from
U{https://pypi.python.org/pypi/EasyCluster}.

For general documentation, see U{http://pythonhosted.org/EasyCluster/}.

Quick start
-----------

To get started, first generate a keyfile::

    $ easycluster -g secret.key
    $ ls -l secret.key
    -rw------- 1 1000 1000 65 2012-12-05 16:00 test.key

Then start the server::

    $ easycluster --serve -k secret.key
    Listening on port 11999

Example usage:

>>> from easycluster import *
>>> define_common('''
... def addvals(a, b):
...     return a + b
... def subvals(a, b):
...     return a - b
... ''')
>>> key = read_key_file('secret.key')
>>> rmt = Client(key, 'localhost')
>>> rmt.execblock('print "Hello"')
>>>

"Hello" will be printed on the server side.

>>> rmt.addvals(3, 4)
7
>>> rmt.subvals(15, 4)
11
>>> rmt.subprocess.call(['/bin/echo', 'hello'])

"""
from __future__ import print_function

import sys
import os
import os.path
import re
import signal
import socket
import select
import traceback
import struct
import weakref
import time
import hmac
import threading
import errno
import zlib
import subprocess
from hashlib import md5
from io import BytesIO, IOBase
from types import GeneratorType, ModuleType, FunctionType, BuiltinFunctionType
from collections import deque
from binascii import a2b_hex, b2a_hex

try:
    import fcntl
except ImportError:
    fcntl = None

VERSION = "0.22.3"
MIN_SERVER_VERSION = '0.09'

PYTHON3 = sys.version_info >= (3, 0)
if PYTHON3:
    import pickle
    import queue
    import builtins
    def _hexenc(data):
        return b2a_hex(data).decode('ascii')
    def _hexdec(data):
        return a2b_hex(data.encode('ascii'))
    def _str_to_bytes(data):
        return str(data).encode('utf-8')

    _next_method = '__next__'

    DEFAULT_PORT = 11998
else:
    import cPickle as pickle
    import Queue as queue
    import __builtin__ as builtins
    _hexenc = b2a_hex
    _hexdec = a2b_hex
    _str_to_bytes = str

    ## Make all classes new-style by default
    __metaclass__ = type
    _next_method = 'next'

    DEFAULT_PORT = 11999

try:
    from select import epoll
except ImportError:
    epoll = None

__all__ = ['AutoThreadingClient', 'ThreadedClient', 'Client', 'ClientGroup',
           'Connection', 'DefaultRemoteProxy', 'RemoteException', 'RemoteProxy',
           'SelfIterProxy', 'ServerObject', 'add_key_options',
           'call_method_multi', 'call_multi', 'decode_key', 'define_common',
           'definitions_module', 'eval_multi', 'exec_return', 'execblock_multi',
           'generate_key', 'key_from_options', 'make_server_class',
           'make_singleton', 'read_key_file', 'write_key_file',
           'parse_connection_spec']

## Special value for TID which causes thread to exit after one request
SINGLE = -1

_nonblocking_errors = set()
for k in ('EWOULDBLOCK', 'EINTR', 'EINPROGRESS', 'EAGAIN'):
    val = getattr(errno, k, None)
    if val is not None:
        _nonblocking_errors.add(val)
del k, val

## Methods we do not want to auto-export.
_forbidden_slots = set(['__init__', '__new__', '__del__', '__getattr__',
                        '__getattribute__', '__setattr__', '__delattr__'])

HMAC_MOD = md5
HMAC_SIZE = len(HMAC_MOD().digest())
ERROR, CHALLENGE, CHALLENGE_RESPONSE, KEEPALIVE, REQUEST, RESPONSE, INIT = range(7)
_pickle_messages = set([REQUEST, RESPONSE, INIT])

MSG_COMPRESSED = 0x80

_singletons = {}

_extra_base_classes = {}

def eval_multi(connections, code):
    '''Evaluates a Python expression on multiple connections in parallel. Does
    not return until all hosts finish executing the code.

    @type  connections: sequence
    @param connections: List (or other sequence) of Client instances to run the
    code on.

    @type  code: str
    @param code: The code to run, which will be executed in the context of the
    easycluster.remote_code module.

    @rtype:  list
    @return: A list of return values in the same order as C{connections}. To
    associate the connections with return values, use C{zip(connections,
    eval_multi(connections, ...))}.
    '''

    resp = [h.eval(code, nonblocking=True) for h in connections]
    return [r.wait() for r in resp]

def execblock_multi(connections, code):
    '''Similar to L{eval_multi}, except C{code} is a block of python code
    instead of a single expression.

    @type  connections: sequence
    @param connections: List (or other sequence) of Client instances to run the
    code on.

    @type  code: str
    @param code: The code to run, which will be executed in the context of the
    easycluster.remote_code module.

    @rtype:  list
    @return: A list of return values in the same order as C{connections}. To
    associate the connections with return values, use C{zip(connections,
    execblock_multi(connections, ...))}.
    '''

    resp = [h.evalblock(code, nonblocking=True) for h in connections]
    return [r.wait() for r in resp]

def call_multi(_connections, _func, *a, **kw):
    '''Calls a function on multiple connections in parallel. Any extra
    positional and keyword arguments are passed to the remote function.

    @type  _connections: sequence
    @param _connections: A list (or other sequence) of connections to call the
    function on.

    @type  _func: str
    @param _func: The name of the function to call. See L{Client.call} for
    details.

    @rtype:  list
    @return: A list of return values in the same order as C{_connections}. To
    associate the connections with return values, use C{zip(connections,
    call_multi(connections, ...))}.
    '''
    resp = [h.raw_call(_func, a, kw, nonblocking=True) for h in _connections]
    return [r.wait() for r in resp]

def call_method_multi(_objects, _method, *a, **kw):
    '''Calls a method on multiple L{RemoteProxy} objects in parallel. Each
    object should be associated with a different L{Client} instance, although
    this is not enforced. Any extra positional and keyword arguments are passed
    to the remote function.

    @type  _objects: sequence
    @param _objects: A list (or other sequence) of L{RemoteProxy} objects to
    call the method on.

    @type  _method: str
    @param _method: The name of the method to be called.

    @rtype:  list
    @return: A list of return values in the same order as C{_objects}. To
    associate the connections with return values, use C{zip(objects,
    call_method_multi(objects, ...))}.
    '''
    resp = [o.raw_call_method(_method, a, kw, nonblocking=True) for o in _objects]
    return [r.wait() for r in resp]

def make_server_class(typ, export_methods=('@auto',), export_attrs=('@auto',),
                      export_attrs_cache=(), proxy_class=None):
    '''Mark a pre-existing class as a server-object class. This function will
    attempt to assign attributes to 'typ'; if that fails, the type will be added
    to a global dictionary.

    @type  typ: class
    @param typ: An old-style or new-style class.

    @type  export_methods: sequence
    @param export_methods: A sequence of method names that the class exports. If
    the sequence contains C{'@auto'} (default), then the class will be scanned
    to determine the methods that it supports.

    @type  export_attrs: sequence
    @param export_attrs: A sequence of attribute names that the class
    exports. If the sequence contains C{'@auto'} (default), then the dynamically generated
    proxy class will subclass from DefaultRemoteProxy, and will therefore
    forward unknown attribute requests to the remote object.

    @type  export_attrs_cache: sequence
    @param export_attrs_cache: Like C{export_attrs}, except the proxy will only
    request the attribute once, and will store the value on the client. Use this
    for attributes which you are 100% certain will not change over the lifetime
    of the object.

    @type  proxy_class: class
    @param proxy_class: A class to instantiate as a proxy for C{typ}. If this is
    specified, then all other parameters will be ignored. This class must be
    importable on the client; generally, classes defined in the top level of a
    module or in L{define_common} are supported.
    '''

    typedat = _make_typedat(
        typ, export_methods, export_attrs, export_attrs_cache, proxy_class)

    try:
        typ._easycluster_server_object_typedat = typedat
    except Exception:
        # If setting attributes on the type fails, it probably means it's an
        # extension type that doesn't have a __dict__. In that case, store it in
        # _extra_base_classes; Server.persistent_id searches through the MRO of
        # new-style classes to find the first one in this dict.
        _extra_base_classes[typ] = typedat

def make_singleton(obj, export_methods=('@auto',), export_attrs=('@auto',),
                   export_attrs_cache=(), proxy_class=None):
    '''Mark an object instance as a server object. Similar to
    L{make_server_class}, except this marks a single object as a server object,
    instead of all instances of a class.

    @type  obj: object
    @param obj: Any object

    @type  export_methods: sequence
    @param export_methods: A sequence of method names that the class exports. If
    the sequence contains C{'@auto'} (default), then the class of C{obj} will be scanned
    to determine the methods that it supports.

    @type  export_attrs: sequence
    @param export_attrs: A sequence of attribute names that the class
    exports. If the sequence contains C{'@auto'} (default), then the dynamically generated
    proxy class will subclass from DefaultRemoteProxy, and will therefore
    forward unknown attribute requests to the remote object.

    @type  export_attrs_cache: sequence
    @param export_attrs_cache: Like C{export_attrs}, except the proxy will only
    request the attribute once, and will store the value on the client. Use this
    for attributes which you are 100% certain will not change over the lifetime
    of the object.

    @type  proxy_class: class
    @param proxy_class: A class to instantiate as a proxy for C{obj}. If this is
    specified, then all other parameters will be ignored. This class must be
    importable on the client; generally, classes defined in the top level of a
    module or in L{define_common} are supported.

    @rtype:  object
    @return: The value of C{obj}.
    '''

    addr = id(obj)
    def wrcb(wr, addr=addr):
        _singletons.pop(addr, None)

    strong_ref = obj
    try:
        weak_ref = weakref.ref(obj, wrcb)
        strong_ref = None
    except TypeError:
        ## type(obj) is not weakref-capable.
        weak_ref = None

    typedat = _make_typedat(
        obj.__class__, export_methods, export_attrs, export_attrs_cache, proxy_class)
    _singletons[addr] = typedat, weak_ref, strong_ref
    return obj

class _DummyConnection(object):
    '''Replacement object for _connection in invalidated proxies.'''
    peername = '<closed connection>'
    def send_request(self, *a, **kw):
        raise IOError("Connection has been closed")

_dummy_connection = _DummyConnection()

class _RemoteProxyRef(weakref.ref):
    '''A weak reference to a remote proxy. Used to tell the Client class when a
    proxy is no longer being used so the server can delete the object it refers
    to.'''
    __slots__ = ('oid',)
    def __new__(cls, prox, cb, oid):
        self = weakref.ref.__new__(cls, prox, cb)
        self.oid = oid
        return self

    def __init__(self, prox, cb, oid):
        super(_RemoteProxyRef, self).__init__(prox, cb)

def _create_wrapper_method(name):
    def rtnf(self, *a, **kw):
        return self._connection.send_request(self._oid, name, a, kw, *_get_special_keywords(kw))
    rtnf.__name__ = name
    return rtnf

def _create_attr_wrapper(name):
    def get(self):
        return self._connection.send_request(0, 'getattr', (self, name))

    def set(self, value):
        return self._connection.send_request(0, 'setattr', (self, name, value))

    def delete(self):
        return self._connection.send_request(0, 'delattr', (self, name))

    return property(get, set, delete)

def _create_cached_attr_wrapper(name):
    non_existant = object()
    def get(self):
        d = self.__dict__
        val = d.get(name, non_existant)
        if val is not non_existant:
            return val
        val = self._connection.send_request(0, 'getattr', (self, name))
        d[name] = val
        return val

    def set(self, value):
        self.__dict__.pop(name, None)
        rv = self._connection.send_request(0, 'setattr', (self, name, value))
        return rv

    def delete(self):
        self.__dict__.pop(name, None)
        return self._connection.send_request(0, 'delattr', (self, name))

    return property(get, set, delete)

class _RemoteProxyMeta(type):
    '''Metaclass for L{RemoteProxy} and subclasses'''
    def __new__(mcs, clsname, bases, typedict):
        proxy_methods = typedict.setdefault('proxy_methods', ())
        proxy_attrs = typedict.setdefault('proxy_attrs', ())
        proxy_attrs_cache = typedict.setdefault('proxy_attrs_cache', ())

        for name in proxy_methods:
            typedict[name] = _create_wrapper_method(name)

        for name in proxy_attrs:
            typedict[name] = _create_attr_wrapper(name)

        for name in proxy_attrs_cache:
            typedict[name] = _create_cached_attr_wrapper(name)

        return super(_RemoteProxyMeta, mcs).__new__(mcs, clsname, bases, typedict)

_RemoteProxyBase = _RemoteProxyMeta('_RemoteProxyBase', (object,), {'__module__': __name__})

class RemoteProxy(_RemoteProxyBase):
    '''A client-side proxy for an object on the server.'''

    _connection = None
    _oid = None

    def __init__(self, client, oid):
        '''Create a RemoteProxy object. This should not be called
        directly. RemoteProxy objects are created automatically when a
        ServerObject is returned by the server.'''

        self._connection = client
        self._oid = oid

    @property
    def proxy_connection(self):
        '''Returns the connection that this object is associated with, or None
        if the connection was closed.'''
        ret = self._connection
        if ret is _dummy_connection:
            ret = None
        return ret

    @property
    def proxy_object_id(self):
        '''The object ID assigned by the remote connection for this object'''
        return self._oid

    def raw_call_method(self, method, args, kwargs={}, nonblocking=False,
                        oncomplete=None, onerror=None, threadid=None,
                        origexc=True):
        '''Call a method on the remote object.

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.

        @type  method: str
        @param method: The name the method to call.

        @type  args: tuple
        @param args: Positional arguments to the method.

        @type  kwargs: dict
        @param kwargs: Keyword arguments to the method.

        @return: Whatever the remote method returns, or a L{NonblockingResponse}
        if C{nonblocking} is True.
        '''
        return self._connection.send_request(self._oid, method, args, kwargs,
                                         nonblocking, oncomplete, onerror, threadid, origexc)

    def raw_get_attribute(self, attr, nonblocking=False,
                        oncomplete=None, onerror=None, threadid=None,
                        origexc=True):
        '''Get the value of an attribute on the remote object.

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.

        @type  attr: str
        @param attr: The name of the attribute.

        @return: The value of the attribute, or a L{NonblockingResponse} if
        C{nonblocking} is True.
        '''
        return self._connection.send_request(0, 'getattr', (self, attr), {},
                                             nonblocking, oncomplete, onerror, threadid, origexc)

    def raw_set_attribute(self, attr, val, nonblocking=False,
                        oncomplete=None, onerror=None, threadid=None,
                        origexc=True):
        '''Set the value of an attribute on the remote object.

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.

        @type  attr: str
        @param attr: The name of the attribute.

        @type  val: object
        @param val: The value to set.

        @return: None, or a L{NonblockingResponse} if C{nonblocking} is True.
        '''
        return self._connection.send_request(0, 'setattr', (self, attr, val), {},
                                             nonblocking, oncomplete, onerror, threadid, origexc)

    def __repr__(self):
        return '<RemoteProxy for oid %d on %s>' % (self._oid, self._connection.peername)

class DefaultRemoteProxy(RemoteProxy):
    """A remote proxy for server-side classes that want to automatically export
    attributes and methods.

    Classes which inherit from this class should define all *local*
    instance attributes on the class itself, like so::

        class SpecialProxy(DefaultRemoteProxy):
            special_dict = None

            def __init__(self, *args, **kw):
                super(SpecialProxy, self).__init__(*args, **kw)
                self.special_dict = {}

    Otherwise, setting self.special_dict will cause that value to be set on the
    *remote* object.
    """

    _known_methods = None
    def __init__(self, *args, **kw):
        super(DefaultRemoteProxy, self).__init__(*args, **kw)
        self._known_methods = {}

    def __getattr__(self, attr):
        meth = self._known_methods.get(attr)
        if meth:
            return meth.__get__(self)

        try:
            ismethod, val = self._connection.send_request(0, 'getmethod', (self, attr), origexc=False)
            if not ismethod:
                return val
            meth = self._known_methods[attr] = _create_wrapper_method(attr)
            return meth.__get__(self)

        except RemoteException as re:
            # Don't report AttributeError: we may be called by hasattr, or
            # getattr(a, 'attr', None).
            if not isinstance(re.orig, AttributeError):
                self._connection.report_exception(re)
            raise re.orig

    def __setattr__(self, attr, val):
        if hasattr(type(self), attr) or attr in self.__dict__:
            return RemoteProxy.__setattr__(self, attr, val)
        return self._connection.send_request(0, 'setattr', (self, attr, val))

    def __delattr__(self, attr):
        if hasattr(type(self), attr) or attr in self.__dict__:
            return RemoteProxy.__delattr__(self, attr)
        return self._connection.send_request(0, 'delattr', (self, attr))

class SelfIterProxy(RemoteProxy):
    """A proxy class for an iterator which returns itself when __iter__ is
    called."""
    proxy_methods = (_next_method,)

    def __iter__(self):
        return self

class _TypeData(str):
    pass

class ServerObject:
    '''A base class for objects which can be referenced by a client.'''
    _easycluster_server_object_typedat = _TypeData('')

    export_methods = '@auto',
    '''Subclasses can override this attribute to specify which methods to
    export. See L{make_server_class} for details.'''

    export_attrs = '@auto',
    '''Subclasses can override this attribute to specify which attributes to
    export. See L{make_server_class} for details.'''

    export_attrs_cache = ()
    '''Subclasses can override this attribute to specify which attributes never
    change, and can be cached on the client. See L{make_server_class} for
    details.'''

    proxy_class = None
    '''Subclasses can override this attribute to directly specify a proxy class.
    If this is specified, then C{export_methods}, C{export_attrs}, and
    C{export_attrs_cache} are ignored. See L{make_server_class} for details.'''

class RemoteException(Exception):
    '''Raised on the client when an exception occurs during execution, and
    C{origexc} is False. See L{Client.send_request} for more information.
    '''
    def __init__(self, orig=None, text=None):
        Exception.__init__(self, str(orig))

        self.orig = orig
        '''The original exception raised by the call.'''

        self.text = text
        '''A list of strings as returned by L{traceback.format_exception}.'''

class NonblockingResponse:
    '''Returned by remote calls when the C{nonblocking} flag is set to True. See
    L{Client.send_request} for more information.'''
    def __init__(self, client, request_id, origexc):
        self.client = client
        self.request_id = request_id
        self._have_response = False
        self._response_val = None
        self._origexc = origexc

    @property
    def have_response(self):
        '''True if a response is available.'''
        return self._have_response

    def fileno(self):
        '''Returns the file descriptor of the associated Client instance so that
        responses can be used with select().'''
        return self.client.fileno()

    def read_response(self, block=True):
        '''Calls C{read_response} on the associated C{Client}.'''
        return self.client.read_response(block)

    def set_response(self, val):
        self._response_val = val
        self._have_response = True

    def wait(self, origexc=None):
        '''Waits for the request to complete.
        '''

        if origexc is None:
            origexc = self._origexc

        self.client._wait_for_response(self)

        rval = self._response_val
        if type(rval) is RemoteException:
            if origexc:
                if origexc != 'quiet':
                    self.client.report_exception(rval)
                raise rval.orig
            raise rval
        return rval

class Connection:
    '''Base class for Client and Server objects'''
    def __init__(self, key, enable_compression=False):
        self._key = key
        self._recv_buf = BytesIO()
        self._recv_expect = 5
        self._recv_msgtype = None
        self._recv_data = None
        self._peer_version = None

        self._my_nonce = struct.pack('>d', time.time()) + os.urandom(HMAC_SIZE - 8)
        self._verified = key is None
        self._recv_expect_hmac = None
        self._recv_hmac = None
        self._send_hmac = None

        self._sock = None
        self._peername = ''
        self._remote_host = None
        self._remote_port = None
        self._ssh = None
        self._ssh_user = None
        self._ssh_extra_args = ()

        self._lock = threading.Lock()
        self._sendlock = threading.Lock()

        self._enable_compression = enable_compression
        self._peer_enable_compression = False
        self._compress = self._decompress = None
        self._peer_init_data = {}
        self._delay_digest = b''
        self._pickle_protocol = 2

        self._init_data = {
            'version': VERSION,
            'enable-compression': self._enable_compression,
            'supported-pickle-protocol': pickle.HIGHEST_PROTOCOL
        }

    @property
    def peername(self):
        '''The name of the host we are connected to'''
        return self._peername

    @property
    def connected(self):
        '''True if we are connected to a remote host.'''
        return self._sock is not None

    @property
    def remote_host(self):
        '''The hostname or IP address passed to connect(), or None for a local
        connection'''
        return self._remote_host

    @property
    def remote_port(self):
        '''The TCP port passed to connect(), or None for a local connection'''
        return self._remote_port

    def connect(self, host, port=None, peername=None, user=None, ssh=None, rpython=None, extra_args=()):
        '''Connect to a remote host.'''

        if port is None:
            port = (22 if ssh else DEFAULT_PORT)

        if ssh is True:
            ssh = 'ssh'

        if rpython is None:
            rpython = _ssh_default_python

        self._remote_host = host
        self._remote_port = port
        self._ssh = ssh
        self._ssh_user = user
        self._ssh_rpython = rpython
        self._ssh_extra_args = extra_args

        if peername is None:
            peername = '%s:%d' % (host, port)

        if ssh:
            userhost = ('%s@%s' % (user, host) if user is not None else host)
            args = [ssh, '-p', str(port), userhost]
            args.extend(extra_args)
            args.append(rpython + _ssh_python_args)
            sock = _prepare_ssh(args)
        else:
            if self._key is None:
                raise ValueError('HMAC key must be specified when not using SSH')
            sock = socket.create_connection((host, port))

        self.set_socket(sock, peername)

    def reconnect(self):
        '''Reconnect to the remote host. This will reset the remote environment,
        and any currently held proxied objects will become invalid.'''
        if self._remote_host is None:
            raise ValueError('Cannot reconnect before first connection.')
        self.close()
        self.connect(self._remote_host, self._remote_port, self._peername,
                     self._ssh_user, self._ssh, self._ssh_rpython, self._ssh_extra_args)

    def set_socket(self, sock, peername=None):
        '''Use an already-open socket for this connection.'''
        if peername is None:
            peername = _get_peer_name(sock.getpeername())

        _mark_non_inheritable(sock.fileno())
        try:
            _mark_non_inheritable(sock.write_fileno())
        except AttributeError:
            pass
        self._sock = sock
        self._peername = peername
        if self._key is not None:
            self._recv_hmac = hmac.new(self._key, self._recviv, HMAC_MOD)
            self._send_hmac = hmac.new(self._key, self._sendiv, HMAC_MOD)
        self._compress = zlib.compressobj(zlib.Z_BEST_COMPRESSION)
        self._decompress = zlib.decompressobj()
        self._delay_digest = b''
        self._after_connect()

    def _after_connect(self):
        pass

    def send_challenge(self):
        if self._key is not None:
            self.send_message(CHALLENGE, self._my_nonce)
        else:
            self.send_message(INIT, self.make_pickle(self._init_data))

    def _on_ready(self):
        pass

    def send_message(self, typ, data, delay_hmac=False):
        hmac = self._send_hmac

        with self._sendlock:
            if (self._enable_compression and self._peer_enable_compression and
                typ in _pickle_messages and len(data) >= 32):
                typ |= MSG_COMPRESSED
                c = self._compress
                data = c.compress(data)
                data += c.flush(zlib.Z_SYNC_FLUSH)

            hdr = struct.pack('>BI', typ, len(data))
            if hmac:
                hmac.update(hdr)
                hmac.update(data)
            digest = prev_hmac = b''
            if hmac:
                if typ != ERROR:
                    digest = hmac.digest()
                    hmac.update(digest)

                prev_hmac = self._delay_digest
                if prev_hmac:
                    if typ == ERROR:
                        prev_hmac = b'\x00' * len(prev_hmac)
                    self._delay_digest = b''

            if delay_hmac:
                data = b''.join((prev_hmac, hdr, data))
                self._delay_digest = digest
            else:
                data = b''.join((prev_hmac, hdr, data, digest))
            _sock_sendall(self._sock, data)

    def make_pickle(self, object):
        sio = BytesIO()
        p = pickle.Pickler(sio, protocol=self._pickle_protocol)
        p.persistent_id = self._persistent_id
        p.dump(object)
        return sio.getvalue()

    def fileno(self):
        '''Returns the file descriptor of the connected socket.'''
        return self._sock.fileno()

    def write_fileno(self):
        '''Returns the file descriptor used to write to the connected
        socket. For normal sockets, this is the same as fileno(); for pipe-based
        connections, it will be different'''
        try:
            return self._sock.write_fileno()
        except AttributeError:
            return self._sock.fileno()


    def _got_request(self, p):
        return True

    def _got_response(self, p):
        return True

    def _got_init(self, p):
        self._peer_version = vers = p.get('version')
        self._peer_init_data = p

        self._peer_enable_compression = p.get('enable-compression', False)

        self._pickle_protocol = min(p.get('supported-pickle-protocol', pickle.HIGHEST_PROTOCOL), pickle.HIGHEST_PROTOCOL)

        return self._check_version(vers)

    def _got_keepalive(self):
        pass

    def _got_challenge(self, data):
        self.send_message(CHALLENGE_RESPONSE, data)

    def _read_data(self, block=True):
        ## attribute access protected by GIL
        sock = self._sock
        if sock is None:
            raise EOFError

        recv_buf = self._recv_buf
        recv_hmac = self._recv_hmac

        while True:
            try:
                data = sock.recv(self._recv_expect)
            except (socket.error, OSError) as e:
                if e.errno not in _nonblocking_errors:
                    raise
                if not block:
                    return False
                select.select([sock], [], [], None)
                continue

            if not data:
                raise EOFError

            if recv_hmac:
                recv_hmac.update(data)

            recv_buf.write(data)
            newlen = self._recv_expect - len(data)
            if newlen > 0:
                if newlen > 256 and not self._verified:
                    self.send_message(ERROR, b'Initial message too long')
                    self.close()
                self._recv_expect = newlen
                continue

            data = recv_buf.getvalue()
            recv_buf.seek(0)
            recv_buf.truncate(0)
            if self._recv_msgtype is None:
                self._recv_msgtype, self._recv_expect = struct.unpack('>BI', data)
                if self._recv_expect == 0:
                    data = ''
                else:
                    continue

            if self._recv_msgtype == ERROR:
                self._recv_msgtype = None
                self._recv_expect = 5
                raise ValueError('Peer error: %s' % data)

            if self._recv_data is None:
                self._recv_data = data
                if recv_hmac:
                    self._recv_expect_hmac = recv_hmac.digest()
                    self._recv_expect = HMAC_SIZE
                    continue

            rmsg = self._recv_msgtype
            rdata = self._recv_data
            if recv_hmac:
                expect_hmac = self._recv_expect_hmac

            self._recv_expect = 5
            self._recv_msgtype = None
            self._recv_data = None
            self._recv_expect_hmac = None

            if recv_hmac and data != expect_hmac:
                self.send_message(ERROR, b'HMAC error')
                continue

            if rmsg & MSG_COMPRESSED:
                rmsg &= ~MSG_COMPRESSED
                rdata = self._decompress.decompress(rdata)

            if rmsg in _pickle_messages:
                if not self._verified:
                    self.send_message(ERROR, b'Not verified')
                    continue

                p = pickle.Unpickler(BytesIO(rdata))
                p.persistent_load = self._persistent_load
                pick = p.load()
                if rmsg == REQUEST:
                    return self._got_request(pick)
                elif rmsg == RESPONSE:
                    return self._got_response(pick)
                elif rmsg == INIT:
                    try:
                        ready = self._got_init(pick)
                    except ValueError as e:
                        self.send_message(ERROR, _str_to_bytes(e))
                        raise
                    if ready:
                        self._on_ready()
                    return True

            elif rmsg == KEEPALIVE:
                self._got_keepalive()
            elif rmsg == CHALLENGE:
                self._got_challenge(rdata)
            elif rmsg == CHALLENGE_RESPONSE:
                if rdata == self._my_nonce:
                    self._verified = True
                    self.send_message(INIT, self.make_pickle(self._init_data))
                else:
                    self.send_message(ERROR, b'Invalid nonce')
            else:
                self.send_message(ERROR, b'Invalid message type')

    def close(self):
        '''Close the connection.'''
        if self._sock is not None:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock = None

class _GlobalProxy:
    '''A proxy for a global object on a remote server'''
    __slots__ = ('_client', '_name')
    def __init__(self, client, name):
        self._client = client
        self._name = name

    def __getattribute__(self, name):
        ## Using a @property and having a fallback __getattr__ does not work as
        ## expected: if the remote call raises an AttributeError, it will be
        ## ignored and __getattr__ will be called instead.

        if name == 'value':
            return self._client.send_request(0, 'get_global', (self._name,))
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return _GlobalProxy(self._client, self._name + '.' + name)

    def __setattr__(self, name, newval):
        if name == 'value':
            self._client.send_request(0, 'set_global', (self._name, newval))
            return newval
        return object.__setattr__(self, name, newval)

    def __call__(self, *args, **kw):
        return self._client.raw_call(self._name, args, kw, *_get_special_keywords(kw))

_upgrade_code = r'''
import sys, os, zlib
import easycluster as _core
import easycluster.server as _server
def upgrade(osvr, defmod):
    global coredata, svrdata, sshdata, upgradecode
    for mod, ztxt in ((_core, coredata), (_server, svrdata)):
        mod._compcode = ztxt
        cb = compile(zlib.decompress(ztxt).decode('utf-8'), mod.__file__, 'exec', dont_inherit=True)
        eval(cb, mod.__dict__)
    defmod.define('import easycluster\nfrom easycluster import *\n')
    return _server.Server(osvr._key, osvr._sock, osvr._peername, osvr._verbosity, osvr)
''' # '''

## Bootstrap code to do an in-memory upgrade on versions older than 0.19
_compat_upgrade_code = _upgrade_code + r'''
defmod = sys.modules[initdata['definitions_module']]
osvr = defmod.running_server
def hack_req(*args):
    osvr._peer_init_data = initdata
    if type(osvr).__name__ == 'QuietServer':
        osvr._verbosity = 0
    else:
        osvr._verbosity = 2
    nsvr = upgrade(osvr, defmod)
    nsvr._got_request(*args)
    _exit = os._exit
    globals().clear()
    try:
        while nsvr:
            nsvr = nsvr.run()
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        _exit(0)

osvr._got_request = hack_req
''' # '''


class Client(Connection):
    '''Represents the client side of the connection.'''

    _sendiv = b'CLNT'
    _recviv = b'SRVR'

    def __init__(self, key=None, host=None, port=None,
                 definitions='easycluster.remote_code',
                 enable_compression=False, ssh=None, user=None,
                 rpython=None, extra_args=()):
        '''Create a new Client object.

        @type  key: bytes
        @param key: The HMAC key to use. See L{read_key_file} and
        L{decode_key}. If C{key} is None, then SSH will be used to connect.

        @type  host: str
        @param host: A host name or IP address to connect to. If C{host} is not
        specified, you must call L{connect} or L{set_socket} before using the
        C{Client} instance.

        @type  port: int
        @param port: The TCP port to use, if a host name is given.

        @type  definitions: str
        @param definitions: The name of the dynamic module where common
        definitions are stored. This must be the same name passed to
        L{define_common} or L{definitions_module}

        @type  enable_compression: bool
        @param enable_compression: A flag specifying whether or not to enable
        compression for this connection.

        @type  ssh: str or bool
        @param ssh: Set to True to use SSH to connect, or to a string to use a
        custom SSH path. If SSH is used, then the remote server does not need to
        have EasyCluster installed, only Python. If C{port} is not specified, it
        defaults to 22.

        @type  user: str
        @param user: The username to conenct as when using SSH

        @type  rpython: str
        @param rpython: The name or path to the python binary on the remote
        server. Defaults to 'python' when using Python 2.x or 'python3' when
        using Python 3.x.

        @type  extra_args: sequence
        @param extra_args: A list or tuple of extra arguments to pass to SSH
        '''

        if key is None and ssh is None:
            ssh = 'ssh'

        if ssh:
            key = None

        super(Client, self).__init__(key, enable_compression)

        self._next_request_id = 0
        self._pending_requests = None
        self._nonblocking_responses = {}
        self._completion = {}

        self._default_thread = 0

        def proxy_deleted(refdat, wrself=weakref.ref(self)):
            self = wrself()
            if self is not None:
                self._proxy_by_id.pop(refdat.oid, None)
                self._garbage_proxies.append(refdat.oid)

        self._proxy_deleted = proxy_deleted

        ## Proxies that we have for remote objects
        self._proxy_by_id = {}
        self._proxy_type_by_id = {}
        self._garbage_proxies = []

        self._is_ready = False
        self._defmod = definitions_module(definitions)
        self._init_data['definitions_module'] = definitions

        self._peer_version = None

        self._initial_def_update = None

        if host is not None:
            self.connect(host, port, ssh=ssh, rpython=rpython, user=user, extra_args=extra_args)

    @classmethod
    def from_spec(cls, spec, default_port=None, default_key=None, warn=True):
        '''Convenience method which creates a new instance from a connection spec.
        See L{parse_connection_spec} for the meaning of the parameters.
        '''

        params = parse_connection_spec(spec, default_port, default_key, (), warn)
        return cls(**params)

    def _send_upgrade(self, compat=False):
        '''Sends upgrade code to the remote host'''
        coretxt, svrtxt = _get_upgrade_code()
        data = {
            'coredata': coretxt,
            'svrdata': svrtxt,
        }
        kw = {}
        if compat:
            data['initdata'] = self._init_data
            if PYTHON3:
                call = ('exec', (_compat_upgrade_code, data), kw)
            else:
                data['upgradecode'] = _compat_upgrade_code
                eval_args = ("eval(compile(upgradecode,'upgrade','exec'))", data)
                call = ('eval', eval_args, kw)
            request = (-1, [], SINGLE, 0, 'call', call, kw)
        else:
            request = (-1, [], None, 0, 'do_easycluster_upgrade', (_upgrade_code, data), kw)
        p = self.make_pickle(request)
        self._completion[-1] = self._upgrade_complete, self._init_error
        self.send_message(REQUEST, p)
        return False

    def _upgrade_complete(self, resp):
        self._on_ready()

    def _check_version(self, pv):
        if _version_compare(pv, VERSION) != 0:
            if _version_compare(pv, '0.09') < 0:
                raise ValueError('Incompatible EasyCluster version: client has version %s, server has version %s; '
                                 'client requires server to have at least version %s' % (VERSION, pv, MIN_SERVER_VERSION))

            else:
                return self._send_upgrade(_version_compare(pv, '0.19') < 0)
            ## Now we know the server supports compression.
            self._peer_enable_compression = False
        return True

    def _init_thread(self):
        self.send_challenge()

    def _after_connect(self):
        self._is_ready = False
        self._initial_def_update = None
        self._pending_requests = []
        self._init_response = None

        self._definition_count = 0

        self._sock.setblocking(0)
        self._init_thread()
        if self._defmod._source_code:
            self.update_definitions(oncomplete=self._on_update_complete,
                                    onerror=self._init_error)
            self._initial_def_update = self._pending_requests
            self._pending_requests = []

    def _init_error(self, exc):
        self.report_exception(exc)
        ## Raise the error in all outstanding requests
        self.close(exc)

    def read_response(self, block=True):
        '''Try to read a response and call its completion function (if any).
        Returns True when a response is received, or False if C{block} is false
        and a response was not processed.

        If using select or another I/O polling method, this method should be
        called after the poll indicates the socket is ready for reading.
        '''
        return self._read_data(block)

    def set_default_thread(self, threadid):
        '''Set the default thread id.'''
        self._default_thread = threadid

    def _on_ready(self):
        with self._lock:
            if self._initial_def_update is not None:
                rq = self._initial_def_update
                self._initial_def_update = []
            else:
                self._is_ready = True
                rq = self._pending_requests
                self._pending_requests = None
        for p in rq:
            self.send_message(REQUEST, p)

    def _on_update_complete(self, val):
        self._initial_def_update = None
        self._on_ready()


    def ready(self):
        '''Returns True if our peer is ready to accept requests.'''
        return self._is_ready

    def wait_ready(self):
        '''Wait until the peer is ready to accept requests.'''
        while not self._is_ready:
            self.read_response()

    def get_root(self):
        '''Returns a proxy for the 'root' object, which is used to implement
        'call' and 'eval' functions. See L{easycluster.server.RootObject}.'''
        return DefaultRemoteProxy(self, 0)

    def _thread_id(self):
        return self._default_thread

    def _set_nbr_response(self, nbr, response):
        '''Set the response value for a non-blocking response and wake it up if
        necessary.'''
        nbr.set_response(response)

    def _got_response(self, p):
        rid, response = p
        complete = self._completion.pop(rid, None)
        if not complete:
            nbr = self._nonblocking_responses.pop(rid, None)
            if nbr is None:
                return
            nbr = nbr()
            if nbr is None:
                return
            self._set_nbr_response(nbr, response)
            return True

        # index 0 = oncomplete, index 1 = onerror
        compf = complete[int(type(response) is RemoteException)]
        if isinstance(compf, tuple):
            compf[0](response, *compf[1:])
        else:
            compf(response)
        return True

    def send_request(self, oid, meth, args, kwargs={}, nonblocking=False,
                     oncomplete=None, onerror=None, threadid=None,
                     origexc=True):
        '''Send a request to the remote server. All requests go through this
        method. This method is normally not called directly, but several of the
        parameters are shared with other functions.

        Normally, this function will wait for the request to complete, then
        return whatever the remote call returns. However, if C{nonblocking} is
        True, or C{oncomplete} is given, then the function returns immediately,
        without waiting.

        @type  oid: int
        @param oid: The object ID of the object on which to call the method.

        @type  meth: str
        @param meth: The name of the method to call.

        @type  args: tuple
        @param args: Positional arguments to the method.

        @type  kwargs: dict
        @param kwargs: Keyword arguments to the method.

        @type  nonblocking: bool
        @param nonblocking: If True, then this method will not wait for the
        remote call to return, but will return a L{NonblockingResponse} object,
        which can be used to retrieve the result later. Ignored when
        C{oncomplete} is given.

        @type  oncomplete: function or tuple
        @param oncomplete: A function which is called with the return value when
        the request is complete. C{oncomplete} can be a tuple of C{(func, arg1,
        arg2, ...)}, in which case the function will be called as
        C{func(response, arg1, arg2, ...)}. If the request raises an exception,
        then the response will be an instance of L{RemoteException}.

        @type  onerror: function or tuple
        @param onerror: Like C{oncomplete}, except it is called instead of
        C{oncomplete} when the request causes an exception.

        @type  threadid: int
        @param threadid: Ihe remote thread to queue the response in. If not
        specified, the current default will be used. The default can be changed
        by calling L{set_default_thread}. If the specified thread does not
        exist on the server, it is created. If C{threadid} is the special
        constant L{SINGLE}, a new thread is created on the server for this request,
        then exits.

        @type  origexc: bool or str
        @param origexc: Determines what to raise if the call causes an
        exception. If True, the remote exception traceback is printed to
        sys.stderr and the original exception is raised. If False, a
        RemoteException is raised instead and the remote traceback is not
        printed. If C{origexc} is the special value C{'quiet'}, then the
        original exception is raised without printing a traceback. Ignored when
        C{oncomplete} is given.

        @return: L{NonblockingResponse} if C{nonblocking} is True; None if
        C{oncomplete} is specified; otherwise, the result of the remote call.
        '''
        with self._lock:
            if self._sock is None:
                raise IOError("Not connected")
            if threadid is None:
                threadid = self._thread_id()

            request_id = self._next_request_id
            self._next_request_id = request_id + 1

            garbage = []
            gobj = self._garbage_proxies
            while gobj:
                garbage.append(gobj.pop())

            try:
                rq = self.make_pickle((request_id, garbage, threadid,
                                       oid, meth, args, kwargs))
            except Exception:
                gobj.extend(garbage)
                raise

            if not self._is_ready:
                self._pending_requests.append(rq)
                rq = None

        if oncomplete is not None:
            if onerror is None:
                onerror = oncomplete
            self._completion[request_id] = oncomplete, onerror
            rval = request_id
        else:
            rval = NonblockingResponse(self, request_id, origexc)
            self._nonblocking_responses[request_id] = weakref.ref(rval)
        if rq is not None:
            self.send_message(REQUEST, rq)

        if oncomplete is None and not nonblocking:
            return rval.wait()
        return rval

    def report_exception(self, exc):
        '''Report a remote exception to sys.stderr. This can be
        overridden in a subclass to change exception reporting.

        @type  exc: RemoteException
        @param exc: The exception that was raised. The original exception value
        is available as C{exc.orig}, and the traceback is available as
        C{exc.text}.
        '''
        ## Don't print anything for StopIteration; remote iterators may generate this.
        if isinstance(exc.orig, StopIteration):
            return

        if exc.text:
            print('*** Remote exception from %s:' % (self._peername), file=sys.stderr)
            print(''.join(exc.text), file=sys.stderr)

    def stop_remote_thread(self, threadid):
        '''Stop the remote thread identified by C{threadid} once it has finished
        processing all of its requests.

        @type  threadid: int
        @param threadid: Thread to stop.
        '''

        self.send_message(REQUEST, self.make_pickle((None, None, threadid,
                                                     None, None, None, None)))

    def _wait_for_response(self, nbr):
        '''Wait for a response to complete.'''
        while not nbr._have_response:
            self.read_response()

    def update_definitions(self, nonblocking=False,
                           oncomplete=None, onerror=None, threadid=None, origexc=True):
        '''Call this after calling define_common to send any new common
        definitions to the server.

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.
        '''

        source = self._defmod._source_code
        current_count = self._definition_count
        rv = self.send_request(0, 'update_definitions', (source[current_count:],), {},
                          nonblocking, oncomplete, onerror, threadid, origexc)
        self._definition_count = len(source)
        return rv

    def raw_call(self, func, args, kwargs={}, nonblocking=False,
                        oncomplete=None, onerror=None, threadid=None, origexc=True):
        '''Call a function by name on the remote server.

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.

        @type  func: str
        @param func: The absolute name of the function to call. If C{func}
        is a simple name, it is assumed to be in the C{easycluster.remote_code}
        module.

        @type  args: tuple
        @param args: Positional arguments to the function.

        @type  kwargs: dict
        @param kwargs: Keyword arguments to the function.
        '''
        return self.send_request(0, 'call', (func, args, kwargs), {},
                                 nonblocking, oncomplete, onerror, threadid, origexc)

    def call(self, _func, *args, **kwargs):
        '''Call a function by name on the remote server.

        @type  _func: str
        @param _func: The absolute name of the function to call.

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.
        '''
        return self.raw_call(_func, args, kwargs, *_get_special_keywords(kwargs))

    def eval(self, expr, nonblocking=False, oncomplete=None, onerror=None, threadid=None, origexc=True):
        '''Evaluate an expression on the remote server. The code is executed in
        the context of the C{easycluster.remote_code} module.

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.

        @type  expr: str
        @param expr: The code to run, which will be executed in the context of the
        easycluster.remote_code module.

        @return: The result of the expression.
        '''
        return self.send_request(0, 'eval', (expr, 'eval'), {},
                                 nonblocking, oncomplete, onerror, threadid, origexc)

    def execblock(self, code, nonblocking=False, oncomplete=None, onerror=None, threadid=None, origexc=True):
        '''Run a block of code on the remote server. The code is executed in the
        context of the C{easycluster.remote_code} module.

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.

        @type  code: str
        @param code: The code to run, which will be executed in the context of the
        easycluster.remote_code module.

        @return: Whatever the code passes to L{exec_return}, or None if
        L{exec_return} is not called.
        '''
        return self.send_request(0, 'eval', (code, 'exec'), {},
                                 nonblocking, oncomplete, onerror, threadid, origexc)

    def import_modules(self, names, nonblocking=False, oncomplete=None, onerror=None, threadid=None, origexc=True):
        '''Imports one or more modules on the remote server.

        C{client.import_modules(["sys", "os"])} is equivalent to
        C{client.eval("import sys, os")}

        See L{Client.send_request} for the meaning of the C{nonblocking},
        C{oncomplete}, C{onerror}, C{threadid}, and C{origexc} arguments.

        @type  names: list:
        @param names: A list of modules to import.

        '''

        return self.send_request(0, 'import_modules', (names,), {},
                                 nonblocking, oncomplete, onerror, threadid, origexc)

    def import_module(self, name, nonblocking=False, oncomplete=None, onerror=None, threadid=None, origexc=True):
        '''Imports a module on the remote server. Equivalent to C{import_modules([name])}.'''

        return self.send_request(0, 'import_modules', ([name],), {},
                                 nonblocking, oncomplete, onerror, threadid, origexc)

    @property
    def server_version(self):
        '''Return the actual version of EasyCluster on the server.'''
        return self._peer_version

    def __getattr__(self, attr):
        '''Returns a proxy object to call a global function or class on the
        server. This lets you do things like:

        C{client.os.system("echo hello")}
        '''
        return _GlobalProxy(self, attr)

    def _persistent_id(self, obj):
        if isinstance(obj, RemoteProxy):
            if obj._connection is self:
                return str(obj._oid)
            raise TypeError('cannot send %r to remote connection %s' % (obj, self._peername))

    def _persistent_load(self, id):
        l = id.split('\n')
        oid = int(l[0])

        wrprox = self._proxy_by_id.get(oid)
        if wrprox is not None:
            prox = wrprox()
            if prox is not None:
                return prox

        proxclas = tid = typedat = None
        if len(l) > 1:
            tid = int(l[1])
            proxclas = self._proxy_type_by_id.get(tid)

            # Check if we have a type created for this object
            if proxclas is None and len(l) > 2:
                typedat = l[2]
                if typedat[0] == ':':
                    _, export_methods_text, export_attrs_text = typedat.split(':')

                    base_class = RemoteProxy
                    export_methods = []
                    export_attrs = []
                    export_attrs_cache = []

                    if export_methods_text:
                        export_methods = export_methods_text.split(',')

                    if export_attrs_text:
                        for attr in export_attrs_text.split(','):
                            if attr.startswith('!'):
                                export_attrs_cache.append(attr[1:])
                            elif attr == '@auto':
                                base_class = DefaultRemoteProxy
                            else:
                                export_attrs.append(attr)

                    typedict = {'__module__':__name__,
                                'proxy_methods': export_methods,
                                'proxy_attrs': export_attrs,
                                'proxy_attrs_cache': export_attrs_cache
                                }
                    proxclas = _RemoteProxyMeta('dynamic_proxy_' + '_'.join(export_methods + export_attrs + export_attrs_cache),
                                               (base_class,), typedict)

                else:
                    mod, cls = typedat.rsplit('.', 1)
                    try:
                        proxclas = getattr(_get_module(mod), cls)
                    except (ImportError, AttributeError):
                        traceback.print_exc()
                        proxclas = DefaultRemoteProxy
                self._proxy_type_by_id[tid] = proxclas

        prox = (proxclas or DefaultRemoteProxy)(self, oid)
        ref = _RemoteProxyRef(prox, self._proxy_deleted, oid)
        self._proxy_by_id[oid] = ref
        return prox

    def close(self, message='Connection closed'):
        '''Close the connection and invalidate all remote proxies.

        @type  message: str or L{RemoteException}
        @param message: Either a string or a L{RemoteException} instance to raise in all
        outstanding requests. If a string is given, then it will cause an IOError
        to be raised with the given message.
        '''
        Connection.close(self)
        proxies = self._proxy_by_id
        while proxies:
            oid, wrprox = proxies.popitem()
            prox = wrprox()
            if prox is not None:
                prox._connection = _dummy_connection

        ## Send an error to any outstanding requests
        if isinstance(message, RemoteException):
            error = message
        else:
            error = RemoteException(IOError(message), '')

        comp = self._completion
        while comp:
            rid, (oncomplete, onerr) = comp.popitem()
            try:
                if isinstance(onerr, tuple):
                    onerr[0](error, *onerr[1:])
                else:
                    onerr(error)
            except Exception:
                pass

        nbrs = self._nonblocking_responses
        while nbrs:
            rid, nbr = nbrs.popitem()
            nbr = nbr()
            if nbr:
                nbr.set_response(error)

class _ATCThread(threading.Thread):
    def __init__(self, atc):
        threading.Thread.__init__(self)
        self.atc = atc
        self.daemon = True

    def run(self):
        '''Read responses from the server.'''
        atc = self.atc
        next_wake_time = 0
        fd = atc.fileno()
        atc._got_keepalive()
        closeargs = ()
        atc.send_challenge()
        try:
            while True:
                ctime = time.time()
                timeout = atc._keep_alive_timeout
                if timeout is not None:
                    if ctime >= atc._last_keep_alive + timeout:
                        closeargs = ('Remote server not responding',)
                        return

                if ctime >= next_wake_time:
                    next_wake_time = ctime + 1
                    # Wake up any threads that are waiting so they can check if they've
                    # been interrupted.
                    with atc._response_lock:
                        atc._have_response.notify_all()
                    continue
                rd, _, _ = select.select([fd], (), (), next_wake_time - ctime)
                if rd:
                    if atc._read_data(False):
                        ## Check thread status after every valid message received
                        atc.check_threads()
        except (EnvironmentError, select.error) as e:
            closeargs = (e,)
            if e.args[0] != errno.ECONNRESET and e.args[0] != errno.EBADF:
                raise
        except EOFError:
            ## Swallow this error so it isn't printed. Since we call close(),
            ## any outstanding or future requests will fail.
            pass
        except Exception as e:
            closeargs = (e,)
            raise
        finally:
            atc.close(*closeargs)

class ThreadedClient(Client):
    '''A client that automatically creates unique threads on the server for each
    thread on the client that makes remote calls.

    Whenever a request is made from a thread on a client, a new thread is
    created on the server. All requests made from this client thread are
    processed by the same thread on the server. If the client thread exits, the
    server thread will be stopped once check_threads() is called. By default,
    threads are checked whenever a response is received.

    This class creates a new thread on the client to process responses. Completion
    functions will be called in the context of this thread. read_response() must not be
    called. This class is also incompatible with ClientGroup.
    '''

    def __init__(self, key=None, host=None, port=None,
                 definitions='easycluster.remote_code',
                 enable_compression=False, ssh=False, user=None, rpython=None, extra_args=(),
                 keep_alive_interval=10,
                 keep_alive_timeout=60):
        '''Creates a new ThreadedClient. Arguments are the same as L{Client}.'''


        ## use pseudo-thread IDs instead of sending real ones
        self._next_thread_id = 1
        self._id_by_thread = {}
        self._response_lock = threading.Lock()
        self._have_response = threading.Condition(self._response_lock)
        self._keep_alive_interval = keep_alive_interval
        self._keep_alive_timeout = keep_alive_timeout
        self._last_keep_alive = None
        self._wrthread = None

        Client.__init__(self, key, host, port, definitions, enable_compression,
        ssh, user, rpython, extra_args)

        self._init_data['keep_alive_interval'] = keep_alive_interval

    def _init_thread(self):
        thread = _ATCThread(self)
        self._wrthread = weakref.ref(thread)
        thread.start()

    def _got_keepalive(self):
        self._last_keep_alive = time.time()

    def check_threads(self):
        '''Check for threads that have exited, and kill the
        corresponding threads on the server.'''
        done = []
        with self._lock:
            if not self._is_ready:
                return
            for t, id in list(self._id_by_thread.items()):
                if not t.is_alive():
                    done.append(id)
                    del self._id_by_thread[t]
        for id in done:
            self.stop_remote_thread(id)


    def read_response(self, *args):
        '''Do not call this method on ThreadedClient.'''
        raise TypeError('read_response should not be called on ThreadedClient objects')

    ## called with lock held
    def _thread_id(self):
        ct = threading.current_thread()
        tid = self._id_by_thread.get(ct)
        if tid is None:
            tid = self._next_thread_id
            self._next_thread_id = tid + 1
            self._id_by_thread[ct] = tid
        return tid

    def _set_nbr_response(self, nbr, response):
        with self._response_lock:
            nbr.set_response(response)
            self._have_response.notify_all()

    def _add_pending_response(self, rid, response):
        with self._response_lock:
            self._pending_responses[rid] = response
            self._have_response.notify_all()

    def _wait_for_response(self, nbr):
        '''Wait for a response to complete. This method is normally not called
        directly.
        '''
        with self._response_lock:
            while not nbr._have_response:
                self._have_response.wait()

    def close(self, *a):
        '''Close the connection and stop the processing thread.'''
        # It's possible that this function could be called recursively, so test
        # if sock is None before we grab the lock.
        if self._sock is None:
            return

        try:
            thread = self._wrthread()
        except TypeError:
            # 'NoneType' is not callable.
            thread = None

        ## This will shut down the socket and cause the reading thread to exit
        ## cleanly.
        with self._response_lock:
            Client.close(self, *a)
            self._have_response.notify_all()

        if thread and thread != threading.current_thread():
            thread.join()

class ClientGroup:
    '''Represents a set of Client objects that can be queried as a group.'''

    def __init__(self, clients=()):
        '''Create a new ClientGroup object. C{clients} is an optional sequence of
        L{Client} instances to add to the group.'''
        self.clients = {}
        self.epoll = (epoll() if epoll is not None else None)
        for c in clients:
            self.add_client(c)

    def add_client(self, cl):
        '''Add a L{Client} instance to the group. Does nothing if the client is already registered.'''
        fd = cl.fileno()
        mycl = self.clients.get(fd)
        if cl is mycl:
            return

        if mycl and self.epoll:
            self.epoll.unregister(fd)

        self.clients[fd] = cl
        if self.epoll:
            self.epoll.register(fd, select.POLLIN|select.POLLERR|select.POLLHUP)

    def remove_client(self, cl):
        '''Remove a L{Client} instance from the group. Does nothing if the client is not registered.'''
        fd = cl.fileno()
        mycl = self.clients.get(fd)
        if cl is mycl:
            del self.clients[fd]
            if self.epoll:
                self.epoll.unregister(fd)

    def read_responses(self, timeout=None, max=-1):
        '''Read responses from the L{Client} objects in the group.'''
        etime = (None if timeout is None else time.time() + timeout)
        while max:
            rtime = (1000.0 if etime is None else etime - time.time())
            if rtime < 0:
                rtime = 0
            if self.epoll:
                evts = self.epoll.poll(rtime, len(self.clients))
                if not evts and not rtime:
                    return
                for fd, evt in evts:
                    if self.clients[fd].read_response(False):
                        if max > 0:
                            max -= 1
                            if max == 0:
                                return

            else:
                r, _, _ = select.select(self.clients.values(), (), (), rtime)
                if not r and not rtime:
                    return
                for client in r:
                    if client.read_response(False):
                        if max > 0:
                            max -= 1
                            if max == 0:
                                return

## Backwards-compatible alias
AutoThreadingClient = ThreadedClient

def exec_return(rval):
    '''When called from within code sent to L{Client.execblock}, causes eval to return C{rval}.'''
    raise _ExecReturn(rval)

def definitions_module(name, keep_source=True):
    '''Get or create a module to store common definitions in.

    @type  name: str
    @param name: The name if the virtual module to create. If the module is in a
    package, then that package must already exist.

    @rtype:  module
    @return: The new virtual module.
    '''

    mod = sys.modules.get(name)
    if mod is not None:
        try:
            mod._source_code
        except AttributeError:
            raise ImportError('%s already exists, but is not a dynamic module' % name)
        return mod

    mod = ModuleType(name, 'EasyCluster common definitions')

    components = name.rsplit('.', 1)
    if len(components) > 1:
        parent_package_name = components[0]
        try:
            parent_package = _get_module(parent_package_name)
        except (ImportError, AttributeError):
            raise ImportError('Cannot import parent package %r: '
                              'Definitions module must be top-level, '
                              'or in an existing package' % parent_package_name)
        if hasattr(parent_package, components[1]):
            raise ImportError('Cannot overwrite non-module value %r with virtual module' % name)

        setattr(parent_package, components[1], mod)

    sys.modules[name] = mod
    mod._source_code = source = []
    def define(code, local=True):
        if not code.endswith('\n'):
            code += '\n'
        cb = compile(code, '<easycluster definitions %r>' % name, 'exec', dont_inherit=True)
        if local:
            eval(cb, mod.__dict__)
        if keep_source:
            source.append(code)

    mod.define = define
    define.__module__ = name
    define('import easycluster\nfrom easycluster import *\n')
    del source[:]
    return mod

def define_common(code, name='easycluster.remote_code', local=True):
    '''Define common classes in the specified module. Equivalent to:
    C{definitions_module(name).define(code, local)}

    @type  code: str
    @param code: The code to evaluate in the context of the module.

    @type  name: str
    @param name: The name if the virtual module to create. If the module is in a
    package, then that package must already exist.

    @type  local: bool
    @param local: If True (default), the code will also be evaluated on the
    client so that things like proxy class definitions will be available.
    '''
    definitions_module(name).define(code, local)

def decode_key(key):
    '''If C{key} is a hex-encoded string of the proper size, returns the actual key,
    otherwise returns a hash of the original string.'''
    try:
        if len(key) == 2*HMAC_SIZE:
            return _hexdec(key)
    except Exception:
        pass
    return HMAC_MOD(_str_to_bytes(key)).digest()

def read_key_file(path):
    '''Read an HMAC key from a file.'''
    with open(path, 'r') as fp:
        return decode_key(fp.readline().rstrip('\r\n'))

def write_key_file(path, key, overwrite=False):
    '''Write an HMAC key to a file. If C{overwrite} is True, it will try to
    overwrite the key file if it already exists.'''
    if not _write_key_file(path, key):
        if not overwrite:
            return False
        os.unlink(path)
        return _write_key_file(path, key)
    return True

def generate_key():
    '''Generates a random HMAC key of the proper size.'''
    return os.urandom(HMAC_SIZE)


def add_key_options(options, key_option='-K', keyfile_option='-k'):
    '''Add options for specifying a HMAC key or keyfile to an L{optparse.OptionParser}.'''
    options.add_option(key_option, '--key', help='HMAC key to use; either a %d-character hex string '
                       'or a ASCII string which will be padded. This method of specifying a key '
                       'is insecure because other users on the system can read it.' % (2*HMAC_SIZE))
    options.add_option(keyfile_option, '--keyfile', metavar='FILE', help='Read HMAC key from file. This '
                       'is the preferred method of specifying a key.')

def key_from_options(opts, warn=True):
    '''Get an HMAC key from an options instance.

    Example:

     >>> options = optparse.OptionParser()
     >>> easycluster.add_key_options(options)
     >>> opts, args = options.parse_args()
     >>> key = easycluster.key_from_options(opts)
     >>>
    '''
    key = b''
    if opts.keyfile:
        key = read_key_file(opts.keyfile)
    elif opts.key:
        if warn:
            print('SECURITY WARNING: using key from command line.', file=sys.stderr)
        key = decode_key(opts.key)
    return key

def parse_connection_spec(spec, default_port=None, default_key=b'',
                          default_enable_compression=False, custom_options=(),
                          warn=True):
    '''
    Parse connection parameters from a string. This is useful if
    you need to provide options to connect to more than one server.

    The connection spec looks like this::

        [user@]host[:port][:opt=val]...

    The 'host' can be a hostname, IPv4 address, or bracketed IPv6 address. If
    'port' is specified, it overrides the C{default_port} parameter.

    The key is determined by specifying either the 'kf' or 'key' options. If
    'key' is specified and 'warn' is True, a warning will be printed to
    STDERR. If the connection spec comes does not come from the command line or
    an environment variable, it's safe to set 'warn' to False. If no key is
    specified, 'default_key' is used.

    If ':compress=1' is specified, then compression is enabled for the connection.

    Example connection specifications::

        'example.com'                        # Bare host name; default port, default key
        '192.0.2.1:9999'                     # IPv4 address on non-standard port
        '[2001:db8::2]'                      # IPv6 addresses must be in brackets
        'example.com:kf=secret.key'          # Using a key from a file
        'example.com:9999:key=s3cret'        # Using a key directly, with non-standard port
        'user@example.com'                   # Using SSH
        'example.com:ssh=/usr/local/bin/ssh' # Using a custom SSH path

    Example:

     >>> spec = 'example.com:1234:kf=secret.key'
     >>> easycluster.parse_connection_spec(spec)
     {'host': 'example.com', 'port': 1234, 'key': '...'}
     >>>
     >>> spec = 'example.com:1234:kf=secret.key:foo=bar'

    @type  spec: str
    @param spec: The connection string

    @type  default_port: int
    @param default_port: Default port to connect to, if not specified in C{spec}

    @type  default_key: bytes
    @param default_key: The default key to use if none is specified in C{spec}

    @type  default_enable_compression: bool
    @param default_enable_compression: Whether or not to enable compression by
    default.

    @type  custom_options: list or bool
    @param custom_options: List of custom options to accept, or True to accept
    all custom options. If specified, then C{parse_connection_spec} returns two
    dictionaries instead of one.

    @type  warn: bool
    @param warn: If True, then a warning will be printed to STDERR if a key is
    given directly instead of using a keyfile.

    @return: A dictionary of parameters which can be passed to the Client or
    ThreadedClient constructors:

     >>> params = easycluster.parse_connection_spec(sys.argv[1])
     >>> client = easycluster.Client(**params)

    If 'custom_options' is specified, two dictionaries are returned instead of
    one:

     >>> params, custom = easycluster.parse_connection_spec(spec, custom_options=['foo'])
     >>> params
     {'host': 'example.com', 'port': 1234, 'key': '...'}
     >>> custom
     {'foo': 'bar'}

    @raise ValueError: If any option is duplicated, or options are malformed.

    @raise IOError: If a keyfile is specified, but can't be opened.
    '''

    # Extract the host. Process a bracketed IPv6 address if it exists.
    m = re.match(r'\[([0-9a-fA-F:]+)\]:(.*)', spec)
    if m:
        host = m.group(1)
        rest = m.group(2)
    else:
        host, _, rest = spec.partition(':')

    # If the first value is a port number, parse it.
    lst = rest.split(':')
    if re.match(r'^\d+$', lst[0]):
        port = int(lst.pop(0))
    else:
        port = default_port

    user = None
    ssh = False
    if '@' in host:
        ssh = True
        user, _, host = host.partition('@')

    params = {'host': host, 'port': port, 'key': default_key, 'ssh': ssh,
              'user': user, 'enable_compression': default_enable_compression}
    new_params = {}

    key = None
    compress = None
    custom = {}
    try:
        for option in lst:
            if not option:
                continue
            name, sep, val = option.partition('=')
            if not sep:
                raise ValueError('Malformed option %r' % (option))
            isparam = False
            if name == 'kf' or name == 'keyfile' or name == 'key':
                isparam = True
                if 'key' not in new_params:
                    if name == 'key':
                        if warn:
                            print('SECURITY WARNING: using key from command line.', file=sys.stderr)
                        val = decode_key(val)
                    else:
                        val = read_key_file(val)
                name = 'key'
            elif name == 'compress':
                isparam = True
                name = 'enable_compression'
                val = bool(val == '1')
            elif name == 'ssh':
                isparam = True
                if val in ('1', 'yes', 'on'):
                    val = True
                elif val in ('0', 'no', 'off'):
                    val = False
            elif name == 'user':
                isparam = True
            elif name == 'extra':
                name = 'extra_args'
                isparam = True
                val = shlex.split(val)
            elif name == 'rpython':
                isparam = True

            if isparam:
                cdict = new_params
            elif custom_options is True or name in custom_options:
                cdict = custom
            else:
                raise ValueError('Unknown option %r' % (name))

            if name in cdict:
                raise ValueError('Duplicate option %r' % (option))
            cdict[name] = val
    except ValueError as e:
        raise ValueError(str(e) + ' (in connection spec %r)' % spec)

    params.update(new_params)

    if custom_options:
        return params, custom
    else:
        return params

def _get_upgrade_code():
    global _compcode
    try:
        return _compcode
    except NameError:
        pass

    coref = os.path.splitext(__file__)[0] + '.py'
    svrf = os.path.join(os.path.dirname(coref), 'server.py')
    coretxt, svrtxt, = [zlib.compress(open(f, 'rb').read(), 9) for f in (coref, svrf)]
    _compcode = coretxt, svrtxt

    return _compcode

def _get_global_root(mod, attr):
    try:
        return getattr(mod, attr)
    except AttributeError:
        return getattr(builtins, attr)

def _try_import(mod, name, is_root):
    newname = (name if is_root else mod.__name__ + '.' + name)
    try:
        newmod = __import__(newname)
    except ImportError:
        return None

    if is_root:
        if mod is not builtins:
            setattr(mod, name, newmod)
        val = newmod
    else:
        val = getattr(mod, name)

    return val

def get_global(name, context=None, auto_import=False):
    """
    Get a global variable in the context of the given module. If C{name} contains
    periods, it will call getattr() to resolve the actual value of the
    object.

    @type  name: str
    @param name: The absolute or relative name of the global to get.

    @type  context: ModuleType
    @param context: The module that the name should be resolved against. If not
    specified, the name must either be absolute, or the name of a built-in
    function or type.

    @type  auto_import: bool
    @param auto_import: If and accessing a value from a module fails, the module
    will be imported. If a C{context} module is specified, the resulting
    imported module will be exposed to that module. For example, if C{testmod}
    is a module, then running C{get_global('os.path.join', testmod, True)} will
    set C{os} in C{testmod} just as if testmod contained C{import os.path}.

    @rtype:  object
    @return: The value of the global variable.
    """

    components = name.split('.')
    if context is None:
        val = builtins
        _getattr = getattr
    else:
        val = context
        _getattr = _get_global_root

    for i, name in enumerate(components):
        try:
            val = _getattr(val, name)
        except AttributeError:
            if auto_import and isinstance(val, ModuleType):
                val = _try_import(val, name, i == 0)
                if val is None:
                    raise
            else:
                raise
        _getattr = getattr

    return val

def set_global(name, value, context=None):
    """
    Set a global variable in the context of the given module. If C{name}
    contains periods, it will call getattr() to resolve the actual value of the
    object on which to set the attribute.

    @type  name: str
    @param name: The absolute or relative name of the global to set.

    @type  value: object
    @param value: The value to put in the global.

    @type  context: ModuleType
    @param context: The module
    If `auto_import` is true, and accessing a value from a module fails, it will
    attempt to import the module and retry the access.
    """

    components = name.split('.')
    if context is None:
        context = builtins

    if len(components) == 1:
        if context is builtins:
            raise TypeError('Cannot set non-absolute global without context module')
        setattr(context, name, value)
    else:
        gv = get_global('.'.join(components[:-1]), context)
        setattr(gv, components[-1], value)

def _ss(ccode):
    '''SSH bootstrap function'''
    global _compcode
    _compcode = ccode
    from easycluster import server
    # Don't want scripts writing shit to stdout and corrupting the stream
    wfd = os.dup(1)
    rfd = os.dup(0)
    nullf = os.open(os.devnull, os.O_RDWR)
    os.dup2(nullf, 0)
    os.dup2(nullf, 1)
    os.close(nullf)

    sys.stdout = sys.stderr
    peer = ':'.join(os.getenv('SSH_CONNECTION').split()[:2])
    sock = PipeSocket(None, rfd, wfd)
    svr = server.Server(None, sock, peer, verbosity=0)
    while svr:
        svr = svr.run()

if PYTHON3:
    _ssh_default_python = 'python3'
    _ssh_python_args = " -u -c 'exec(eval(input())) # easycluster'"
else:
    _ssh_default_python = 'python'
    _ssh_python_args = " -u -c 'exec input() # easycluster'"

_ssh_bootstrap = r'''
import sys,os
if sys.version_info < (2, 6):
 print('v=%%rXEC'%%sys.version)
 sys.exit(0)
import zlib,types
def r(n,a):
 sys.modules[n]=m=types.ModuleType(n)
 r=bytearray()
 while a > 0:
  t = os.read(0, a)
  if not t:
   break
  a -= len(t)
  r.extend(t)
 r=bytes(r)
 eval(compile(zlib.decompress(r),n,'exec'),m.__dict__)
 return m,r
print('YEC')
e,c=r('easycluster',%d)
e.server,s=r('easycluster.server',%d)
e._ss((c,s))
''' # '''

def _prepare_ssh(ssh_args):
    coredata, svrdata = _get_upgrade_code()
    bootstrap = repr(_ssh_bootstrap % (len(coredata), len(svrdata))) + '\n'
    proc = subprocess.Popen(ssh_args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    sock = PipeSocket(proc)
    sock.sendall(_str_to_bytes(bootstrap))
    data = bytearray()
    while not data.endswith(b'EC\n'):
        r = sock.recv(16)
        if not r:
            raise EOFError('Failed to read signature from remote SSH bootstrap')
        data.extend(r)
    if data.endswith(b'XEC\n'):
        m = re.search('v=(.*)XEC', data.decode('utf-8', 'ignore'))
        rvers = 'Unknown'
        if m:
            rvers = m.group(1)
        raise ValueError('Remote version of Python too old: %s' % rvers)
    sock.sendall(coredata)
    sock.sendall(svrdata)
    return sock

#def _connect_ssh(host, port=None, user=None, ssh='ssh', extra_args=()):

###############################
# Internal classes
###############################

class GeneratorProxy(SelfIterProxy):
    """A proxy class for generator objects."""
    proxy_methods = 'send', 'throw', 'close'

    def __iter__(self):
        return self

class FileProxy(RemoteProxy):
    """A proxy class for files and file-like objects."""
    proxy_methods = ('close',  'errors', 'fileno', 'flush', 'isatty', 'next', 'read',
                     'readinto', 'readline', 'readlines', 'seek', 'tell', 'truncate',
                     'write', 'writelines', 'xreadlines')
    proxy_attrs = ('closed', 'encoding', 'errors', 'mode', 'name', 'newlines')

class _ExecReturn(BaseException):
    def __init__(self, val):
        self.val = val

class PipeSocket:
    def __init__(self, proc, rfd=None, wfd=None, peername=None):
        self._proc = proc
        if rfd is None:
            rfd = proc.stdout.fileno()
            wfd = proc.stdin.fileno()
        self._rfd = rfd
        self._wfd = wfd
        self._peername = peername

        #detect fork
        self._origpid = os.getpid()

    def fileno(self):
        return self._rfd

    def write_fileno(self):
        return self._wfd

    def recv(self, amt):
        return os.read(self._rfd, amt)

    def send(self, data):
        return os.write(self._wfd, data)

    def sendall(self, data):
        while data:
            w = os.write(self._wfd, data)
            data = data[w:]

    def close(self):
        try:
            if self._proc is not None:
                if self._origpid == os.getpid():
                    self._proc.terminate()
                    self._proc.wait()
                self._proc.stdin.close()
                self._proc.stdout.close()
                self._proc = None
                self._rfd = None
                self._wfd = None
                return
        except EnvironmentError:
            pass

        try:
            if self._rfd is not None:
                os.close(self._rfd)
                os.close(self._wfd)
                self._rfd = self._wfd = None
        except EnvironmentError:
            pass


    def shutdown(self, type):
        self.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def setblocking(self, block):
        for fd in (self._rfd, self._wfd):
            flags = fcntl.fcntl(fd, fcntl.F_GETFL) & ~os.O_NONBLOCK
            if not block:
                flags |= os.O_NONBLOCK
            fcntl.fcntl(fd, fcntl.F_SETFL, flags)

    def getpeername(self):
        return self._peername

###############################
# Internal functions
###############################

def _get_typedat(obj, typ):
    '''Returns the saved type data for object C{obj} of type C{typ}.'''
    sdat = _singletons.get(id(obj))
    if sdat is not None:
        typedat, wr, sobj = sdat
        if sobj is not None or (wr is not None and wr() is obj):
            return typedat

    typedat = getattr(typ, '_easycluster_server_object_typedat', None)
    if type(typedat) == _TypeData:
        if typedat == '':
            typedat = _make_typedat(
                typ, typ.export_methods, typ.export_attrs,
                typ.export_attrs_cache, typ.proxy_class)
            typ._easycluster_server_object_typedat = typedat
        return typedat

    ebc = _extra_base_classes.get
    for b in getattr(typ, '__mro__', ()):
        r = ebc(b)
        if r:
            return r
    return None

def _fill_old_style_mro(typ, mro):
    if typ not in mro:
        mro.append(typ)
    for b in typ.__bases__:
        _fill_old_style_mro(b, mro)

def _class_mro(typ):
    mro = getattr(typ, '__mro__', None)
    if mro is not None:
        return mro[:-1]
    mro = []
    _fill_old_style_mro(typ, mro)
    return mro

def _make_typedat(typ, export_methods, export_attrs, export_attrs_cache, proxy_class):
    '''
    Generate a type data string for the given set of exported methods and
    attributes or proxy class.
    '''
    if isinstance(export_methods, str):
        export_methods = (export_methods,)
    if isinstance(export_attrs, str):
        export_attrs = (export_attrs,)
    if isinstance(export_attrs_cache, str):
        export_attrs_cache = (export_attrs_cache,)

    if proxy_class:
        return _TypeData(proxy_class.__module__ + '.' + proxy_class.__name__)
    else:
        if '@auto' in export_methods:
            export_methods = set(export_methods)
            export_methods.discard('@auto')
            attrs = {}
            for cls in _class_mro(typ):
                if cls is not object:
                    attrs.update(cls.__dict__)

            # Built-in slot methods have a type of <type 'wrapper_descriptor'>
            # that does not have a name exported in the types module.
            functypes = (FunctionType, BuiltinFunctionType, staticmethod,
                         classmethod, type(FunctionType.__dict__['__call__']))
            export_methods.update(name for name, val in attrs.items()
                                  if (name not in _forbidden_slots and
                                      isinstance(val, functypes)))

        export_attrs = set(export_attrs or ())
        for cattr in (export_attrs_cache or ()):
            export_attrs.discard(cattr)
            export_attrs.add('!' + cattr)

        return _TypeData(':' + ','.join(sorted(export_methods or ())) + ':' + ','.join(sorted(export_attrs)))

def _get_module(name):
    '''Imports and returns a module object.'''
    components = name.split('.')
    mod = __import__(name)
    for c in components[1:]:
        mod = getattr(mod, c)
    return mod

def _get_peer_name(addr):
    if isinstance(addr, tuple):
        host, port = addr[:2]
        ## When listening on a dual-stack socket, IPv4 addresses
        ## are embedded within IPv6 addresses.
        if host.startswith('::ffff:'):
            host = host[7:]
        ## Standard convention for IPv6 addresses is to surround
        ## them with brackets when used with a port number.
        if ':' in host:
            host = '[%s]' % host
        return '%s:%d' % (host, port)
    return addr

def _sock_sendall(sock, data):
    '''Send all of C{data} over C{sock}, blocking until the send is complete'''
    while data:
        try:
            numsent = sock.send(data)
            data = data[numsent:]
        except (socket.error, OSError) as e:
            if e.errno not in _nonblocking_errors:
                raise
            select.select([], [sock], [], None)

def _get_special_keywords(kwargs):
    '''Returns the values of the keywords nonblocking, oncomplete, onerror, and threadid.'''

    nonblocking = kwargs.pop('nonblocking', False)
    oncomplete = kwargs.pop('oncomplete', None)
    onerror = kwargs.pop('onerror', None)
    threadid = kwargs.pop('threadid', None)
    origexc = kwargs.pop('origexc', True)
    return nonblocking, oncomplete, onerror, threadid, origexc

def _add_extra_classes():
    make_server_class(GeneratorType, proxy_class=GeneratorProxy)
    make_server_class(IOBase, proxy_class=FileProxy)
    try:
        make_server_class(file, proxy_class=FileProxy)
    except NameError:
        pass

    try:
        import _io
        make_server_class(_io._IOBase, proxy_class=FileProxy)
        del _io
    except (NameError, ImportError):
        pass

    # Proxy module objects.
    make_server_class(ModuleType)

_add_extra_classes()
del _add_extra_classes

def _vers_tuple(vers):
    return tuple(int(v) for v in vers.split('.'))

def _version_compare(va, vb):
    va = _vers_tuple(va)
    vb = _vers_tuple(vb)
    if va < vb:
        return -1
    if va > vb:
        return 1
    return 0

if sys.platform.startswith('win'):
    from ctypes import windll, WinError, wintypes
    kernel32 = windll.kernel32
    SetHandleInformation = kernel32.SetHandleInformation
    SetHandleInformation.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD]

    def _write_key_file(path, key):
        '''Write an HMAC key to a file. Returns True if the file was created, or
        False if it already exists.'''
        import win32api, win32file, win32security
        import ntsecuritycon, win32con, pywintypes

        dacl = win32security.ACL()

        user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName())
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION,
                                 ntsecuritycon.FILE_ALL_ACCESS, user)

        try:
            user, domain, type = win32security.LookupAccountName ("", 'SYSTEM')
            dacl.AddAccessAllowedAce(win32security.ACL_REVISION,
                                 ntsecuritycon.FILE_ALL_ACCESS, user)
        except pywintypes.error:
            pass

        sd = win32security.SECURITY_DESCRIPTOR()
        sd.SetSecurityDescriptorDacl(1, dacl, 0)

        sa = win32security.SECURITY_ATTRIBUTES()
        sa.SECURITY_DESCRIPTOR = sd
        sa.bInheritHandle = 0

        try:
            fil = win32file.CreateFile(path, win32con.GENERIC_WRITE, 0, sa,
                                       win32con.CREATE_NEW, 0, 0)
        except pywintypes.error as e:
            ## File exists.
            if e.args[0] == 80:
                return False
        try:
            win32file.WriteFile(fil, _str_to_bytes(_hexenc(key) + '\r\n'), None)
        finally:
            win32file.CloseHandle(fil)
        return True

    def _mark_non_inheritable(fd):
        """Mark the given handle as non-inheritable."""
        if not SetHandleInformation(fd, 1, 0):
            raise WinError()
else:

    def _mark_non_inheritable(fd):
        fcntl.fcntl(fd, fcntl.F_SETFD, fcntl.fcntl(fd, fcntl.F_GETFD, 0) | fcntl.FD_CLOEXEC)

    def _write_key_file(path, key):
        '''Write an HMAC key to a file. Returns True if the file was created, or
        False if it already exists.'''
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except OSError as e:
            if e.args[0] == errno.EEXIST:
                return False
            raise

        try:
            os.write(fd, _str_to_bytes(_hexenc(key) + '\n'))
        finally:
            os.close(fd)
        return True
