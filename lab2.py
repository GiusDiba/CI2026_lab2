
from random import seed, random, sample, randint
from matplotlib import pyplot as plt
from itertools import accumulate
from icecream import ic

SETS_AMT = 1000
seed(42)

OBJECTS = frozenset(range(SETS_AMT))
SETS = tuple(frozenset(sample(range(SETS_AMT), k = s + 1)) for s in range(SETS_AMT))
COSTS = tuple(10*random() + (s + random()) ** 2 for s in range(SETS_AMT) )

XCOSTS = {SETS[i]: COSTS[i] for i in range(SETS_AMT)}
COSTS_SUM = sum(COSTS)

# Solution as a list of sets
solution = [] # sample(SETS, randint(0, SETS_AMT))
available_sets = [s for s in SETS if s not in solution]


# Negative fitness for illegal states, positive fitness for legal states
def fitness(solution: list[frozenset]) -> float:
    covered = frozenset().union(*solution)
    if covered != OBJECTS:
        return len(covered) / SETS_AMT - 1
    return 1 - sum(XCOSTS[s] for s in solution) / COSTS_SUM

# Tweak: random removal, adding or swap of a set

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
    0: remove_random_set,
    1: add_random_set,
    2: swap_random_set
}

# Tweak
def tweak(solution: list[frozenset], sets: list[frozenset]):
    new_sol = solution.copy()
    new_available_sets = sets.copy()

    while random() < 0.8:
        operation = randint(0, 2)
        new_sol, new_available_sets = op_map[operation](new_sol, new_available_sets)
    
    return new_sol, new_available_sets

# Hill Climber
current_fitness = fitness(solution)
print("INITIAL SOLUTION'S FITNESS:")
ic(fitness(solution))

MAX_STEPS = 255

history = [current_fitness]
step = 0
while step < MAX_STEPS:
    new_solution, new_sets = tweak(solution, available_sets)
    new_fitness = fitness(new_solution)

    history.append(fitness(new_solution))
    if new_fitness > current_fitness:
        solution = new_solution.copy()
        current_fitness = fitness(solution)
        available_sets = new_sets.copy()
        step = 0
    else:
        step += 1

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