from random import seed, random, sample, randint
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
solution = [] # sample(SETS, randint(0, SETS_AMT))
available_sets = [s for s in SETS if s not in solution]


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
    sol_len = len(solution)
    sets_len = len(sets)
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
    #   [WIP]

def tweak(solution: list[frozenset], sets: list[frozenset], current_fitness: float):
    new_sol = solution.copy()
    new_available_sets = sets.copy()

    min_op = 1
    max_op = 2

    if current_fitness < 0:
        operations_amt = -current_fitness * SETS_AMT / 2
        min_op = 0
        max_op = 0
    elif current_fitness <= 0.2:
        operations_amt = 3
    else:
        operations_amt = 2 * ceil(1 - current_fitness)

    idx = 0
    while idx < operations_amt:
        operation = randint(min_op, max_op)
        new_sol, new_available_sets = op_map[operation](new_sol, new_available_sets)
        idx += 1

    return new_sol, new_available_sets

# Hill Climber
current_fitness = fitness(solution)
print("INITIAL SOLUTION'S FITNESS:")
ic(fitness(solution))

MAX_STEPS = 255

history = [current_fitness]
step = 0
while step < MAX_STEPS:
    new_solution, new_sets = tweak(solution, available_sets, current_fitness)
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

print("\nFINAL SOLUTION:")
ic(solution, fitness(solution))

plt.figure(figsize = (14, 8))
plt.plot(
    range(len(history)),
    list(accumulate(history, max)),
    color = "red"
)

_ = plt.scatter(range(len(history)), history, marker = ".")
plt.show()