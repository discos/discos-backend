import logging
logger = logging.getLogger(__name__)
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import Factory

import grammar
from handlers import HandlerException


class DBProtocol(LineOnlyReceiver):
    """
    This class defines the DBProtocol. Its duty is to control protocol consistency
    and correctness and to pass correct messages to a protocol handler which return
    reply messages which this class will forward to the request sender in the
    correct protocol format.
    """
    def __init__(self):
        self.protocol_version = grammar.PROTOCOL_VERSION

    def lineReceived(self, line):
        logger.debug("received line: " + line)
        try:
            message = grammar.parse_message(line)
            logger.debug("message successfully parsed")
        except grammar.GrammarException, ge:
            logger.debug("synthax error: %s" % (ge.message,))
            reply_message = grammar.Message(message_type = grammar.REPLY,
                                    name = "undefined",
                                    code = grammar.INVALID,
                                    arguments = ["synthax error: %s" %
                                                 (ge.message,)])
            self.sendLine(str(reply_message))
            return
        if message.is_request(): #we only process requests
            try:
                reply_message = self.factory.handler.handle(message)
                if not reply_message.is_correct_reply(message):
                    logger.debug("The handler returned an incorrect reply")
                    self.send_default_reply(message)
                else:
                    self.sendLine(str(reply_message))
            except HandlerException, he:
                logger.exception(he)
                #this exceptions is some way expected
                #we coudl differentiate the behaviour here
                self._send_default_reply(message)
            except Exception, e:
                #unexpected exception from the handler
                logger.exception(e)
                self._send_default_reply(message)

    def _send_default_reply(self, request):
        reply = grammar.Message(
                    message_type = grammar.REPLY,
                    name = request.name,
                    code = grammar.FAIL,
                    arguments = ["Request could not be hanlded correctly"])
        self.sendLine(str(reply))

    def connectionMade(self):
        logger.debug("client connected")

    def connectionLost(self, reason):
        logger.debug("client disconnected: " + str(reason))


class DBFactory(Factory):

    protocol = DBProtocol

    def __init__(self, handler):
        """
        @param handler: an instance of the protocol handler to be used, defaults
        to 'AlwaysOkHandler'
        """
        self.handler = handler

    def startFactory(self):
        self.handler.start()

    def stopFactory(self):
        self.handler.stop()

