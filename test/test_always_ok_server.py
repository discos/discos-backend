import unittest
from twisted.internet import reactor

from discosbackend.handlers import AlwaysOkHandler
from discosbackend.server import run_server
from discosbackend import grammar

from simple_client import SimpleClient

TCP_PORT = 8988

class TestAlwaysOkServer(unittest.TestCase):

    def setUp(self):
        self.client = SimpleClient(TCP_PORT)

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

