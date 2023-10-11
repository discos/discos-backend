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
import logging
import unittest
import time
from multiprocessing import Process
from discosbackend.handlers import AlwaysOkHandler
from discosbackend.handlers import AlwaysFailHandler
from discosbackend.handlers import AlwaysRaiseHandler
from discosbackend.server import run_server
from discosbackend import grammar
from simple_client import SimpleClient
logger = logging.getLogger(__name__)

STARTING_PORT = 10000


def port_generator_function():
    port = STARTING_PORT
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('127.0.0.1', port)
        try:
            s.bind(address)
            s.close()
            time.sleep(0.01)
            yield port
        except OSError:
            pass
        port += 1


port_generator = port_generator_function()


class TestAlwaysOkServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = next(port_generator)
        cls._server = Process(
            target=run_server,
            args=(cls.port, AlwaysOkHandler())
        )
        cls._server.start()
        logger.info("SERVER LISTENING PID %d", cls._server.pid)
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls):
        logger.info("KILLING SERVER PID %d", cls._server.pid)
        cls._server.terminate()

    def setUp(self):
        self.client = SimpleClient(self.port)
        self.client.read_message()

    def test_good_request_without_argument(self):
        request = grammar.Message(
            message_type=grammar.REQUEST,
            name="prova"
        )
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertTrue(reply.is_correct_reply(request))
        self.assertEqual(reply.code, grammar.OK)

    def test_good_request_with_arguments(self):
        request = grammar.Message(
            message_type=grammar.REQUEST,
            name="prova",
            arguments=["arg1", "arg2"]
        )
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


class TestAlwaysFailServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = next(port_generator)
        cls._server = Process(
            target=run_server,
            args=(cls.port, AlwaysFailHandler())
        )
        cls._server.start()
        logger.info("SERVER LISTENING PID %d", cls._server.pid)
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls):
        logger.info("KILLING SERVER PID %d", cls._server.pid)
        cls._server.terminate()

    def setUp(self):
        self.client = SimpleClient(self.port)
        self.client.read_message()

    def test_incorrect_reply(self):
        request = grammar.Message(
            message_type=grammar.REQUEST,
            name="prova"
        )
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertTrue(reply.is_correct_reply(request))
        self.assertEqual(reply.code, grammar.FAIL)


class TestAlwaysRaiseServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = next(port_generator)
        cls._server = Process(
            target=run_server,
            args=(cls.port, AlwaysRaiseHandler())
        )
        cls._server.start()
        logger.info("SERVER LISTENING PID %d", cls._server.pid)
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls):
        logger.info("KILLING SERVER PID %d", cls._server.pid)
        cls._server.terminate()

    def setUp(self):
        self.client = SimpleClient(self.port)
        self.client.read_message()

    def test_incorrect_reply(self):
        request = grammar.Message(
            message_type=grammar.REQUEST,
            name="prova"
        )
        self.client.send_message(request)
        reply = self.client.read_message()
        self.assertTrue(reply.is_correct_reply(request))
        self.assertEqual(reply.code, grammar.FAIL)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
