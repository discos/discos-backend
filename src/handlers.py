import logging
logger = logging.getLogger(__name__)

import grammar
import timediscos

class HandlerException(Exception):
    pass

class Handler(object):
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
    server which simply replies ok to every possible request. Used only for
    debug and testing purpose.
    """
    def handle(self, message):
        return grammar.Message(message_type = grammar.REPLY,
                               name = message.name,
                               code = grammar.OK,
                               arguments = message.arguments)


class DBProtocolHandler(Handler):
    """The real protocol handler. It parses the message and check for
    correctness and protol compliance. Then it call the proper backend method
    and get the answer with which to build the reply Message
    """

    def __init__(self, backend):
        super(DBProtocolHandler, self).__init__()
        self.backend = backend
        self.commands = {
                    "status"           : self.do_status,
                    "version"          : self.do_version,
                    "configuration"    : self.do_configuration,
                    "set-configuration": self.do_set_configuration,
                    "time"             : self.do_time,
                    "start"            : self.do_start,
                    "stop"             : self.do_stop,
                   }

    """This is the class which defines the actual handling of message protocols
    """
    def handle(self, message):
        reply = grammar.Message(message_type = grammar.REPLY,
                                name = message.name)
        if not self.commands.has_key(message.name):
            raise HandlerException("invalid command '%s'" % (message.name,))
        logger.debug("received command: %s" % (message.name,))
        reply_arguments = self.commands[message.name](message.arguments)
        if reply_arguments:
            reply.arguments = map(str, reply_arguments)
        reply.code = grammar.OK
        return reply

    def do_status(self, args):
        return self.backend.status()

    def do_version(self, args):
        return self.backend.version()

    def do_configuration(self, args):
        return self.backend.configuration()

    def do_set_configuration(self, args):
        if len(args) < 1:
            raise HandlerException("missing argument: configuration")
        return self.backend.set_configuration(str(args[0]))

    def do_time(self, args):
        return self.backend.time()

    def do_start(self, args):
        if len(args) < 1:
            return self.backend.start()
        try:
            timestamp = timediscos.parse_unix_time(args[0])
        except:
            raise HandlerException("wrong timestamp '%s'" % (args[0],))
        return self.backend.start(timestamp.unix)

    def do_stop(self, args):
        if len(args) < 1:
            return self.backend.stop()
        try:
            timestamp = timediscos.parse_unix_time(args[0])
        except:
            raise HandlerException("wrong timestamp '%s'" % (args[0],))
        return self.backend.stop(timestamp.unix)
        
