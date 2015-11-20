import logging
logger = logging.getLogger(__name__)

import unittest
import subprocess32 as subprocess
import time

from discosbackend.handlers import AlwaysOkHandler
from discosbackend.server import run_server
from discosbackend import grammar

from simple_client import SimpleClient

TCP_PORT = 8988

class TestAlwaysOkServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._server = subprocess.Popen(["python", 
                                    "test/run_always_ok_server.py",
                                    str(TCP_PORT)]
                                  )
        logger.info("SERVER LISTENING PID %d" % (cls._server.pid,))
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        #does not work on OSX
        #subprocess.call(["kill", "-9", str(cls.pid)])
        logger.info("KILLING SERVER PID %d" % (cls._server.pid,))
        cls._server.terminate()
        time.sleep(3)

    def setUp(self):
        self.client = SimpleClient(TCP_PORT)
        time.sleep(1)
        self.client.read_message()

    def test_good_request_without_argument(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "prova")
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertTrue(reply.is_correct_reply(request))
        self.assertEqual(reply.code, grammar.OK)

    def test_good_request_with_arguments(self):
        request = grammar.Message(message_type = grammar.REQUEST,
                                  name = "prova",
                                  arguments = ["arg1", "arg2"])
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertTrue(reply.is_correct_reply(request))
        self.assertEqual(reply.code, grammar.OK)
        self.assertEqual(request.arguments, reply.arguments)

    def test_bad_request_type(self):
        self.client.send_message("$name")
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.INVALID)

    def test_bad_request_name(self):
        self.client.send_message("?bad name")
        reply = self.client.read_message()
        self.assertEqual(reply.code, grammar.INVALID)

