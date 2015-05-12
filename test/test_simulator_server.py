import unittest
import subprocess
import time

from discosbackend.handlers import AlwaysOkHandler
from discosbackend.server import run_server
from discosbackend import grammar

from simple_client import SimpleClient

TCP_PORT = 8988

class TestSimulatorServer(unittest.TestCase):

    def setUp(self):
        self.pid = subprocess.Popen(["python", 
                                    "test/run_simulator_server.py",
                                    str(TCP_PORT)]
                                  ).pid
        time.sleep(1.0)
        self.client = SimpleClient(TCP_PORT)

    def tearDown(self):
        self.client.close()
        subprocess.call(["kill", "-9", str(self.pid)])

    def test_undefined_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "badcommand")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)

    def test_time_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "time")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        self.assertAlmostEqual(time.time(),
                               float(reply.arguments[0]),
                               delta = 0.5)

    def test_status_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "status")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        self.assertAlmostEqual(time.time(),
                               float(reply.arguments[0]),
                               delta = 0.5)
        self.assertEqual(reply.arguments[1], grammar.OK)
        self.assertEqual(reply.arguments[2], "0")

    def test_configuration_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "configuration")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        self.assertEqual(reply.arguments[0], "unconfigured")

    def test_set_configuration_command(self):
        conf_name = "testconfiguration"
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-configuration",
                                  arguments = [conf_name])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "configuration")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        self.assertEqual(reply.arguments[0], conf_name)

    def test_start_now_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "start")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "status")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "1")

    def test_start_already_started_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "start")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "status")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "1")
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "start")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)

    def test_stop_not_started_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "stop")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)

    def test_start_at_command(self):
        delay = 5
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "start",
                                  arguments = [str(time.time() + delay)])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "status")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "0")
        time.sleep(delay)
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "1")

    def test_stop_at_command(self):
        delay = 5
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "start")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "stop",
                                  arguments = [str(time.time() + delay)])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "status")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "1")
        time.sleep(delay)
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "0")

    def test_startand_stop__at_command(self):
        start_delay = 5
        stop_delay = 10
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "start",
                                  arguments = [str(time.time() + start_delay)])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "stop",
                                  arguments = [str(time.time() + stop_delay)])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "status")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "0")
        time.sleep(start_delay)
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "1")
        time.sleep(stop_delay - start_delay)
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.arguments[2], "0")

