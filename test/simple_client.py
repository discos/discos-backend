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


client = SimpleClient(10000)
client.send_message("?integration,101")
print client.read_message()
client.send_message("?set-configuration,RL23")
print client.read_message()
client.send_message("?set-section,0,0.000000,1500.000000,0,2,750.000000,16384")
print client.read_message()
client.send_message("?start,000000")
print client.read_message()
time.sleep(10)
client.send_message("?get-tpi")
print client.read_message()
print client.read_message()
time.sleep(30)
client.send_message("?stop,0")
print client.read_message()

#print client.read_message()

#DEBUG:discosbackend.protocol:received line: ?set-section,0,0.000000,500.000000,0,2,250.000000,16384
#DEBUG:discosbackend.protocol:received line: ?set-section,0,0.000000,1501.000000,0,2,250.000000,16384

