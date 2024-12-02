from decisionMaker import DecisionMaker
from simspace import SimState
from datetime import timedelta
import matplotlib.pyplot as plt
import typing
class NaiveDM(DecisionMaker):
    def __init__(self, sim_state):
        super().__init__(sim_state)
        self.charge_rate = [[] for bus in self.state.buses]

    def update_chargers(self, timesteps) -> None:
        self.__calc_charge_rates()
        for charger in self.state.chargers:
            for connector in charger.connectors:
                connector.deliver_power(timesteps)

    def __calc_charge_rates(self) -> None: 
        right_now = self.state.current_time
        for charger in self.state.chargers:
            for connector in charger.connectors:
                if connector.connected_to != None:
                    bus = connector.connected_to
                    if bus.current_soc() >= bus.desired_soc:
                        connector.update_charge_rate(0)
                        self.charge_rate[bus.id].append(0)
                    else:
                        hours_remaining = (bus.departure_time - right_now).seconds // 3600
                        soc_delta = bus.desired_soc - bus.current_soc()
                        charge_needed = abs(soc_delta - bus.desired_soc) 
                        # calculate lowest charge rate which will charge the bus by the desired end time
                        if hours_remaining == 0:
                            connector.update_charge_rate(0)
                        else:
                            charge_rate = ((charge_needed * bus.battery_capacity) / hours_remaining) * 1000
                            connector.update_charge_rate(charge_rate)


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

