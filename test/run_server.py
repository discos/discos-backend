import logging 
import sys

from discosbackend import server
from discosbackend.handlers import DBProtocolHandler

from roach2_backend import Roach2_Backend
#filename='example.log'
logging.basicConfig(filename='example.log',level=logging.DEBUG)
server.run_server(int(sys.argv[1]),
                  DBProtocolHandler(Roach2_Backend()))

