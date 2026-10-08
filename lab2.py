from random import seed, random, sample, randint, choice
from matplotlib import pyplot as plt
from itertools import accumulate
from math import ceil
from icecream import ic

SETS_AMT = 1000
seed(42)

OBJECTS = frozenset(range(SETS_AMT))
SETS = tuple(frozenset(sample(range(SETS_AMT), k = s + 1)) for s in range(SETS_AMT))
COSTS = tuple(10*random() + (s + random()) ** 2 for s in range(SETS_AMT) )

XCOSTS = {SETS[i]: COSTS[i] for i in range(SETS_AMT)}
REF_COST = COSTS[-1]

# Solution as a list of sets
def get_solution(len: int):
    solution = sample(SETS, randint(0, len))
    available_sets = [s for s in SETS if s not in solution]
    return solution, available_sets

solution, available_sets = get_solution(0)


# Negative fitness for illegal states, positive fitness for legal states
def fitness(solution: list[frozenset]) -> float:
    covered = frozenset().union(*solution)
    if covered != OBJECTS:
        return len(covered) / SETS_AMT - 1
    return 1 / (1 + sum(XCOSTS[s] for s in solution) / REF_COST)

# Tweak: removal, adding or swap of a set

# Possible operations
def remove_random_set(solution: list[frozenset], sets: list[frozenset]):
    sol_len = len(solution)
    if sol_len != 0:
        rand_sol_idx = randint(0, sol_len - 1)
        removed = solution.pop(rand_sol_idx)
        sets.append(removed)

    return solution, sets

def add_random_set(solution: list[frozenset], sets: list[frozenset]):
    sets_len = len(sets)
    if sets_len != 0:
        rand_sets_idx = randint(0, len(sets) - 1)
        chosen = sets.pop(rand_sets_idx)
        solution.append(chosen)

    return solution, sets

def swap_random_set(solution: list[frozenset], sets: list[frozenset]):
    sets_len = len(sets)
    sol_len = len(solution)
    if sol_len != 0 and sets_len != 0:
        rand_sol_idx = randint(0, sol_len - 1)
        rand_sets_idx = randint(0, sets_len - 1)

        removed = solution.pop(rand_sol_idx)
        chosen = sets.pop(rand_sets_idx)

        solution.append(chosen)
        sets.append(removed)

    return solution, sets

op_map = {
    0: add_random_set,
    1: remove_random_set,
    2: swap_random_set
}

# Tweak
    # More operations are performed if the fitness is low (exploration)
    # Less operation are performed if the fitness is high (exploitation)
    # The fitness can range between -1 and 1, so the following arbitrary criterion has been chosen:

def get_tweak_parameters(current_fitness: float):
    min_op = 0
    max_op = 2

    if current_fitness < 0:
        operations_amt = 1
        min_op = 0
        max_op = 0
    elif current_fitness <= 0.2:
        operations_amt = 6 * ceil(1 - current_fitness)
    else:
        operations_amt = 1
    
    return min_op, max_op, operations_amt

def tweak(solution: list[frozenset], sets: list[frozenset], min_op: int, max_op: int, operations_amt: int):
    new_sol = solution.copy()
    new_available_sets = sets.copy()

    idx = 0
    while idx < operations_amt:
        operation = op_map[randint(min_op, max_op)]
        new_sol, new_available_sets = operation(new_sol, new_available_sets)
        idx += 1


    return new_sol, new_available_sets

# Hill Climber
current_fitness = fitness(solution)
print("INITIAL SOLUTION'S FITNESS:")
ic(current_fitness)

MAX_STEPS = 256

history = [current_fitness]
step = 0

MAX_RESTARTS = 16
restart_counter = 0
best_sol = solution
best_fitness = current_fitness
while restart_counter < MAX_RESTARTS:
    while step < MAX_STEPS:
        min_op, max_op, op_amt = get_tweak_parameters(current_fitness)
        new_solution, new_sets = tweak(solution, available_sets, min_op, max_op, op_amt)
        new_fitness = fitness(new_solution)

        history.append(new_fitness)

        if new_fitness < current_fitness:
            step += 1

        else:
            if new_fitness == current_fitness:
                step += 1
            else:
                step = 0

            solution = new_solution    
            current_fitness = new_fitness     
            available_sets = new_sets
        

    if current_fitness > best_fitness:
        best_sol = solution
        best_fitness = current_fitness

    # Restart procedure: the current solution is tweaked in a way to allow exploration of further areas
    # The number of operations decreases until a legal solution is found as a new starting point
    # this approach led to worse results than random restarts
    #new_fitness = -1
    #op_amt = .3 * SETS_AMT
    #while new_fitness < 0:
    #    new_solution, new_sets = tweak(solution, available_sets, 1, 2, max(op_amt, 0))
    #    new_fitness = fitness(new_solution)
    #    history.append(new_fitness)
    #   op_amt -= 1

    # Iterated local search from another random starting point
    solution, available_sets = get_solution(randint(0, SETS_AMT))
    current_fitness = fitness(solution)

    step = 0
    restart_counter += 1
        

print("\nFINAL SOLUTION:")
ic(fitness(best_sol))

plt.figure(figsize = (14, 8))
plt.plot(
    range(len(history)),
    list(accumulate(history, max)),
    color = "red"
)

_ = plt.scatter(range(len(history)), history, marker = ".")
plt.show()