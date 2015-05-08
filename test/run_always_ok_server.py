import logging 

from discosbackend import server
from discosbackend.handlers import AlwaysOkHandler

logging.basicConfig(level=logging.DEBUG)
server.run_server(8988, AlwaysOkHandler())

