
from random import random, sample
from icecream import ic

N = 10
OBJECTS = {n for n in range(N)}
SETS = tuple(frozenset(sample(range(N), k = s + 1)) for s in range(N))
COSTS = tuple(10*random() + (s + random()) ** 2 for s in range(N) )

print(SETS)
print(COSTS)