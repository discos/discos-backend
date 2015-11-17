import logging
logger = logging.getLogger(__name__)
from twisted.internet import reactor

from protocol import DBFactory

def run_server(port, handler):
    logger.info("running discos backend protocol server")
    logger.info("listening on TCP port %d" % (port,))
    logger.info("Protocol handler: %s" % (str(handler.__class__)))
    reactor.listenTCP(port, DBFactory(handler = handler))
    reactor.run()

