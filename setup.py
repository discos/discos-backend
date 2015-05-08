from distutils.core import setup
import os

setup(name = "discosbackend",
        version = "0.3",
        author = "Marco Bartolini",
        author_email = "bartolini@ira.inaf.it",
        description = "reference implementation of the discos protocol for backend communication",
        license="gpl",
        url = "https://github.com/discos/discosbackend",
        packages = ['discosbackend'],
        package_dir = {'discosbackend' : 'src',},
        requires = ["twisted"],
        classifiers = [
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Natural Language :: English",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Astronomy"
            ],
        long_description = """
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
