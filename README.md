DISCOS
======

Discos is **Development of the Italian Single-dish Control System**
developed by INAF. 
You can find more informations on our home site at
http://discos.readthedocs.org/en/latest/

DISCOS BACKEND
==============

This package defines a reference implementation for the protocol used by
discos for communicating with external backends. The protocol is defined
at
http://discos.readthedocs.org/en/latest/developer/protocols/backends.html

Package contents
----------------

This package implements a parser for the protocol grammar as well as a
twisted protocol which exploits the parser. 
The handlers module also defines some simple protocol handlers which can
be used for testing and protocol simulation, giving at the same time a
good starting point for other implementations.

Requirements
~~~~~~~~~~~~

**twisted** for the thersver implemntation and **astropy** now only used for
time management, both installable via pip::

  $ pip install astropy twisted

Testing
-------

The package tests can be run with the provided script **run_tests** 
depends on python modules **nose** and **coverage**::

  $ pip install nose coverage
  $./run_tests

It will print to screen test results as expected while also generating xunit xml
report in *test/results/report.xml* and a coverage html report in
*test/coverage/index.html*.

