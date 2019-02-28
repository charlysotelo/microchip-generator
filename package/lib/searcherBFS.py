class BFSStateWrapper:
    def __init__(self, state, depth=0):
        self.depth = depth
        self.state = state

    def is_goal(self):
        return self.state.is_goal()

    def generate_possible_actions(self):
        generated_actions = self.state.generate_possible_actions()
        return [BFSStateWrapper(x, depth=self.depth+1) for x in generated_actions]

    def __eq__(self, other):
        return self.state == other.state

class SearcherBFS:
    def __init__(self, initial_state, max_depth=1000):
        self.initial_state = BFSStateWrapper(initial_state)
        self.max_depth = max_depth

    def search(self):
        if self.initial_state.is_goal():
            return 0

        self.initial_state.depth = 0
        current_depth = 0
        open_set = [self.initial_state]
        closed_set = [] # Possibly hcange this to a dictionary and implement __hash_

        while len(open_set) > 0:
            current_node = open_set.pop(0)
            if current_node.depth >= self.max_depth:
                return None

            if current_depth < current_node.depth:
                print('Searched all nodes at depth {}'.format(current_depth))
                current_depth = current_node.depth

            generated_actions = current_node.generate_possible_actions()
            for generated_action in generated_actions:
                if generated_action.is_goal():
                    return generated_action.depth
                if generated_action in closed_set:
                    continue
                if not (generated_action in open_set):
                    open_set.append(generated_action)
            closed_set.append(current_node)
