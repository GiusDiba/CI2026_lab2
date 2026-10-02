
from random import seed, random, sample, randint
from collections.abc import Sequence
from icecream import ic

N = 10
seed(42)

OBJECTS = {n for n in range(N)}
SETS = tuple(frozenset(sample(range(N), k = s + 1)) for s in range(N))
COSTS = tuple(10*random() + (s + random()) ** 2 for s in range(N) )

print(SETS)
print(COSTS)

# Solution as a list of sets
XCOSTS = {SETS[i]: COSTS[i] for i in range(N)}
SOL_SIZE = 5

solution = sample(SETS, k = SOL_SIZE)
available_sets = [s for s in SETS if s not in solution]
ic(available_sets)

def fitness(solution: list[frozenset]) -> list[frozenset]:
    return -sum(XCOSTS[s] for s in solution)

# Tweak: swapping a set from the solution with one from the remaining available sets
def tweak(solution: list[frozenset], sets: list[frozenset]):
    rand_sol_idx = randint(0, SOL_SIZE - 1)
    rand_sets_idx = randint(0, len(sets) - 1)

    new_sol = solution.copy()
    new_available_sets = sets.copy()

    removed = new_sol.pop(rand_sol_idx)
    chosen = new_available_sets.pop(rand_sets_idx)

    new_sol.append(chosen)
    new_available_sets.append(removed)

    return new_sol, new_available_sets

def isValid(solution: list[frozenset]) -> bool:
    return frozenset.union(*solution) == frozenset(range(N))

# Hill Climber
print("INITIAL SOLUTION:")
ic(solution, fitness(solution))

MAX_STEPS = 255

step = 0
while step < MAX_STEPS:
    new_solution, new_sets = tweak(solution, available_sets)

    if isValid(new_solution) and fitness(new_solution) > fitness(solution):
        solution = new_solution.copy()
        available_sets = new_sets.copy()
    else:
        step += 1

print("\nFINAL SOLUTION:")
ic(solution, fitness(solution))