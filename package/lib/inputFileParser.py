import copy
import re

from package.lib.state import State

class Parser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        with open(self.filepath) as f:
            initial_state = []
            for line in f:
                generators = re.findall(r' an? (\S*?) generator', line)
                microchips = re.findall(r' an? (\S*?)-compatible microchip',
                                        line)
                initial_state.append((generators, microchips))
        return State(initial_state)
