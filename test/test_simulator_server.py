import unittest
import subprocess32 as subprocess
import time
import logging
logger=logging.getLogger(__name__)

from discosbackend.handlers import AlwaysOkHandler
from discosbackend.server import run_server
from discosbackend import grammar
from discosbackend import __protocol_version__ as PROTOCOL_VERSION
from discosbackend.timediscos import get_acs_now, unix_to_acs_time

from simple_client import SimpleClient

TCP_PORT = 8988

def time_to_string(unix_time):
    discos_time = unix_to_acs_time(unix_time)
    return str("%.f" % discos_time.discos)

class TestSimulatorServer(unittest.TestCase):

    def setUp(self):
        self._server = subprocess.Popen(["python", 
                                    "test/run_simulator_server.py",
                                    str(TCP_PORT)]
                                  )
        logger.info("SERVER LISTENING PID %d" % (self._server.pid,))
        time.sleep(3)
        self.client = SimpleClient(TCP_PORT)
        self.client.read_message()

    def tearDown(self):
        self.client.close()
        self._server.terminate()
        time.sleep(1)

    def test_undefined_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "badcommand")
        logger.debug(request)
        self.client.send_message(request)
        reply = self.client.read_message()
        logger.debug(reply)
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

    def test_version_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "version")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        self.assertEqual(reply.arguments[0], PROTOCOL_VERSION)

    def test_get_configuration_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "get-configuration")
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
                                  name = "get-configuration")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        self.assertEqual(reply.arguments[0], conf_name)

    def test_get_integration_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "get-integration")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        self.assertEqual(reply.arguments[0], "0")

    def test_set_integration_command(self):
        integration = 10
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-integration",
                                  arguments = [str(integration)])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "get-integration")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        self.assertEqual(int(reply.arguments[0]), integration)

    def set_bad_integration_string_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-integration",
                                  arguments = ['ciao'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)

    def test_get_tpi_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "get-tpi")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        for tpi in map(float, reply.arguments):
            self.assertGreaterEqual(tpi, 0)
            self.assertLessEqual(tpi, 100)

    def test_get_tp0_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "get-tp0")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        for tpi in map(float, reply.arguments):
            self.assertEqual(tpi, 0)

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
                                  arguments = [time_to_string(time.time() + delay)])
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
                                  arguments = [time_to_string(time.time() + delay)])
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

    def test_start_and_stop_at_command(self):
        start_delay = 5
        stop_delay = 10
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "start",
                                  arguments = [time_to_string(time.time() + \
                                      start_delay)])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "stop",
                                  arguments = [time_to_string(time.time() + \
                                          stop_delay)])
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

    def test_set_section_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-section",
                                  arguments = ['1', '*','*','*','*','*','*'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-section",
                                  arguments = ['1', '234.0',
                                               '500.23','3','FullStokes','10','2048'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)

    def test_bad_set_section_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-section",
                                  arguments = ['ciao', '*','*','*','*','*','*'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-section",
                                  arguments = ['1', 'wrong',
                                               '500.23','3','FullStokes','10','2048'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-section",
                                  arguments = ['1', '234.0',
                                               'wrong','3','FullStokes','10','2048'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-section",
                                  arguments = ['1', '234.0'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)

    def test_cal_on_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "cal-on",
                                  arguments = ['1'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)
        #test also default argument
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "cal-on")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)

    def test_bad_cal_on_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "cal-on",
                                  arguments = ['wrong'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "cal-on",
                                  arguments = ['-10'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)

    def test_set_filename_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-filename",
                                  arguments = ['newfilename'])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.OK)

    def test_bad_set_filename_command(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "set-filename",
                                  arguments = [])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.FAIL)
