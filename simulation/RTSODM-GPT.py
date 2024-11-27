import pygad
import numpy as np

# Simulation parameters
num_buses = 3
num_time_slots = 24  # 24 one-hour slots for simplicity
grid_limit = 300  # Grid limit in kWh per time slot
electricity_prices = np.random.rand(num_time_slots)  # Simulated price data
energy_demands = [588, 588, 588]  # kWh for each bus
time_slot_duration = 1  # Assume 1 hour for simplicity

# Randomize arrival and departure times for each bus
arrival_times = [np.random.randint(0, 12) for _ in range(num_buses)]  # Random arrival slots
departure_times = [np.random.randint(12, num_time_slots) for _ in range(num_buses)]  # Random departure slots

# Fitness function
def fitness_function(ga_instance, solution, solution_idx):
    penalty = 0
    charging_schedule = solution.reshape(num_buses, num_time_slots)  # kWh per time slot
    total_cost = 0

    for bus in range(num_buses):
        energy_delivered = 0
        for t in range(num_time_slots):
            if arrival_times[bus] <= t < departure_times[bus]:  # Check if the bus is available
                energy_delivered += charging_schedule[bus, t]
            elif charging_schedule[bus, t] > 0:  # Penalize charging outside availability
                penalty += 1000 * charging_schedule[bus, t]

        if energy_delivered < energy_demands[bus]:
            penalty += 1000 * (energy_demands[bus] - energy_delivered)  # Penalize unmet demand

        total_cost += np.sum(charging_schedule[bus] * electricity_prices)

    # Grid constraints
    total_energy_per_slot = np.sum(charging_schedule, axis=0)
    if np.any(total_energy_per_slot > grid_limit):
        penalty += 1000 * np.sum(total_energy_per_slot - grid_limit)

    return -1 * (total_cost + penalty)  # Minimize cost with penalties


# Explicitly mark unavailable times for each bus
gene_space = []
for bus in range(num_buses):
    bus_gene_space = []
    for t in range(num_time_slots):
        if arrival_times[bus] <= t < departure_times[bus]:
            bus_gene_space.append({'low': 0, 'high': grid_limit / num_buses})  # Allow charging
        else:
            bus_gene_space.append(0)  # Force zero when unavailable
    gene_space.extend(bus_gene_space)



# Initialize PyGAD
num_genes = num_buses * num_time_slots
ga_instance = pygad.GA(
    num_generations=50,
    num_parents_mating=5,
    fitness_func=fitness_function,
    sol_per_pop=20,
    num_genes=num_genes,
    gene_space=gene_space,  # Reasonable kWh range for each bus
    parent_selection_type="rank",
    crossover_type="single_point",
    mutation_type="random",
    mutation_percent_genes=2
)

ga_instance.run()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
charging_schedule = solution.reshape(num_buses, num_time_slots)
print("Optimal charging schedule (kWh):")
for bus in range(num_buses):
    print(f"Bus {bus + 1} (Arrival: {arrival_times[bus]}, Departure: {departure_times[bus]}):")
    print(charging_schedule[bus])
