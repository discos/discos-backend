import logging 
import sys

from discosbackend import server
from discosbackend.handlers import AlwaysOkHandler

logging.basicConfig(level=logging.DEBUG)
server.run_server(int(sys.argv[1]), AlwaysOkHandler())

