import unittest

from package.lib.searcherBFS import SearcherBFS
from package.lib.state import State

class TestSearcherBFS(unittest.TestCase):
    def test_search1(self):
        state = State([(["helium"],["helium"]), (["hydrogen"],["hydrogen"])])
        self.assertEqual(SearcherBFS(state).search(), 1)
    def test_search2(self):
        state = State([([],[]), (["hydrogen"],["hydrogen"])])
        state.elevator_level = state.num_floors - 1
        self.assertEqual(SearcherBFS(state).search(), 0)
    def test_search3(self):
        state = State([([],["lithium", "helium", "hydrogen"]), (["hydrogen", "helium", "lithium"],[])])
        self.assertEqual(SearcherBFS(state).search(), 3)
