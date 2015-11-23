
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

import logging
logger = logging.getLogger(__name__)
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import Factory

import grammar
from handlers import HandlerException
from discosbackend import __protocol_version__ as PROTOCOL_VERSION


class DBProtocol(LineOnlyReceiver):
    """
    This class defines the DBProtocol. Its duty is to control protocol consistency
    and correctness and to pass correct messages to a protocol handler which return
    reply messages which this class will forward to the request sender in the
    correct protocol format.
    """
    def __init__(self):
        pass

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
                    self.send_fail_reply(message)
                else:
                    self.sendLine(str(reply_message))
            except HandlerException, he:
                logger.exception(he)
                #this exception is some way expected it happens 
                #on every failure from the handler
                self._send_fail_reply(message, he.message)
            except Exception, e:
                #unexpected exception from the handler
                logger.exception(e)
                self._send_fail_reply(message)

    def _send_fail_reply(self, request,
        fail_message="Request could not be handled correctly"):
        reply = grammar.Message(
                    message_type = grammar.REPLY,
                    name = request.name,
                    code = grammar.FAIL,
                                arguments = [fail_message])
        self.sendLine(str(reply))

    def connectionMade(self):
        logger.debug("client connected")
        connection_reply = grammar.Message(
                    message_type = grammar.REPLY,
                    name = "version",
                    code = grammar.OK,
                    arguments = [PROTOCOL_VERSION])
        self.sendLine(str(connection_reply))


    def connectionLost(self, reason):
        logger.debug("client disconnected: " + str(reason))


class DBFactory(Factory):

    protocol = DBProtocol

    def __init__(self, handler):
        """
        @param handler: an instance of the protocol handler to be used, should
        be a subclass of handlers.Handler
        """
        self.handler = handler

    def startFactory(self):
        self.handler.start()

    def stopFactory(self):
        self.handler.stop()

