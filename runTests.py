#!/usr/bin/python3

import unittest

from package.tests.test_inputFileParser import TestParser
from package.tests.test_state import TestState
from package.tests.test_searcherBFS import TestSearcherBFS
from package.tests.test_searcherAstar import TestSearcherAstar

test_classes = [
    TestParser,
    TestState,
    TestSearcherBFS,
    TestSearcherAstar,
]
suite_collection = []
for test_class in test_classes:
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    suite_collection.append(suite)
suite = unittest.TestSuite(suite_collection)

unittest.TextTestRunner(verbosity=2).run(suite)
