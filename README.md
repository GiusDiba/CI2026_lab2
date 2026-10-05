# LAB 2 - _Set Cover_ problem approached using a Hill Climber

- **Chosen Solution:** list of sets
- **Chosen Tweak:** adding, removal or swap of sets.
- **Stopping Method:** a `step` variable is incremented only if the state produced by the tweak is either illegal or has a smaller fitness compared to the previous solution, and is used as a stop criterion