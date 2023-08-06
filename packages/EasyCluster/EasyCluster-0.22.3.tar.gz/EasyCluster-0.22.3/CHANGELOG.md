[Version 0.22.3 (2022-08-30)](https://pypi.org/project/EasyCluster/0.22.3/)
=============================

* Update easycluster_demo.py to reference python3 ([748b227](https://gitlab.com/ktpanda/easycluster/-/commit/748b227fd44f110201cdfa9d51c4bc59b91a68ab))
* Update setup instructions ([bc0a764](https://gitlab.com/ktpanda/easycluster/-/commit/bc0a76449285755f1a44559fdb961540761a7ce0))
* Migrate to setup.cfg ([47f41e5](https://gitlab.com/ktpanda/easycluster/-/commit/47f41e5b76ab2f9f3c1c8fe869b299047754c370))
* Author name change ([127c11c](https://gitlab.com/ktpanda/easycluster/-/commit/127c11c797db212d76b3070c9b37227c93e20c94))


[Version 0.22.2 (2016-10-14)](https://pypi.org/project/EasyCluster/0.22.2/)
=============================

* Added profiling option to server


[Version 0.22.1 (2014-02-28)](https://pypi.org/project/EasyCluster/0.22.1/)
=============================

* Added SSH tunneling
* Added pickle protocol negotiation for interop between Python 3.2 and 3.4
* Fixed race condition that can happen on slow servers when using
  multithreading


[Version 0.21 (2014-01-23)](https://pypi.org/project/EasyCluster/0.21/)
=============================

* Added option to disable IPv6 entirely and added more automatic IPv4
  fallbacks


[Version 0.20 (2014-01-20)](https://pypi.org/project/EasyCluster/0.20/)
=============================

* Found yet another way that Windows can fail to support IPv6.
* Added new utility functions get_global and set_global


[Version 0.19 (2013-08-29)](https://pypi.org/project/EasyCluster/0.19/)
=============================

* Client can now do an in-memory upgrade of server, as long as server is
  running version >= 0.09.
* Removed --class (-c) option, replaced with --verbose (-v). The -c option was
  generally only used to specify QuietServer, which is the default now.


[Version 0.18 (2013-08-26)](https://pypi.org/project/EasyCluster/0.18/)
=============================

* Implemented __setattr__ and __delattr__ on DefaultRemoteProxy. User-defined
  subclasses must define local instance attributes on the class itself to avoid
  inadvertently setting attributes on the remote object.
* Added compression as option in parse_connection_spec
* Fixed bug where typedat was not being cached properly and new proxy types
  were being created for each new object
* Fixed raw_{get|set}_attribute and added tests for them
* Fixed bug where proxy classes defined in define_common() were not being used
* Fixed race condition with ThreadedClient


[Version 0.17 (2013-08-23)](https://pypi.org/project/EasyCluster/0.17/)
=============================

* Added ability to bind server to a specific address; Added IP
  access controls.
* Fixed compatibility with Python 3 - All features, including service
  installation, now work
* Fixed bugs in raw_get_attribute and raw_set_attribute
* Changed DEFAULT_PORT to 11998 for python3 so both python2 and python3
  services can run at the same time
* Fixed bug where server would refuse to start with a blank key
* Fixed bug in make_singleton
* Changed the styles in the documentation a bit


[Version 0.16 (2013-08-23)](https://pypi.org/project/EasyCluster/0.16/)
=============================

* Expanded documentation: added README.html generated from README.txt
* Reworked the way proxies are handled
* added 'origexc' parameter to common methods
* Exported methods now automatically detected, and attribute access passed
  through
* Breaks compatibility with older versions, and has code to gracefully detect
  and report incompatibilities
* Added raw_get_attribute and raw_set_attribute
* Client.peername now contains hostname instead of IP address
* Fixed bug where setting remote global value using _GlobalProxy fails
* Changed AutoThreadingClient to ThreadedClient, old name kept for
  compatibility


[Version 0.15 (2013-08-21)](https://pypi.org/project/EasyCluster/0.15/)
=============================

* New function: parse_connection_spec
* Fixed some bugs with AutoThreadingClient


[Version 0.14 (2013-07-25)](https://pypi.org/project/EasyCluster/0.14/)
=============================

* Added support for service installation on Solaris


[Version 0.13 (2013-07-25)](https://pypi.org/project/EasyCluster/0.13/)
=============================

* Added support for chkconfig (Redhat Enterprise Linux 5)


[Version 0.12 (2013-07-02)](https://pypi.org/project/EasyCluster/0.12/)
=============================

* Added LSB compatible headers to init script


[Version 0.11 (2013-06-18)](https://pypi.org/project/EasyCluster/0.11/)
=============================

* Fixed service removal on Debian
* Add --query-installed option


[Version 0.10 (2013-06-11)](https://pypi.org/project/EasyCluster/0.10/)
=============================

* Fixed SetHandleInformation on Windows x86_64
* Fixed silent AttributeError bug in _GlobalProxy


[Version 0.09 (2013-05-20)](https://pypi.org/project/EasyCluster/0.09/)
=============================

* Changed the way non-hex keys are used. This breaks compatibility with
  command line keys and keys not generated by -g.
* Changed Windows code back to using subprocess due to weird bugs in
  multiprocessing.
* Moved Linux service later in startup order.


[Version 0.08 (2013-05-20)](https://pypi.org/project/EasyCluster/0.08/)
=============================

* Minor fixes to service installation
* Added linux_service module
* Added service installation options to main script


[Version 0.07 (2013-05-11)](https://pypi.org/project/EasyCluster/0.07/)
=============================

* Changed Windows server code to use multiprocessing instead of subprocess
* Initial support for installing as a service on Windows
* Changed single-file module into a package. Server specific functionality is
  now in easycluster.server.


[Version 0.06 (2013-02-27)](https://pypi.org/project/EasyCluster/0.06/)
=============================

* Reverted 'max_response' argument of ClientGroup.read_responses to 'max'
* Added _peer_version to Connection and server_version property to Client
* Fixed bug where 'onerror' was never called even if given
* Modified common definition initialization so that import and other errors
  are reported to the client
* Fixed timeout and max_responses on ClientGroup.read_responses
* Changing definitions so that compilation flags are not inherited (not
  everyone is ready for print_function).


[Version 0.05 (2013-02-19)](https://pypi.org/project/EasyCluster/0.05/)
=============================

* Fixing regression with closed connections
* Fixes compatibility with Python 3
* Tweaked demo script


[Version 0.04 (2013-02-15)](https://pypi.org/project/EasyCluster/0.04/)
=============================

* Fixed problem with keepalive messages
* Changed the way NonblockingResponses are handled
* Added initialization parameters to be sent to the server - breaks compatibility with earlier versions
* Added keepalive and timeout to AutoThreadingClient


[Version 0.03 (2013-02-15)](https://pypi.org/project/EasyCluster/0.03/)
=============================

* Added reconnect() method to Client
* Added public properties to proxies to get the connection
* Implemented key file security on Windows


[Version 0.02 (2013-02-08)](https://pypi.org/project/EasyCluster/0.02/)
=============================

* Deleted scripts/easycluster, replaced with entry point


[Version 0.01 (2013-02-07)](https://pypi.org/project/EasyCluster/0.01/)
=============================

* Changed the definition of eval and added execblock
* Added setuptools manifest and bootstrap
* Updated documentation
* Updated server script
* Added PyPI URL to setup.py


[Version 0.00](https://pypi.org/project/EasyCluster/0.00/)
=============================

* Initial version
