
#
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

import unittest
from copy import copy

from discosbackend import grammar

class TestMessage(unittest.TestCase):
    def setUp(self):
        self.request = grammar.Message(message_type = grammar.REQUEST,
                                       name = "req")
        self.reply = grammar.Message(message_type = grammar.REPLY,
                                     name = "req",
                                     code = grammar.OK)
    
    def test_is_request(self):
        self.assertTrue(self.request.is_request())
        self.assertFalse(self.reply.is_request())

    def test_is_correct_reply(self):
        self.assertTrue(self.reply.is_correct_reply(self.request))
        
    def test_is_wrong_reply_name(self):
        self.reply.name = "wrongname"
        self.assertFalse(self.reply.is_correct_reply(self.request))

    def test_is_wrong_reply_type(self):
        self.reply.message_type = "?"
        self.assertFalse(self.reply.is_correct_reply(self.request))

    def test_check_synthax_ok(self):
        self.assertTrue(self.reply.check_synthax())

    def test_check_synthax_bad_name(self):
        self.reply.name = "what a bad name!!"
        self.assertFalse(self.reply.check_synthax())

    def test_check_synthax_bad_message_type(self):
        self.reply.message_type = "^"
        self.assertFalse(self.reply.check_synthax())

    def test_check_synthax_bad_message_code(self):
        self.reply.code = "badcode"
        self.assertFalse(self.reply.check_synthax())


class TestParsing(unittest.TestCase):
    def test_good_request_pattern_without_arguments(self):
        match = grammar.request_pattern.match("?name")
        self.assertIsNotNone(match)

    def test_good_request_pattern_with_arguments(self):
        match = grammar.request_pattern.match("?name,arg1,arg2")
        self.assertIsNotNone(match)

    def test_good_reply_pattern_without_arguments(self):
        match = grammar.reply_pattern.match("!name,fail")
        self.assertIsNotNone(match)

    def test_good_reply_pattern_with_arguments(self):
        match = grammar.reply_pattern.match("!name,ok,arg1,arg2")
        self.assertIsNotNone(match)

    def test_trailing_cr_lf(self):
        message = grammar.parse_message("?ciao\r\n")
        self.assertTrue(message.check_synthax())
        self.assertEqual(message.name, "ciao")

    def test_trailing_cr_lf_with_arguments(self):
        message = grammar.parse_message("?ciao,arg1\r\n")
        self.assertTrue(message.check_synthax())
        self.assertEqual(message.name, "ciao")
        self.assertEqual(message.arguments[0], "arg1")

    def test_wrong_message_type(self):
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("#unusefulmessage")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("unusefulmessage")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message(" ?unusefulmessage")

    def test_wrong_message_name(self):
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("?-badrequest")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("?0badrequest")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("! badrequest")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("!bad?request")

    def test_wrong_reply_code(self):
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("!reply,notok")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("!reply,error")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("!reply, fail")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("!reply,ok ")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("!reply, invalid ")
        with self.assertRaises(grammar.GrammarException):
            grammar.parse_message("!reply,!invalid")

        
