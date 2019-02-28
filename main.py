#!/usr/bin/python3

import logging
import sys

from package.lib.inputFileParser import Parser
from package.lib.searcherBFS import SearcherBFS
from package.lib.searcherAstar import SearcherAstar

# Parse input argument
if (len(sys.argv) != 2):
    print('Usage: ./main.py <filepath>')
    sys.exit(1)

state = Parser(sys.argv[1]).parse()
number_of_steps = SearcherAstar(state).search()
#number_of_steps = SearcherBFS(state).search()
print('Number of steps {}'.format(number_of_steps))
