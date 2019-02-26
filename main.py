#!/usr/bin/python3

import logging
import sys

from package.lib.inputFileParser import Parser


# Parse input argument
if (len(sys.argv) != 2):
    print("Usage: ./main.py <filepath>")
Parser(sys.argv[1])	
