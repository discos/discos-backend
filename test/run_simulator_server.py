import logging 
import sys

from discosbackend import server
from discosbackend.handlers import DBProtocolHandler

from backend_simulator import Backend

logging.basicConfig(level=logging.DEBUG)
server.run_server(int(sys.argv[1]),
                  DBProtocolHandler(Backend()))

