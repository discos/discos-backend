
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.34127.svg)](http://dx.doi.org/10.5281/zenodo.34127)
[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
[![Build Status](https://github.com/discos/discos-backend/workflows/CI%20Tests/badge.svg)](https://github.com/discos/discos-backend)
[![Coverage Status](https://codecov.io/gh/discos/discos-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/discos/discos-backend)

# DISCOS BACKEND

This package defines a reference implementation for the protocol used by
discos for communicating with external backends. The protocol is defined
at
http://discos.readthedocs.org/en/latest/developer/protocols/backends.html

# Package contents

This package implements a parser for the protocol grammar as well as a
twisted protocol which exploits the parser. 
The handlers module also defines some simple protocol handlers which can
be used for testing and protocol simulation, giving at the same time a
good starting point for other implementations.

## Requirements

  * **twisted** for the the server implementation 
  * **astropy** for time management
  * **coverage** and **prospector** are used for test execution

Dependencies can be installed via pip:

```bash
  $ pip install -r requirements.txt
```

The same can be done for testing dependencies:

```bash
  $ pip install -r testing_requirements.txt
```

# Using the package

You can have an idea about how to integrate your own discos protocol 
implementation into the tcp server by looking at the 
**test/backend_simulator.py** module which defines a **Backend** class. 
If you need to define your own implementation you can just mimic its 
behaviour by implementing your own class which redefines all the public 
methods (the one which do not start with _). 

You can run the server using your protocol definitions, just like 
the definition in **scripts/run_server.py**:

```python
from discosbackend import server
from discosbackend.handlers import DBProtocolHandler
 
from yourmodule import YourBackend

tcp_port = 8978
server.run_server(
    tcp_port, DBProtocolHandler(YourBackend())
)
```

## Testing your implementation

Once you write your own implementation of the protocol you can test it 
just like it's done in **test/test_simulator_server.py**. You can safely 
reuse the tests defined in this TestCase, all you need to do is to 
redefine the **setUp** and **tearDown** methods to let them launch 
your own implementation.

# Testing the package

The package tests can be run with the provided script **run_tests** .

```bash
  $./run_tests
```

It will print to screen test results as expected while also generating a
coverage html report in *htmlcov/index.html*.
