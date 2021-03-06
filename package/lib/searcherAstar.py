import heapq
import math

def _heuristic_cost1(state):
    return 0

def _heuristic_cost2(state):
    return state.state.num_floors - 1 - state.state.elevator_level

def _heuristic_cost3(state):
    # Clearly if there are 4 items in a floor, it will take at least
    # 1.5 Roundtrips, since we can fit at most 2 items in the elevator
    # If there are N items, it will take N/2 * 1 RTT  - 0.5 RTT 
    floor_number = 1
    total = 0
    for (generator_list, microchip_list) in state.state.floors_list:
        round_trip_length = 2 * (state.state.num_floors - 1 - floor_number)
        number_of_items = len(generator_list) + len(microchip_list)
        tt = round_trip_length * math.ceil(number_of_items / 2)
        tt = tt - round_trip_length / 2
        total += tt
        floor_number += 1
    return total 

def _estimated_total_cost(state):
    return state.depth + max([_heuristic_cost1(state),
                              _heuristic_cost2(state),
                              _heuristic_cost3(state)])

class AstarStateWrapper:
    def __init__(self, state, depth=0):
        self.state = state
        self.depth = depth

    # WARNING: Playing a dangerous game here saying that two things can be equal and
    # also one less than the other!:

    # Less than is implemented puerly for heap functions.
    def __lt__(self, other):
        return _estimated_total_cost(self) < _estimated_total_cost(other)
   
    # The following 3 are used purely for set operations
    def __eq__(self, other):
        return self.state == other.state
    
    def __ne__(self, other):
        return not (self.state == other.state)
 
    def __hash__(self):
        return hash(self.state)

    def is_goal(self):
        return self.state.is_goal()

    def generate_possible_actions(self):
        generated_actions = self.state.generate_possible_actions()
        return [AstarStateWrapper(x, depth=self.depth+1) for x in generated_actions]

class SearcherAstar:
    def __init__(self, initial_state, max_depth=1000):
        self.initial_state = initial_state
        self.max_depth = max_depth
    
    def search(self):
        if self.initial_state.is_goal():
            return 0
        
        open_set = []
        closed_set = set() 
        heapq.heappush(open_set,
                       AstarStateWrapper(self.initial_state))
        current_depth = 0
        while len(open_set) > 0:
            current_node = heapq.heappop(open_set)
            if current_node.depth >= self.max_depth:
                return None

            if current_node.depth > current_depth:
                current_depth = current_node.depth
                print('Depth is {}'.format(current_depth))

            if current_node in closed_set:
                continue    

            if current_node.is_goal():
                return current_node.depth

            generated_actions = current_node.generate_possible_actions()
            for generated_action in generated_actions:
                if generated_action in closed_set:
                    continue
                heapq.heappush(open_set, generated_action)
            closed_set.add(current_node)
