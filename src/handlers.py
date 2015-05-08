import logging
logger = logging.getLogger(__name__)

import grammar

class HandlerException(Exception):
    pass

class Handler:
    """Base class for defining protocol handlers
    """
    def handle(self, message):
        """Handles a request message. This methos must be reimplemented by
        subclasses
        @param message: a request message, the message has already been parsed
        and proven correct, the handler does not need to perform any check
        @type message: grammar.Message
        @return reply: a reply message object. The reply should be correct
        otherwise there is no guarantee that it will be delivered. The default
        server implementation for example will discard it and substitute with
        a 'fail' reply
        @raise HandlerException: if we want to notify the server that something
        went wrong we can use this exception that will be managed by the server
        in a clean way.
        """
        raise NotImplementedError

    def start(self):
        """Called upon protocol initialization
        """
        logger.debug("%s started" % self.__class__)

    def stop(self):
        """Called before shutting down the server
        """
        logger.debug("%s stopped" % self.__class__)

class AlwaysOkHandler(Handler):
    """This is a null protocol handler, it defines the behaviour of a 
    server which simply replies ok to every possible request.
    """
    def handle(self, message):
        return grammar.Message(message_type = grammar.REPLY,
                               name = message.name,
                               code = grammar.OK,
                               arguments = message.arguments)

