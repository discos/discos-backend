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

"""This module implements all the necessary logics used to read and write
correct messages according to the protocol.
It defines regular expression for message parsing and validation, and a Message
class used to incapsulate a protocol message within the software logics.
Defines functions for (de)serialization of basic types into text.
"""

import re
import logging
logger = logging.getLogger(__name__)


REQUEST = '?'
REPLY = '!'
SEPARATOR = ','
OK = "ok"
FAIL = "fail"
INVALID = "invalid"

type_re = fr"(?P<type>(\{REQUEST}|\{REPLY}))"
type_pattern = re.compile(type_re)
name_re = r"(?P<name>[a-zA-Z][a-zA-Z0-9-]*)"
name_pattern = re.compile(name_re)
code_re = fr",(?P<code>({OK}|{FAIL}|{INVALID}))"
code_pattern = re.compile(code_re)
argument_re = r""
arguments_re = r"(,(?P<arguments>[^\r\n]+))?"
arguments_pattern = re.compile(arguments_re)
linefeed_re = r"(?P<linefeed>\r\n)?"
linefeed_pattern = re.compile(linefeed_re)
request_re = fr"^(?P<type>\{REQUEST})"
request_re += name_re + arguments_re + linefeed_re + "$"
request_pattern = re.compile(request_re)
reply_re = fr"^(?P<type>\{REPLY})"
reply_re += name_re + code_re + arguments_re + linefeed_re + "$"
reply_pattern = re.compile(reply_re)


class GrammarException(Exception):
    pass


class Message:
    def __init__(self, **kwargs):
        self.message_type = kwargs["message_type"]
        self.name = kwargs["name"]
        self.code = kwargs["code"] if "code" in kwargs else ""
        self.arguments = kwargs["arguments"] if "arguments" in kwargs else []

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
        except GrammarException:
            return False
        return True

    def __str__(self):
        """Transforms the message object into a correct message string, the CR
        LF trailing is omitted.
        """
        return_str = ""
        args_str = "," + ",".join(self.arguments) if self.arguments else ""
        if self.is_reply():
            args = (
                self.message_type,
                self.name,
                self.code,
                args_str
            )
            return_str = f"{args[0]}{args[1]},{args[2]}{args[3]}"
        else:
            args = (
                self.message_type,
                self.name,
                args_str
            )
            return_str = f"{args[0]}{args[1]}{args[2]}"
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
    if message_string.startswith(REPLY):
        match = reply_pattern.match(message_string)
    elif message_string.startswith(REQUEST):
        match = request_pattern.match(message_string)
    else:
        raise GrammarException(f"invalid message type '{message_string[0]}'")
    if not match:
        raise GrammarException("invalid synthax")
    # TODO: validate arguments synthax and resolve the ',' issue
    if match.groupdict()["arguments"]:
        arguments = match.groupdict()["arguments"].split(",")
    else:
        arguments = []
    code = match.groupdict()["code"] if "code" in match.groupdict() else ""
    return Message(
        message_type=match.groupdict()["type"],
        name=match.groupdict()["name"],
        code=code,
        arguments=arguments
    )
