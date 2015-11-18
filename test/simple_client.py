import telnetlib
import time

from discosbackend import grammar

class SimpleClient:
    def __init__(self, port):
        self.telnet_client = telnetlib.Telnet("localhost", port)

    def send_message(self, message):
        self.telnet_client.write(str(message) + '\r\n')

    def read_message(self):
        recv = self.telnet_client.read_until('\r\n', 10)
        return grammar.parse_message(recv)

    def close(self):
        self.telnet_client.close()

