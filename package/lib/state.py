import copy
import bisect

GENY = 0
CHIP = 1

UP = 1
DOWN = -1

class State:
    def __init__(self, raw_floor_list=[]):
        # Format of floors_list: 
        # (floor1, floor2, ....)
        # floori = (gens, chips)
        # gens = (gen1, gen2, ...)
        # chips = (chip1, chip2, ...)
        # gen/chip = floor number of matching chip/gen 
        self.floors_list = None
        self.elevator_level = 0
        self.num_floors = len(raw_floor_list)
        self._anonymize_items(raw_floor_list)

    def _can_move_in_direction(self, direction):
        if direction == UP:
            return self.elevator_level < self.num_floors - 1
        elif direction == DOWN:
            return self.elevator_level > 0

    def generate_possible_actions(self):
        # Generate all possibilities:
        possible_actions = []

        # Code is a little verbose to prevent generating unnecessary states.
        # There are only 4 types of possible next states to generate, sans up/down: 
        # M, G, MM, GG, GM (microchip, generator, microchip-microchip, etc...)
        # each case has restriction conditions.
        # M can only move to a floor with no conflicting gennys or a matching geny
        # G can only move to a floor with no non-matched chips, unless G matches M
        # etc...      
        directions = [x for x in [UP, DOWN] if self._can_move_in_direction(x)]
        (generator_list, microchip_list) = self.floors_list[self.elevator_level]
        for direction in directions:
            dst_floor = self.elevator_level + direction
            (dst_gen_list, dst_mic_list) = self.floors_list[dst_floor]
            dst_unpaired_mics = [m for m in dst_mic_list if m != dst_floor]
            # Generate next states where we move a microchip
            for i in range(len(microchip_list)):
                one_item_move_state = copy.copy(self)
                one_item_move_state._move_item(microchip_list[i], CHIP,
                             self.elevator_level, dst_floor)
                one_item_move_state.elevator_level = dst_floor

                # Generate the next state for moving a single microchip only if
                # it does not make the state invalid
                if ((len(dst_gen_list) == 0) or
                    microchip_list[i] == dst_floor):
                    possible_actions.append(one_item_move_state)
                
                    # Generate the next state where we move two microchips. Notice
                    # this is only possible if we succeeded in generating a state
                    # with only the first microchip moved 
                    for j in range(i + 1, len(microchip_list)):

                        # Generate state only if moving second chip does not make
                        # the state invalid
                        if ((microchip_list[j] != dst_floor) and
                            (len(dst_gen_list) > 0)):
                            continue
                    
                        two_item_move_state = copy.copy(one_item_move_state)
                        two_item_move_state._move_item(microchip_list[j], CHIP,
                                     self.elevator_level, dst_floor)
                        possible_actions.append(two_item_move_state)
                else:
                    # cannot match a microchip with anything but a compatible genny
                    if microchip_list[i] == self.elevator_level:
                        two_item_move_state = copy.copy(one_item_move_state)
                        two_item_move_state._move_item(dst_floor, GENY,
                                     self.elevator_level, dst_floor)
                        possible_actions.append(two_item_move_state)

            if len(dst_unpaired_mics) <= 2:
                if len(dst_unpaired_mics) == 0:
                    for i in range(len(generator_list)):
                        one_item_move_state = copy.copy(self)
                        one_item_move_state._move_item(generator_list[i], GENY,
                                     self.elevator_level, dst_floor)
                        one_item_move_state.elevator_level = dst_floor
                        possible_actions.append(one_item_move_state)

                        for j in range(i + 1, len(generator_list)):
                            two_item_move_state = copy.copy(one_item_move_state)
                            two_item_move_state._move_item(generator_list[j], GENY,
                                        self.elevator_level, dst_floor)
                            possible_actions.append(two_item_move_state)
                elif len(dst_unpaired_mics) <= 2: # Cant be 0 at this point
                    if dst_unpaired_mics[0] == self.elevator_level:
                        one_item_move_state = copy.copy(self)
                        one_item_move_state._move_item(dst_floor, GENY,
                                        self.elevator_level, dst_floor)
                        one_item_move_state.elevator_level = dst_floor
                        
                        if len(dst_unpaired_mics) == 1:
                            possible_actions.append(one_item_move_state)
                            other_gens = [x for x in generator_list if x != dst_floor]
                            for other_gen in other_gens:
                                two_item_move_state = copy.copy(one_item_move_state)
                                two_item_move_state._move_item(other_gen, GENY,
                                            self.elevator_level, dst_floor)
                                possible_actions.append(two_item_move_state)
                        elif dst_unpaired_mics[1] == self.elevator_level: # 2 unpaired microchips
                            two_item_move_state = copy.copy(one_item_move_state)
                            two_item_move_state._move_item(dst_floor, GENY,
                                            self.elevator_level, dst_floor)
                            possible_actions.append(two_item_move_state)
        return possible_actions
      
    def is_goal(self):
        if self.elevator_level != self.num_floors - 1:
            return False

        # if there are items on a non-max floor level, we are not in goal
        for i in range(self.num_floors - 1):
            (generator_list, microchip_list) = self.floors_list[i]
            items_list = generator_list + microchip_list
            if len(items_list) > 0:
                return False
        return True

    def _move_item(self, item_number, item_type, src_floor, target_floor):
        def tuple2list(a):
            return list((tuple2list(x) if isinstance(x, tuple) else x for x in a))

        def list2tuple(a):
            return tuple((list2tuple(x) if isinstance(x, list) else x for x in a))

        other_item_type = GENY if item_type is CHIP else CHIP
        
        # Tuples are immutable, so we must do this dance:
        floors_list = tuple2list(self.floors_list)
        # Move item out
        floors_list[src_floor][item_type].remove(item_number)
       
        # Insert item into target floor 
        bisect.insort(floors_list[target_floor][item_type], item_number)

        # Update matching item with the floor number of match
        floors_list[item_number][other_item_type].remove(src_floor)
        bisect.insort(floors_list[item_number][other_item_type], target_floor)
        self.floors_list = list2tuple(floors_list)        

    def _anonymize_items(self, raw_floor_list):
        # Make every item point to the floor of its matching item
        chips_per_floor = [microchips for (generators, microchips) in raw_floor_list]
        genys_per_floor = [generators for (generators, microchips) in raw_floor_list]
        for chip_floor_index in range(self.num_floors):
            chips = chips_per_floor[chip_floor_index]
            for chip_index in range(len(chips)):
                chip = chips[chip_index]
                for geny_floor_index in range(self.num_floors):
                    if chip in genys_per_floor[geny_floor_index]:
                        geny_index = genys_per_floor[geny_floor_index].index(chip)
                        raw_floor_list[chip_floor_index][CHIP][chip_index] = geny_floor_index
                        raw_floor_list[geny_floor_index][GENY][geny_index] = chip_floor_index
        # Make it a tuple so it is hashable
        self.floors_list = ()
        for (genys, chips) in raw_floor_list:
            self.floors_list += ((tuple(sorted(genys)), tuple(sorted(chips))),)
    
    def __eq__(self, other):
        return (self.floors_list == other.floors_list and
                self.elevator_level == other.elevator_level)

    def __hash__(self):
        return hash((self.floors_list, self.elevator_level))
