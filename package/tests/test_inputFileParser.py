import unittest

from package.lib.inputFileParser import Parser

class TestParser(unittest.TestCase):
    def test_parse(self):
        state = Parser('package/tests/testInput.txt').parse()
