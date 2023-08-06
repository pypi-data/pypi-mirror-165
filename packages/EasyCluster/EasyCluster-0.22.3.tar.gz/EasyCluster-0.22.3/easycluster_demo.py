#!/usr/bin/python3

import sys
import easycluster
import traceback
import threading
import time
from optparse import OptionParser
from easycluster.server import server_check_runner, spawn_local

rcode = '''\
from __future__ import print_function
#'

import time
class TestObject(ServerObject):
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def setval(self, val):
        print('TestObject %s: setval %s -> %s' % (self.name, self.val, val))
        self.val = val

    def getval(self):
        return self.val

    def __del__(self):
        print('TestObject %s: deleted' % self.name)

class TestObject2(ServerObject):
    export_methods = '__add__', 'set_val'
    export_attrs_cache = 'val',

    def __init__(self, val):
        self.val = val

    def __add__(self, o):
        oval = o.val
        rval = self.val + oval
        print('Testobject __add__: %s + %s = %s' % (self.val, oval, rval))
        return TestObject2(rval)

    def set_val(self, val):
        self.val = val

class TestOldStyleClass:
    def __init__(self, val):
        self.val = val

    def testmeth(self):
        print('old-style class, val = %s' % self.val)

make_server_class(TestOldStyleClass, ['testmeth'], ['val'])

class TestObject3Proxy(RemoteProxy):
    proxy_methods = 'rmethod',
    proxy_attrs = 'val',

    def lmethod(self):
        print('TestObject3Proxy intercepting call to lmethod: self.val = %s, self.rmethod() = %s' % (self.val, self.rmethod()))
        return self.raw_call_method('lmethod', (), {})

class TestObject3(ServerObject):
    proxy_class = TestObject3Proxy

    def __init__(self, val):
        self.val = val

    def lmethod(self):
        print('TestObject3 running lmethod: self.val = %s, self.rmethod() = %s' % (self.val, self.rmethod()))

    def rmethod(self):
        rval = self.val + 100
        print('TestObject3 running rmethod: self.val = %s (returning %s)' % (self.val, rval))
        return rval


    def __add__(self, o):
        oval = o.val
        rval = self.val + oval
        print('Testobject __add__: %s + %s = %s' % (self.val, oval, rval))
        return TestObject3(rval)

class TestDefaultProxy(DefaultRemoteProxy):
    pass

class TestObject4(ServerObject):
    proxy_class = TestDefaultProxy

    def __init__(self, a):
        self.a = a

    def instmethod(self):
        return self.a

    @classmethod
    def cmethod(cls):
        return cls.__name__

    @staticmethod
    def smethod():
        return 'static'

testobjects = [TestObject('s%d' % i, i) for i in range(3)]

def test_generator_func():
    print('generator func called...')
    yield 1
    print('generator func resumed (1)...')
    yield 2
    print('generator func resumed (2)...')
    yield 3
    print('generator func resumed (3)...')

## Make sure that RemoteProxy objects are converted to
## the objects they refer to
def check_test_objects(lst):
    for a, b in zip(lst, testobjects):
        assert a is b, "objects are not same reference"

## Test exceptions and traceback
def te1(a):
    raise ValueError('foo')

def te2(b):
    te1(b)

testlst = []

make_singleton(testlst)

def get_test_list():
    return testlst

def print_test_list():
    print('testlst = %r' % testlst)

def dosleep(s):
    print('sleeping %s' % s)
    time.sleep(s)
    print('done')
    return time.time()

''' # '''

easycluster.define_common(rcode)

tests = []
def define_test(name, rpt=False):
    def r(f):
        tests.append((name, f, rpt))
        return f
    return r

@define_test('Connect')
def connect():
    global l1
    l1 = easycluster.Client(**conn_params)

@define_test('Test eval')
def eval():
    print('eval returned %s' % l1.eval('2 + 2'))

@define_test('Test execblock')
def execblock():
    print('exec returned %s' % l1.execblock('assert 2 + 2 == 4; exec_return(5)'))

