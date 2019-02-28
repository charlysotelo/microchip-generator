import heapq
import math

def _heuristic_cost1(state):
    return 0

def _heuristic_cost2(state):
    return state.state.max_floor_number - state.state.elevator_level

def _heuristic_cost3(state):
    # Clearly if there are 4 items in a floor, it will take at least
    # 1.5 Roundtrips, since we can fit at most 2 items in the elevator
    # If there are 6 items, it will take N/2 * 1 RTT  - 0.5 RTT if there were 4 
    floor_number = 1
    total = 0
    for (generator_list, microchip_list) in state.state.floors_list:
        round_trip_length = 2 * (state.state.max_floor_number - floor_number)
        number_of_items = len(generator_list) + len(microchip_list)
        tt = round_trip_length * math.ceil(number_of_items / 2)
        tt = tt - round_trip_length / 2
        #tt = tt + abs(floor_number - state.state.elevator_level)
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

    def __lt__(self, other):
        return _estimated_total_cost(self) < _estimated_total_cost(other)

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
        closed_set = [] # Warning, only store non-wrapped states here
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

            if current_node.is_goal():
                return current_node.depth

            generated_actions = current_node.generate_possible_actions()
            for generated_action in generated_actions:
                if generated_action.state in closed_set:
                    continue
                if not (generated_action in open_set):
                    heapq.heappush(open_set, generated_action)
                else: #TODO modify prioirty here?
                    pass 
            closed_set.append(current_node.state)
