# LAB 2 - _Set Cover_ problem approached using a Hill Climber

- **Chosen Solution:** list of sets
- **Chosen Tweak:** adding, removal or swap of sets.
- **Stopping Method:** a `step` variable is incremented only if the state produced by the tweak is either illegal or has a smaller fitness compared to the previous solution. After a fixed amount of iterations, a random restart is performed, until a limit is reached.