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

import telnetlib

from discosbackend import grammar


class SimpleClient:
    def __init__(self, port):
        self.telnet_client = telnetlib.Telnet("localhost", port)

    def send_message(self, message):
        self.telnet_client.write(
            (str(message) + '\r\n').encode('latin-1')
        )

    def read_message(self):
        recv = self.telnet_client.read_until(b'\r\n', 10)
        return grammar.parse_message(recv.decode())

    def close(self):
        self.telnet_client.close()
