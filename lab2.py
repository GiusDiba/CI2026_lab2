
from random import seed, random, sample, randint
from matplotlib import pyplot as plt
from itertools import accumulate
from icecream import ic

N = 10
seed(42)

OBJECTS = {n for n in range(N)}
SETS = tuple(frozenset(sample(range(N), k = s + 1)) for s in range(N))
COSTS = tuple(10*random() + (s + random()) ** 2 for s in range(N) )

ic(SETS, COSTS)

XCOSTS = {SETS[i]: COSTS[i] for i in range(N)}

def isValid(solution: list[frozenset]) -> bool:
    return frozenset().union(*solution) == frozenset(range(N))

# Solution as a list of sets
solution = []
while not isValid(solution):
    solution = sample(SETS, randint(0, N))
    available_sets = [s for s in SETS if s not in solution]
ic(available_sets)

def fitness(solution: list[frozenset]) -> float:
    if len(solution) == 0:
        return -sum(COSTS) - 1
    return -sum(XCOSTS[s] for s in solution)

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
print("INITIAL SOLUTION:")
ic(solution, fitness(solution))

MAX_STEPS = 255

history = [fitness(solution)]
step = 0
while step < MAX_STEPS:
    new_solution, new_sets = tweak(solution, available_sets)

    history.append(fitness(solution))
    if isValid(new_solution) and fitness(new_solution) > fitness(solution):
        solution = new_solution.copy()
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