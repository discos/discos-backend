"""This module implemetns all the necessary logics used to read and write
correct messages according to the protocol.
It defines regular expression for message parsing and validation, and a Message
class used to incapsulate a protocol message within the software logics.
Defines functions for (de)serialization of basic types into text.
"""

import re
import logging
logger = logging.getLogger(__name__)

import time

REQUEST = '?'
REPLY = '!'
SEPARATOR = ','
OK = "ok"
FAIL = "fail"
INVALID = "invalid"

type_re = "(?P<type>(\%s|\%s))" % (REQUEST,REPLY)
type_pattern = re.compile(type_re)
name_re = "(?P<name>[a-zA-Z][a-zA-Z0-9-]*)"
name_pattern = re.compile(name_re)
code_re = ",(?P<code>(%s|%s|%s))" % (OK, FAIL, INVALID)
code_pattern = re.compile(code_re)
arguments_re = "(,(?P<arguments>[^\r\n]+))?"
arguments_pattern = re.compile(arguments_re)
linefeed_re = "(?P<linefeed>\r\n)?"
linefeed_pattern = re.compile(linefeed_re)
request_re = "^(?P<type>\%s)" % (REQUEST,) + \
          name_re + \
          arguments_re + \
          linefeed_re + \
          "$"
request_pattern = re.compile(request_re)
reply_re = "^(?P<type>\%s)" % (REPLY,) + \
          name_re + \
          code_re + \
          arguments_re + \
          linefeed_re + \
          "$"
reply_pattern = re.compile(reply_re)

argument_re = ""

class GrammarException(Exception):
    pass

class Message:
    def __init__(self, **kwargs):
        self.message_type = kwargs["message_type"]
        self.name = kwargs["name"]
        self.code = kwargs["code"] if kwargs.has_key("code") else ""
        self.arguments = kwargs["arguments"] if kwargs.has_key("arguments") else []

    def is_request(self):
        return self.message_type == REQUEST

    def is_reply(self):
        return self.message_type == REPLY

    def is_correct_reply(self, request):
        """
        check if this message is a correct reply according to the protocol, for
        the request message given as parameter
        @param request: the request message
        """
        if not self.is_reply():
            return False
        if not self.name == request.name:
            return False
        if not self.check_synthax():
            return False
        return True

    def check_synthax(self):
        """check if the message object can be converted to a syntactically
        correct message string
        @return True if synthax is ok, False otherwise
        """
        try:
            parse_message(str(self))
            return True
        except GrammarException:
            return False
        return True #never reached

    def __str__(self):
        """Transforms the message object into a correct message string, the CR
        LF trailing is omitted.
        """
        return_str = ""
        arguments_str = "," + ",".join(self.arguments) if self.arguments else ""
        if self.is_reply():
            return_str = "%s%s,%s%s" % (self.message_type,
                                        self.name,
                                        self.code,
                                        arguments_str)
        else:
            return_str = "%s%s%s" % (self.message_type,
                                     self.name,
                                     arguments_str)
        return return_str

def parse_message(message_string):
    """
    Parses a message. 
    @param message: the message to be parsed, if the trailing \\r\\n is present
    it will be removed
    @return the grammar.Message object resulting from the parsing
    @raises GrammarException if the message synthax is invalid
    """
    if not message_string:
        raise GrammarException("empty message is not valid")
    elif message_string.startswith(REPLY):
        match = reply_pattern.match(message_string)
    elif message_string.startswith(REQUEST):
        match = request_pattern.match(message_string)
    else:
        raise GrammarException("invalid message type '%s'" % (message_string[0],))
    if not match:
        raise GrammarException("invalid synthax")
    #TODO: validate arguments synthax and resolve the ',' issue
    if match.groupdict()["arguments"]:
        arguments = match.groupdict()["arguments"].split(",")
    else:
        arguments = []
    code = match.groupdict()["code"] if match.groupdict().has_key("code") else ""
    return Message(message_type = match.groupdict()["type"],
                   name = match.groupdict()["name"],
                   code = code,
                   arguments = arguments)