@define_test('Test exceptions')
def exceptions():
    print(r'\/\/\/ Exception reports expected below \/\/\/', file=sys.stderr)

    try:
        ## Will throw the original exception (ValueError)
        ## and print the traceback to stderr.
        l1.te2(3)
    except Exception as e:
        traceback.print_exc()

    try:
        ## Have the object throw a RemoteException instead of
        ## the original exception. This will not print the
        ## trace
        l1.te2(3, origexc=False)
    except easycluster.RemoteException as e:
        print('Remote exception, traceback:', file=sys.stderr)
        print(''.join(e.text), file=sys.stderr)
    print('/\\/\\/\\ End of exceptions test /\\/\\/\\', file=sys.stderr)

@define_test('Test references')
def reftest():
    objects = l1.testobjects.value

    ## Check references on the server
    l1.check_test_objects(objects)

    otherobjects = l1.testobjects.value
    ## Make sure that each remote object is converted into the
    ## same proxy object every time it is returned.
    for a, b in zip(objects, otherobjects):
        assert a is b, 'proxy objects are not the same'

    for a in objects:
        assert type(a) is type(objects[0])

    print('Server-created object values: %r' % [o.getval() for o in objects])

@define_test('Test method calls')
def methods():
    global obj1
    # Create a new object
    obj1 = l1.TestObject('c1', 100)
    obj1.setval(101)
    obj1.setval(102)
    ## Implicitly removes reference to Testobject('c1').
    ## This object will be deleted the next time any
    ## request is made to the server.
    obj1 = l1.TestObject('c2', 200)
    obj1.setval(201)
    obj1.setval(203)

@define_test('Test attribute access')
def attrs():
    print('test attr access: obj1.val = %d' % obj1.val)
    obj1.val = 150
    print('obj1.getval() = %d' % obj1.getval())
    obj1.newval = 1234
    obj1.raw_set_attribute('newval2', 9999)
    d = obj1.raw_get_attribute('__dict__')
    print('remote __dict__ = %r' % d)
    assert d.get('newval') == 1234
    assert d.get('newval2') == 9999
    del obj1.newval
    d = obj1.raw_get_attribute('__dict__')
    print('remote __dict__ = %r' % d)
    assert 'newval' not in d
    assert d.get('newval2') == 9999

@define_test('Test operator overloading (via exported methods)')
def overload():
    a = l1.TestObject2(3)
    b = l1.TestObject2(4)
    c = a + b
    print('final value = %s' % c.val)

@define_test('Test client-side attribute caching')
def test_cache():
    a = l1.TestObject2(3)
    print('initial value = %s' % a.val)
    a.set_val(4)
    assert a.val == 3

@define_test('Test custom proxy classes')
def custom_proxy():
    from easycluster.remote_code import TestObject3Proxy
    a = l1.TestObject3(3)
    print('proxy class = %r' % type(a))
    assert isinstance(a, TestObject3Proxy)
    a.lmethod()

@define_test('Test default proxy class')
def custom_proxy():
    a = l1.TestObject4(123)
    assert a.instmethod() == 123
    assert a.a == 123
    a.a = 1234
    assert a.instmethod() == 1234
    assert a.a == 1234
    assert a.raw_get_attribute('__dict__')['a'] == 1234

    assert a.cmethod() == 'TestObject4'
    assert a.smethod() == 'static'

@define_test('Test old-style classes')
def old():
    obj1 = l1.TestOldStyleClass(300)
    print('osc.val = %d' % obj1.val)
    obj1.testmeth()

@define_test('Test generator')
def gen():
    obj1 = l1.call('test_generator_func')
    print('values = %r' % list(obj1))

@define_test('Test RemoteFile class')
def rfile():
    obj1 = l1.open('test.txt', 'w')
    print('foo', 'bar', file=obj1)
    obj1.close()

@define_test('Test singleton')
def singleton():
    ## Test singleton objects. Run twice to make sure that
    ## singletons stay on server.
    for i in (0, 1):
        lst = l1.call('get_test_list')
        lst.append(3)
        lst.append(4)
        lst = None
        l1.call('print_test_list')

