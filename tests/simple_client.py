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

import socket

from discosbackend import grammar


class SimpleClient:
    def __init__(self, port):
        self.client = None
        self.port = port
        self.timeout = 10

    def _lazy_connection(self):
        if self.client is None:
            self.client = socket.create_connection(
                ('localhost', self.port),
                self.timeout
            )

    def send_message(self, message):
        self._lazy_connection()
        self.client.sendall(
            (str(message) + '\r\n').encode('latin-1')
        )

    def read_message(self):
        self._lazy_connection()
        recv = b''
        while True:
            chunk = self.client.recv(1)
            recv += chunk
            if recv.endswith(b'\r\n'):
                return grammar.parse_message(recv.decode())

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
