"""
A 'set' is a collection of equivalent states.
We define a state Si of a set M as a two tuple (set_id, on_0, on_1).
set_id is the id of the set Si belongs to.
on_0 is the state Si transitions to on 0.
on_1 is the state Si transitions to on 1.
For any two states Si and Sj belonging to M,
Si.on_0.set_id == Sj.on_0.set_id and Si.on_1.set_id == Sj.on_1.set_id
We continue recalcutating the tuple until there are
changes in at least one of the sets.
"""

class State:

    identifier = 1

    def __init__(self):
        self.id_ = State.identifier
        State.identifier += 1
        self.set_id = 0
        self.on_0 = 0
        self.on_1 = 0

    def __str__(self):
        return "State %d: (%d, %d, %d)" % (self.id_, self.set_id, self.on_0.id_, self.on_1.id_)

    def __repr__(self):
        return "%d" % self.id_

def find_equivalent_states(states, combination_count):
    sets = []
    for i in range(combination_count):
        sets.append(set())
    for state in states:
        sets[state.set_id].add(state)
    print("Initial set:", sets)
    pass_count = 0
    while True:
        #print(sets)
        should_decide = set()
        for state_set in sets:
            for state1 in state_set:
                # if we already considered state1 or
                # state2 for removal, we're skipping them
                if state1 in should_decide:
                    continue
                for state2 in state_set:
                    if state2 in should_decide:
                        continue
                    if state1.id_ != state2.id_:
                        if state1.on_0.set_id != state2.on_0.set_id or \
                            state1.on_1.set_id != state2.on_1.set_id:
                                #print("Removing", state2, "from", state_set)
                                should_decide.add(state2)
            # if we have to modify at least one set, we're going to
            # apply the modification immediately and then
            # repeat this whole process in the next iteration
            if len(should_decide) > 0:
                state_set.difference_update(should_decide)
                break
        if len(should_decide) == 0:
            break
        # now for each of the states tbd, we'll try adding it to
        # an existing set. if we can't, we'll add a new set
        for state in should_decide:
            already_added = False
            for i, state_set in enumerate(sets):
                should_insert = False
                for existing in state_set:
                    # we need to compare the state tbd with only
                    # one item from the existing set in hand,
                    # because we already guaranteed that all
                    # the remaining items in this set transitions
                    # to the same equivalent sets
                    if state.on_0.set_id == existing.on_0.set_id and \
                            state.on_1.set_id == existing.on_1.set_id:
                        should_insert = True
                    break
                if should_insert:
                    state.set_id = i
                    state_set.add(state)
                    already_added = True
                    break
            if not already_added:
                # add a new set
                s = set()
                s.add(state)
                sets.append(s)
                # don't update the set id of the new state yet
        # now, update the set id for all remaining sets
        for state in should_decide:
            for i, state_set in enumerate(sets):
                if state in state_set:
                    state.set_id = i
                    break
        print("After pass %d:" % (pass_count + 1), sets)
        pass_count += 1
    return sets

def main():
    num_states = int(input("Enter number of states: "))
    states = []
    for i in range(num_states):
        states.append(State())
    print("Enter the transition table..")
    print("  State  \t\t Output")
    print("         \tI/P = 0\t\tI/P = 1")
    print("         \t NS  Z \t\t NS  Z")
    print("=========\t=======\t\t=======")
    # a dictionary to keep track of output combinations
    output_combinations = {}
    combination_count = 0
    for i in range(num_states):
        vals = input("State {:2}\t".format(i + 1))
        vals = vals.replace("\t", " ")
        parts = ' '.join(vals.split()).split(" ")
        on_0 = int(parts[0])
        on_1 = int(parts[2])
        op = parts[1] + parts[3]
        states[i].on_0 = states[on_0 - 1]
        states[i].on_1 = states[on_1 - 1]
        if op not in output_combinations:
            output_combinations[op] = combination_count
            combination_count += 1
        states[i].set_id = output_combinations[op]
    print("Final set:", find_equivalent_states(states, combination_count))

if __name__ == "__main__":
    main()
