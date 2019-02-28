import unittest

from package.lib.state import State

class TestState(unittest.TestCase):
    def test_generate1(self):
        state = State([(["helium"],["helium"]), (["hydrogen"],["hydrogen"])])
        generated_states = state.generate_possible_actions()
        self.assertEqual(len(generated_states), 2) 
    
    def test_generate2(self):
        state = State([([],[]), ([],[])])
        generated_states = state.generate_possible_actions()
        self.assertEqual(len(generated_states), 0)

    def test_is_goal1(self):
        state = State([(["1"],["1"]), (["2"],["2"])])
        self.assertFalse(state.is_goal())
    
    def test_is_goal2(self):
        state = State([([],[]), (["2"],["2"])])
        state.elevator_level = state.num_floors - 1
        self.assertTrue(state.is_goal())
