from decisionMaker import DecisionMaker
from datetime import timedelta
import pygad
import numpy as np
import matplotlib.pyplot as plt

class rtsoDM(DecisionMaker):

    def __init__(self, sim_state):
        super().__init__(sim_state)
        self.num_buses          = len(self.state.buses)
        self.num_time_slots     = self.__get_num_time_slots()
        self.energy_demands     = self.__get_energy_demands()
        self.grid_limit         = 500 # TODO: arbitrary value, test best input
        self.time_slot_duration = 1   # TODO: another arbitrary value, currently assumes time slots are hours
        self.electricity_prices = self.state.price_schedule.price_schedule
        self.arrival_times, self.departure_times    = self.__get_bus_times()
        self.charge_rate        = self.__get_charge_rates(self.__create_gene_space())
        self.cost = 0.0


    def update_chargers(self, timesteps) -> None:
        """
        update connector with charge rate and then
        deliver power to bus over timesteps
        """
        right_now = self.state.current_time 
        curr_power_price = self.state.price_schedule.get_current_price(right_now)


        for _ in range(timesteps):
            rate_step = (self.state.current_time - self.state.start_schedule).seconds // 3600
            for i, bus in enumerate(self.state.buses):
                # find connector with bus
                for charger in self.state.chargers:
                    for connector in charger.connectors:
                        if connector.connected_to == bus:
                            connector.update_charge_rate(self.charge_rate[i, rate_step])
                            power_delivered = connector.deliver_power(timesteps)
                            self.cost += curr_power_price * power_delivered


    def print_metrics(self):
        metrics = f"""
        number of buses: {self.num_buses}
        number of time slots: {self.num_time_slots}
        energy demand (per bus): {self.energy_demands}
        total grid pull limit: {self.grid_limit}
        time slot duration (hours): {self.time_slot_duration}
        electricity prices: {self.electricity_prices}
        bus arrival times: {self.arrival_times}
        bus departure times: {self.departure_times}
        charge rates for each bus:\n{self.charge_rate}
        """
        print(metrics)

    def __get_bus_times(self):

        arrival_times = []
        departure_times = []

        for bus in self.state.buses:
            arrival_times.append(bus.arrival_time)
            departure_times.append(bus.departure_time)

        return arrival_times, departure_times

    def __get_num_time_slots(self):
        """
        From the simstate stand and end schedule times, get the 
        number of hours in the simstate
        """
        return (self.state.end_schedule - self.state.start_schedule).seconds // 3600


    def __get_energy_demands(self):
        """
        calculate the energy demands for each bus based on their
        desired state of charge
        """
        energy_demands = []

        for bus in self.state.buses:
            energy_demands.append(bus.battery_capacity * (bus.desired_soc - bus.current_soc()))

        return energy_demands


    @staticmethod
    def __fitness_function(
            ga_instance, 
            solution, 
            solution_idx, 
            num_buses, 
            num_time_slots, 
            arrival_times, 
            departure_times, 
            energy_demands, 
            electricity_prices, 
            grid_limit,
            start_schedule
            ):
        """
        Fitness function for GA
        Decides if a gene is strong enough to live (low enough cost)
        """
        penalty = 0
        charging_schedule = solution.reshape(num_buses, num_time_slots)  # kWh per time slot
        total_cost = 0
    
        for bus in range(num_buses):
            energy_delivered = 0
            for t in range(num_time_slots):
                if charging_schedule[bus, t] < 0:  # Penalize negative charge rates
                    penalty += 1000 * abs(charging_schedule[bus, t])

                right_now = start_schedule + timedelta(hours=t)
                if arrival_times[bus] <= right_now < departure_times[bus]:  # Check if the bus is available
                    energy_delivered += charging_schedule[bus, t]
                elif charging_schedule[bus, t] > 0:  # Penalize charging outside availability
                    penalty += 1000 * charging_schedule[bus, t]
    
            if energy_delivered < energy_demands[bus]:
                penalty += 3000 * (energy_demands[bus] - energy_delivered)  # Penalize unmet demand
    
            total_cost += np.sum(charging_schedule[bus] * electricity_prices)
    
        # Grid constraints
        total_energy_per_slot = np.sum(charging_schedule, axis=0)
        if np.any(total_energy_per_slot > grid_limit):
            penalty += 1000 * np.sum(total_energy_per_slot - grid_limit)
    
        return -1 * (total_cost + penalty)  # Minimize cost with penalties


    def __create_gene_space(self):
        """
        set charge rate to 0 if bus will not be at charge
        otherwise, allow charging
        """
        # Explicitly mark unavailable times for each bus
        gene_space = []
        for bus in range(self.num_buses):
            bus_gene_space = []
            for t in range(self.num_time_slots):
                right_now = self.state.start_schedule + timedelta(hours=t)
                if self.arrival_times[bus] <= right_now < self.departure_times[bus]:
                    bus_gene_space.append({'low': 0, 'high': self.grid_limit / self.num_buses})  # Allow charging
                else:
                    bus_gene_space.append(0)  # Force zero when unavailable
            gene_space.extend(bus_gene_space)
        return gene_space


    def __get_charge_rates(self, gene_space):
        num_genes = self.num_buses * self.num_time_slots

        ga_instance = pygad.GA(
            num_generations=50,
            num_parents_mating=5,
            fitness_func=lambda ga, sol, idx: self.__fitness_function(
                ga, sol, idx, self.num_buses, self.num_time_slots, self.arrival_times,
                self.departure_times, self.energy_demands, self.electricity_prices, self.grid_limit,
                self.state.start_schedule
            ),
            sol_per_pop=20,
            num_genes=num_genes,
            gene_space=gene_space,
            parent_selection_type="rank",
            crossover_type="single_point",
            mutation_type="random",
            mutation_percent_genes=8
        )

        ga_instance.run()
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        charging_schedule = solution.reshape(self.num_buses, self.num_time_slots)

        return charging_schedule


    def plot_bus_charge_rates(self):
        for i, row in enumerate(self.charge_rate):
            plt.plot(row, label=f"bus {i}")
        plt.xlabel("hour of charge session")
        plt.ylabel("power to deliver (kWh)")
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def plot_total_charge_rate(self):
        totals = [0 for _ in self.charge_rate[0]]
        for charge_rate in self.charge_rate:
            for i, element in enumerate(charge_rate):
                totals[i] += element
        plt.plot(totals)
        plt.xlabel("hour of charge session")
        plt.ylabel("total power delivered (kWh)")
        plt.grid(True)
        plt.show()

