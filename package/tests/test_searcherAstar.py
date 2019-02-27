import unittest

from package.lib.searcherAstar import SearcherAstar
from package.lib.state import State

class TestSearcherAstar(unittest.TestCase):
    def test_search1(self):
        state = State([(["helium"],["helium"]), (["hydrogen"],["hydrogen"])])
        self.assertEqual(SearcherAstar(state).search(), 1)
    def test_search2(self):
        state = State([([],[]), (["hydrogen"],["hydrogen"])])
        state.elevator_level = state.max_floor_number
        self.assertEqual(SearcherAstar(state).search(), 0)
    def test_search3(self):
        state = State([([],["lithium", "helium", "hydrogen"]), (["hydrogen", "helium", "lithium"],[])])
        self.assertEqual(SearcherAstar(state).search(), 3)
