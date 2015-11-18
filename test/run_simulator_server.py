import logging 
import sys

from discosbackend import server
from discosbackend.handlers import DBProtocolHandler

from roach2_backend import Roach2_Backend

logging.basicConfig(level=logging.DEBUG)
server.run_server(int(sys.argv[1]),
                  DBProtocolHandler(Roach2_Backend()))

