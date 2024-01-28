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
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import Factory

from discosbackend import grammar
from discosbackend.handlers import HandlerException
from discosbackend import __protocol_version__
logger = logging.getLogger(__name__)


class DBProtocol(LineOnlyReceiver):
    """
    This class defines the DBProtocol. Its duty is to control protocol
    consistency and correctness and to pass correct messages to a protocol
    handler which return reply messages which this class will forward to the
    request sender in the correct protocol format.
    """
    def __init__(self):
        pass

    def lineReceived(self, line):
        logger.debug("received line: %s", line.decode())
        line = line.decode("latin-1")
        try:
            message = grammar.parse_message(line)
            logger.debug("message successfully parsed")
        except grammar.GrammarException as ge:
            logger.debug("synthax error: %s", str(ge))
            reply_message = grammar.Message(
                message_type=grammar.REPLY,
                name="undefined",
                code=grammar.INVALID,
                arguments=["synthax error: {str(ge)}"]
            )
            self.sendLine(str(reply_message).encode('latin-1'))
            return
        if message.is_request():  # we only process requests
            try:
                reply_message = self.factory.handler.handle(message)
                if not reply_message.is_correct_reply(message):
                    logger.debug("The handler returned an incorrect reply")
                    self._send_fail_reply(message)
                else:
                    self.sendLine(
                        str(reply_message).encode('latin-1')
                    )
            except HandlerException as he:
                logger.exception(he)
                # this exception is some way expected it happens
                # on every failure from the handler
                self._send_fail_reply(message, str(he))
            except Exception as e:
                # unexpected exception from the handler
                logger.exception(e)
                self._send_fail_reply(message)

    def _send_fail_reply(
            self,
            request,
            fail_message="Request could not be handled correctly"):
        reply = grammar.Message(
            message_type=grammar.REPLY,
            name=request.name,
            code=grammar.FAIL,
            arguments=[fail_message]
        )
        self.sendLine(str(reply).encode("latin-1"))

    def connectionMade(self):
        logger.debug("client connected")
        connection_reply = grammar.Message(
            message_type=grammar.REPLY,
            name="version",
            code=grammar.OK,
            arguments=[__protocol_version__]
        )
        self.sendLine(str(connection_reply).encode("latin-1"))

    def connectionLost(self, reason=None):
        logger.debug("client disconnected: %s", str(reason))


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
