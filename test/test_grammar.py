import unittest

from discosbackend import grammar

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

        
