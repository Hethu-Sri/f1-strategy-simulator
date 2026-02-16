import numpy as np
import random

class RaceSimulator:

    def __init__(self, total_laps=50):
        self.total_laps = total_laps
        self.pit_loss = 22
        self.fuel_factor = 2.5

    def degradation(self, compound, laps_on_tire):
        if compound == "soft":
            return 0.09 * (laps_on_tire ** 1.35)
        elif compound == "medium":
            return 0.06 * (laps_on_tire ** 1.2)
        elif compound == "hard":
            return 0.035 * (laps_on_tire ** 1.1)

    def fuel_penalty(self, current_lap):
        remaining_ratio = (self.total_laps - current_lap) / self.total_laps
        return self.fuel_factor * remaining_ratio

    def warmup_penalty(self, laps_on_tire):
        if laps_on_tire == 1:
            return 0.4
        elif laps_on_tire == 2:
            return 0.2
        return 0

    def simulate(self, pit_lap=20, start_compound="medium", next_compound="hard"):

        base_time = 80
        total_time = 0
        laps_on_tire = 0
        compound = start_compound

        lap_times = []

        for lap in range(1, self.total_laps + 1):

            if lap == pit_lap:
                total_time += self.pit_loss
                compound = next_compound
                laps_on_tire = 0

            laps_on_tire += 1

            fuel = self.fuel_penalty(lap)
            deg = self.degradation(compound, laps_on_tire)
            warm = self.warmup_penalty(laps_on_tire)
            noise = random.uniform(-0.15, 0.15)

            lap_time = base_time + fuel + deg + warm + noise

            total_time += lap_time
            lap_times.append(lap_time)

        return total_time, lap_times

def optimize_pit_window():
    sim = RaceSimulator()
    best_time = float("inf")
    best_lap = None

    for pit in range(10, 35):
        avg_time = np.mean([sim.simulate(pit_lap=pit)[0] for _ in range(100)])
        if avg_time < best_time:
            best_time = avg_time
            best_lap = pit

    print("Optimal Pit Lap:", best_lap)
    print("Expected Race Time:", round(best_time, 2))


def monte_carlo(pit_lap, runs=200):
    sim = RaceSimulator()
    results = []
    
    for _ in range(runs):
        total, _ = sim.simulate(pit_lap=pit_lap)
        results.append(total)
    
    return np.mean(results)


def compare_strategies():
    strategies = [15, 20, 25, 30]
    
    for pit in strategies:
        avg_time = monte_carlo(pit)
        print(f"Pit Lap {pit}: Avg Time = {round(avg_time,2)}")

if __name__ == "__main__":
     compare_strategies()