@define_test('Test reconnect')
def reconnect_test():
    t1 = l1.TestObject('rc1', 100)
    assert t1.proxy_connection is l1
    print('t1.value is %d' % t1.getval())
    l1.reconnect()
    assert t1.proxy_connection is None
    try:
        t1.getval()
    except IOError:
        pass
    else:
        assert False, "IOError not raised for stale object"

def do_wait_multi(rsp):
    cg = easycluster.ClientGroup()
    for i, r in enumerate(rsp):
        r.num = i
        cg.add_client(r.client)
    rsp = set(rsp)
    while rsp:
        cg.read_responses(max=1)
        for r in list(rsp):
            if r.have_response:
                print('response from %d: %r' % (r.num, r.wait()))
                rsp.discard(r)

@define_test('Test server multithreading')
def svr_thread1():
    do_wait_multi([l1.dosleep(0.3 - (i*0.1), nonblocking=True, threadid=i + 1)
                   for i in (0, 1)])
    l1.stop_remote_thread(1)
    l1.stop_remote_thread(2)

@define_test('Test server multithreading (single)')
def svr_thread2():
    do_wait_multi([l1.dosleep(0.3 - (i*0.1), nonblocking=True, threadid=easycluster.SINGLE)
                   for i in (0, 1)])


@define_test('Connect again')
def parallel_connect():
    global l2
    ## Create another connection, then call a function on both
    ## in parallel.
    l2 = easycluster.Client(**conn_params)

@define_test('Test call_multi')
def parallel():
    print(easycluster.call_multi([l1, l2], 'dosleep', 0.2))

@define_test('Test oncomplete and ClientGroup')
def parallel3():
    def report(v, i):
        print('response from %d: %r' % (i, v))

    cg = easycluster.ClientGroup((l1, l2))
    for i, h in enumerate((l1, l2)):
        h.dosleep(0.3 - (i*0.1), oncomplete=(report, i))
    cg.read_responses(max=2)

@define_test('Test spawnlocal')
def testlocal():
    global l1
    l1 = spawn_local()
    reftest()
    methods()
    attrs()
    l1.testobjects.value = None

define_test('Parallel test with local and remote')(parallel3)

def test_rmt_thread(h, i, amt):
    print('Calling dosleep from thread %d' % i)
    v = h.dosleep(amt)
    print('Return in thread %d: %r' % (i, v))

@define_test('Connect using ThreadingClient')
def connectthread():
    global l2
    l2 = easycluster.AutoThreadingClient(**conn_params)

@define_test('Test ThreadingClient')
def connectthread():
    t1 = threading.Thread(target=test_rmt_thread, args=(l2, 1, 0.3))
    t2 = threading.Thread(target=test_rmt_thread, args=(l2, 2, 0.2))
    t1.start()
    t2.start()
    active_now = l2.call('threading.active_count')
    print('Active after starting: %d' % active_now)

    t1.join()
    t2.join()

    ## Dead threads are checked when responses are received
    l2.eval('0')
    active_after = l2.call('threading.active_count')
    print('Active after finishing: %d' % active_after)

def test_disconnect_thread(h, amt):
    print('Calling dosleep')
    try:
        h.dosleep(amt)
    except IOError as e:
        print('Disconnection caused error: %s' % e)
    else:
        assert False, 'Exception not raised on close'


@define_test('Test disconnection')
def disconnect_thread():
    t1 = threading.Thread(target=test_disconnect_thread, args=(l2, 2))
    t1.start()
    time.sleep(0.1)
    l2.close()
    time.sleep(0.2)
    t1.join()

server_check_runner()

options = OptionParser(usage='%prog [options] [host[:port][:key[file]=...]]', description='Demo script for EasyCluster')
opts, args = options.parse_args()
if len(args) > 0:
    rhost = args[0]
else:
    rhost = 'localhost'
conn_params = easycluster.parse_connection_spec(rhost)

for i, (name, f, rpt) in enumerate(tests):
    print('%03d %s...' % (i, name))
    stime = time.time()
    f()
    etime = time.time()
    print('   ... %s took %.3fs' % (name, etime - stime))
