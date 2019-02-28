import copy
import bisect

class State:
    def __init__(self, raw_floor_list=[]):
        self.item_number_map = {} # Maps item name to number
        self.number_item_map = {} # Maps item name to number
        self.floors_list = []
        self.elevator_level = 1
        
        # Enumerate all items to provide canonical representation
        self._enumerate_items(raw_floor_list)
        self._create_canonical_state(raw_floor_list)
        self.max_floor_number = len(self.floors_list)

    def generate_possible_actions(self):
        # Generate all possibilities:
        possible_actions = []
        
        # Possible Directions: up and down
        # Note this only checks floor bounds
        directions = []
        can_go_up = (self.elevator_level + 1) <= self.max_floor_number
        can_go_down = (self.elevator_level - 1) >= 1

        if can_go_up:
            directions.append(1)
        if can_go_down:
            directions.append(-1)
       
        (generator_list, microchip_list) = self.floors_list[self.elevator_level - 1]
        for direction in directions:
            target_floor = self.elevator_level + direction
            (target_gen_list, target_mic_list) = self.floors_list[target_floor - 1]
            trgt_unpaired_mics = [m for m in target_mic_list if not (m in target_gen_list)]
            # Generate next states where we move a microchip
            for i in range(len(microchip_list)):
                one_item_move_state = copy.deepcopy(self)
                one_item_move_state._move_item(microchip_list[i], 1,
                             self.elevator_level, target_floor)
                one_item_move_state.elevator_level = target_floor

                # Generate the next state for moving a single microchip only if
                # does not make the state invalid
                if ((len(target_gen_list) == 0) or
                    microchip_list[i] in target_gen_list):
                    possible_actions.append(one_item_move_state)
                
                    # Generate the next state where we move two microchips. Notice
                    # this is only possible if we succeeded in generateing a state
                    # with only the first microchip moved 
                    for j in range(i + 1, len(microchip_list)):

                        # Generate state only if moving second chip does not make
                        # the state invalid
                        if ((not (microchip_list[j] in target_gen_list)) and
                            len(target_gen_list) > 0):
                            continue
                    
                        two_item_move_state = copy.deepcopy(one_item_move_state)
                        two_item_move_state._move_item(microchip_list[j], 1,
                                     self.elevator_level, target_floor)
                        possible_actions.append(two_item_move_state)
                else:
                    # cannot match a microchip with anything but a compatible genny
                    if microchip_list[i] in generator_list:
                        two_item_move_state = copy.deepcopy(one_item_move_state)
                        two_item_move_state._move_item(microchip_list[i], 0,
                                     self.elevator_level, target_floor)
                        possible_actions.append(two_item_move_state)

            if len(trgt_unpaired_mics) <= 2:
                if len(trgt_unpaired_mics) == 0:
                    for i in range(len(generator_list)):
                        one_item_move_state = copy.deepcopy(self)
                        one_item_move_state._move_item(generator_list[i], 0,
                                     self.elevator_level, target_floor)
                        one_item_move_state.elevator_level = target_floor
                        possible_actions.append(one_item_move_state)

                        for j in range(i + 1, len(generator_list)):
                            two_item_move_state = copy.deepcopy(one_item_move_state)
                            two_item_move_state._move_item(generator_list[j], 0,
                                        self.elevator_level, target_floor)
                            possible_actions.append(two_item_move_state)
                elif len(trgt_unpaired_mics) <= 2: # Cant be 0 at this point
                    if trgt_unpaired_mics[0] in generator_list:
                        one_item_move_state = copy.deepcopy(self)
                        one_item_move_state._move_item(trgt_unpaired_mics[0], 0,
                                        self.elevator_level, target_floor)
                        one_item_move_state.elevator_level = target_floor
                        
                        if len(trgt_unpaired_mics) == 1:
                            possible_actions.append(one_item_move_state)
                            other_gens = [x for x in generator_list if x != trgt_unpaired_mics[0]]
                            for other_gen in other_gens:
                                two_item_move_state = copy.deepcopy(one_item_move_state)
                                two_item_move_state._move_item(other_gen, 0,
                                            self.elevator_level, target_floor)
                                possible_actions.append(two_item_move_state)
                        elif trgt_unpaired_mics[1] in generator_list: # 2 unpaired microchips
                            two_item_move_state = copy.deepcopy(one_item_move_state)
                            two_item_move_state._move_item(trgt_unpaired_mics[1], 0,
                                            self.elevator_level, target_floor)
                            possible_actions.append(two_item_move_state)
        return possible_actions #TODO: prune already seen states and isomorphic states       

    def is_valid(self):
        # WARNING:
        # Can a single RTG power multiple microchips of the same type???
        # This needs to be clarified!!!
        # Im going with the assumption that yes it can!
        # Note this does not make a difference if more than one RTG or microchip
        # of one type is not allowed
        
        # If there is a generator in this floor, ensure all microchips
        # have a compatiblef RTG to power their shield
        for (generator_list, microchip_list) in self.floors_list:
            if len(generator_list) > 0:
                for microchip in microchip_list:
                    if not (microchip in generator_list):
                        return False
        return True
            
    def is_goal(self):
        if self.elevator_level != self.max_floor_number:
            return False

        # if there are items on a non-max floor level, we are not in goal
        for i in range(1, self.max_floor_number):
            (generator_list, microchip_list) = self.floors_list[i - 1]
            items_list = generator_list + microchip_list
            if len(items_list) > 0:
                return False
        return True

    def _move_item(self, item_number, item_type, src_floor, target_floor):
        self.floors_list[src_floor - 1][item_type].remove(item_number)
        bisect.insort(self.floors_list[target_floor - 1][item_type], item_number)

    def __deepcopy__(self, memo):
        new_state = State()
        new_state.elevator_level = self.elevator_level
        new_state.max_floor_number = self.max_floor_number
        memo[id(self)] = self
        new_state.item_number_map = copy.deepcopy(self.item_number_map, memo)
        new_state.number_item_map = copy.deepcopy(self.number_item_map, memo)
        new_state.floors_list = copy.deepcopy(self.floors_list, memo)
        return new_state

    def _enumerate_items(self, raw_floor_list):
        # Flatten list and gather unique items
        flattened_list = []
        for (generator_list, microchip_list) in raw_floor_list:
            flattened_list += generator_list + microchip_list
        item_set = set(flattened_list)
       
        # Create item to number map. Note this maps both generators and
        # microchips to the same number. 
        item_number = 0
        for item in item_set:
            self.item_number_map[item] = item_number
            self.number_item_map[item_number] = item
            item_number += 1
    
    def _create_canonical_state(self, raw_floor_list):
        for (generator_list, microchip_list) in raw_floor_list:
            g = [self.item_number_map[generator] for generator in generator_list]
            m = [self.item_number_map[microchip] for microchip in microchip_list]
            self.floors_list.append((sorted(g), sorted(m)))

    def __eq__(self, other):
        return (self.floors_list == other.floors_list and
                self.elevator_level == other.elevator_level)

    def __str__(self):
        result = ''
        floor_number = 1
        for (generator_list, microchip_list) in self.floors_list:
            result += 'Floor {}:\n'.format(floor_number)
            result += 'Generators:\n'
            for generator in generator_list:
                result += '{}\n'.format(self.number_item_map[generator])
            result += '\nMicrochips:\n'
            for microchip in microchip_list:
                result += '{}\n'.format(self.number_item_map[microchip])
            result += '\n'
            floor_number += 1
        result += 'Elevator Level {}'.format(self.elevator_level)
        return result
