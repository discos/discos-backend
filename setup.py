
#
#
#   Copyright 2015 Marco Bartolini, bartolini@ira.inaf.it
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from setuptools import setup

setup(
    name="discosbackend",
    version="1.4",
    author="Marco Bartolini",
    maintainer="Giuseppe Carboni",
    maintainer_email="giuseppe.carboni@inaf.it",
    description="reference implementation of the discos \
        protocol for backend communication",
    license="gpl",
    url="https://github.com/discos/discosbackend",
    packages=['discosbackend'],
    package_dir={'discosbackend' : 'src'},
    requires=["twisted", "astropy"],
    classifiers=[
        "Development Status :: 5 - Production",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Astronomy"
    ],
    long_description="""
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
    The handler module also defines some simple protocol handlers which can
    be used for testing and protocol simulation, giving at the same time a
    good starting point for other implementations.
    """,
)
