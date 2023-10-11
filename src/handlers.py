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
from discosbackend import grammar
from discosbackend import __protocol_version__
from astropy.time import Time
logger = logging.getLogger(__name__)


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
        raise NotImplementedError  # pragma: no cover

    def start(self):
        """Called upon protocol initialization
        """
        logger.debug("%s started", self.__class__)

    def stop(self):
        """Called before shutting down the server
        """
        logger.debug("%s stopped", self.__class__)


class AlwaysOkHandler(Handler):
    """This is a null protocol handler, it defines the behaviour of a
    server which simply replies ok to every possible request. Used only for
    debug and testing purpose.
    """
    def handle(self, message):
        return grammar.Message(
            message_type=grammar.REPLY,
            name=message.name,
            code=grammar.OK,
            arguments=message.arguments
        )


class AlwaysFailHandler(Handler):
    """This is a null protocol handler, it defines the behaviour of a
    server which simply replies fail to every possible request. Used only for
    debug and testing purpose.
    """
    def handle(self, message):
        return grammar.Message(
            message_type=grammar.REQUEST,
            name=message.name,
            code=grammar.OK,
            arguments=message.arguments
        )


class AlwaysRaiseHandler(Handler):
    """This is a null protocol handler, it defines the behaviour of a
    server which simply replies with another request to every possible
    request. Used only for debug and testing purpose.
    """
    def handle(self, message):
        raise Exception("always raised exception")


class DBProtocolHandler(Handler):
    """The real protocol handler. It parses the message and check for
    correctness and protol compliance. Then it call the proper backend method
    and get the answer with which to build the reply Message
    """

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.commands = {
            "status"            : self.do_status,
            "get-tpi"           : self.do_getTpi,
            "get-tp0"           : self.do_getTp0,
            "version"           : self.do_version,
            "get-configuration" : self.do_get_configuration,
            "set-configuration" : self.do_set_configuration,
            "set-integration"   : self.do_set_integration,
            "get-integration"   : self.do_get_integration,
            "time"              : self.do_time,
            "start"             : self.do_start,
            "stop"              : self.do_stop,
            "set-section"       : self.do_set_section,
            "cal-on"            : self.do_cal_on,
            "set-filename"      : self.do_set_filename,
            # new in version 1.2
            "convert-data"      : self.do_convert_data,
            # new in version 1.3
            "set-enable"        : self.do_set_enable
        }

    def handle(self, message):
        logger.info("HANDLE:")
        reply = grammar.Message(
            message_type=grammar.REPLY,
            name=message.name
        )
        if message.name not in self.commands:
            raise HandlerException(f"invalid command '{message.name}'")
        logger.debug("received command: %s", message.name)
        reply_arguments = self.commands[message.name](message.arguments)
        if reply_arguments:
            reply.arguments = list(map(str, reply_arguments))
        reply.code = grammar.OK
        return reply

    def do_status(self, _):
        return self.backend.status()

    def do_getTpi(self, _):
        return self.backend.get_tpi()

    def do_getTp0(self, _):
        return self.backend.get_tp0()

    def do_version(self, _):
        return [__protocol_version__]

    def do_get_configuration(self, _):
        return self.backend.get_configuration()

    def do_set_configuration(self, args):
        if len(args) < 1:
            raise HandlerException("missing argument: configuration")
        return self.backend.set_configuration(str(args[0]))

    def do_get_integration(self, _):
        return self.backend.get_integration()

    def do_set_integration(self, args):
        if len(args) < 1:
            raise HandlerException("missing argument: integration time")
        try:
            _integration = int(args[0])
        except ValueError as ex:
            raise HandlerException(
                "integration time must be an integer number"
            ) from ex
        return self.backend.set_integration(_integration)

    def do_time(self, _):
        return self.backend.time()

    def do_start(self, args):
        if len(args) < 1:
            return self.backend.start()
        try:
            timestamp = Time(int(args[0]), format="discos")
        except ValueError as ex:
            raise HandlerException("wrong timestamp '{args[0]}'") from ex
        return self.backend.start(timestamp)

    def do_stop(self, args):
        if len(args) < 1:
            return self.backend.stop()
        try:
            timestamp = Time(int(args[0]), format="discos")
        except ValueError as ex:
            raise HandlerException("wrong timestamp '{args[0]}'") from ex
        return self.backend.stop(timestamp)

    def do_set_section(self, args):
        def _get_param(p, _type_converter=str):
            if p == "*":
                return p
            return _type_converter(p)

        if len(args) < 7:
            raise HandlerException("set-section needs 7 arguments")
        try:
            section = _get_param(args[0], int)
            start_freq = _get_param(args[1], float)
            bandwidth = _get_param(args[2], float)
            feed = _get_param(args[3], int)
            mode = _get_param(args[4])
            sample_rate = _get_param(args[5], float)
            bins = _get_param(args[6], int)
        except ValueError as ex:
            raise HandlerException("wrong parameter format") from ex
        return self.backend.set_section(
            section,
            start_freq,
            bandwidth,
            feed,
            mode,
            sample_rate,
            bins
        )

    def do_cal_on(self, args):
        if len(args) < 1:
            _interleave = 0
        else:
            try:
                _interleave = int(args[0])
            except ValueError as ex:
                raise HandlerException(
                    "interleave samples must be a positive int"
                ) from ex
            if _interleave < 0:
                raise HandlerException(
                    "interleave samples must be a positive int"
                )
        return self.backend.cal_on(_interleave)

    def do_set_filename(self, args):
        if len(args) < 1:
            raise HandlerException("command needs <filename> as argument")
        return self.backend.set_filename(args[0])

    def do_convert_data(self, _):
        """
        Added in version 1.2
        """
        return self.backend.convert_data()

    def do_set_enable(self, args):
        """
        Added in version 1.3
        """
        if len(args) < 2:
            raise HandlerException("set-enable needs 2 arguments")
        try:
            _feed1 = int(args[0])
            _feed2 = int(args[1])
        except ValueError as ex:
            raise HandlerException("wrong parameter format") from ex
        return self.backend.set_enable(_feed1, _feed2)
