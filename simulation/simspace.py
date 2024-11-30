from bus import Bus
from charger import Charger
from priceSchedule import PriceSchedule
import numpy as np
from datetime import datetime, timedelta
from typing import List



class SimState():
    def __init__(self, 
                 start_schedule, 
                 end_schedule, 
                 num_chargers=5,
                 num_connectors=2,
                 num_buses=6,
                 min_power=0,
                 max_power=1000,
                 timestep_duration=1,
                 max_rate=0.24,
                 min_rate=0.08,
                 battery_capacity=588,
                 desired_soc=90
                 ) -> None:
        self.num_buses = num_buses
        self.battery_capacity = battery_capacity
        self.desired_soc = desired_soc
        self.is_done = False
        self.start_schedule: datetime       = start_schedule
        self.end_schedule:   datetime       = end_schedule
        self.current_time:   datetime       = self.start_schedule
        self.price_schedule: PriceSchedule  = self.__initialize_price_schedule(timestep_duration, max_rate, min_rate)
        self.chargers:       List[Charger]  = self.__initialize_chargers(num_chargers, 
                                                                         min_power, 
                                                                         max_power,
                                                                         num_connectors)
        self.buses:          List[Bus]      = self.__initialize_buses(num_buses, battery_capacity, desired_soc)


    def __initialize_chargers(self, num_chargers: int, min_power: float, max_power: float, num_connectors: int)\
            -> List[Charger]:
        """
        Initialize a set of chargers which make up a bus deport
        """
        charger_list = []
        for charger in range(0, num_chargers):
            charger_list.append( Charger(charger, min_power, max_power, num_connectors, self.price_schedule.timestep_duration))

        # return a list of chargers with the passed in specifications
        return charger_list


    def __initialize_buses(self, num_buses, battery_capacity, desired_soc) -> list[Bus]:
        bus_list = []
        for _ in range(0, num_buses):
            bus_list.append(Bus(
                self.start_schedule, 
                self.end_schedule - timedelta(hours=1), 
                battery_capacity, 
                desired_soc
                )
            )
        return bus_list

    def __initialize_price_schedule(self, timestep_duration, max_rate, min_rate) -> PriceSchedule:
        return PriceSchedule(
                timestep_duration,  
                min_rate, 
                max_rate,
                self.start_schedule, 
                self.end_schedule
                )
    
    def print_metrics(self):
        print("SIMULATION STATS")
        sim_stats = f"""
        start datetime: {self.start_schedule}
        end datetime: {self.end_schedule}
        current datetime: {self.current_time}
        """
        print(sim_stats)
        print("BUS INFORMATION")
        for bus in self.buses:
            bus.print_metrics()
        print("PRICING INFORMATION")
        self.price_schedule.print_metrics()
        print("CHARGER INFORMATION")
        for charger in self.chargers:
            charger.print_metrics()

    def reset_simulation(self):
        """
        Reset the simulation state to its initial conditions.
        """
        self.current_time = self.start_schedule
        self.total_price = 0
        self.is_done = False
        self.buses:          List[Bus]      = self.__initialize_buses(self.num_buses, self.battery_capacity, self.desired_soc)

    def apply_action(self, action):
        """
        Apply the action to the simulation state by updating charger outputs
        and advancing the simulation by one timestep.

        Args:
            action (list or np.array): Charging rates for each bus as a fraction of max charger power.
        """
        if len(action) != len(self.buses):
            raise ValueError("Action length must match the number of buses.")

        # Step 1: Apply the charging action
        for i, bus in enumerate(self.buses):
            # Find the charger and connector associated with the bus
            for charger in self.chargers:
                for connector in charger.connectors:
                    if connector.connected_to == bus:
                        # Calculate the charging power based on action
                        charge_rate = action[i] * charger.max_power
                        charge_rate = max(0, min(charge_rate, charger.max_power))  # Clamp to valid range
                        connector.update_charge_rate(charge_rate)

        # Step 2: Advance the simulation state
        timestep_duration = self.price_schedule.timestep_duration  # Time step in hours
        for charger in self.chargers:
            for connector in charger.connectors:
                connector.deliver_power(timestep_duration)  # Update bus SOCs based on charging rates

        # Update the simulation time
        self.current_time += timedelta(hours=timestep_duration)
        if self.current_time == self.end_schedule:
            self.is_done = True
       


    def get_current_meterics(self):
       grid_pull = np.sum([charger.current_draw for charger in self.chargers])
       cost = grid_pull * self.price_schedule.get_current_price(self.current_time)
       return grid_pull, cost

    


if __name__ == "__main__":
    starttime = datetime.now()
    endtime = starttime + timedelta(hours=8)
    simstate = SimState(starttime, endtime)
    simstate.print_metrics()
