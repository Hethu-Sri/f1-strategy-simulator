import matplotlib.pyplot as plt
from engine import RaceSimulator

sim = RaceSimulator()
_, laps = sim.simulate(pit_lap=20, start_compound="soft", next_compound="hard")

plt.plot(laps)
plt.title("Lap Time Evolution")
plt.xlabel("Lap")
plt.ylabel("Lap Time (s)")
plt.show()
