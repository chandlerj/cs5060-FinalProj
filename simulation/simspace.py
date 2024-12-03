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
                 num_buses=10,
                 min_power=0,
                 max_power=100,
                 timestep_duration=1,
                 max_rate=0.24,
                 min_rate=0.08,
                 battery_capacity=588,
                 desired_soc=90
                 ) -> None:
        self.min_power = min_power
        self.max_power = max_power
        self.num_chargers = num_chargers
        self.num_connectors = num_connectors
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
        for i in range(0, num_buses):
            bus_list.append(Bus(
                i,
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

    # this stuff aids in training the RL model -------------------------------------------------------------------------------
    
    def reset_simulation(self):
        """
        Reset the simulation state to its initial conditions.
        """
        self.current_time = self.start_schedule
        self.is_done = False
        self.chargers:       List[Charger]  = self.__initialize_chargers(self.num_chargers, 
                                                                         self.min_power, 
                                                                         self.max_power,
                                                                         self.num_connectors)
        self.buses:          List[Bus]      = self.__initialize_buses(self.num_buses, self.battery_capacity, self.desired_soc)
        print("resetting...")


    def apply_action(self, action, verbose=False):
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
                        charge_rate = action[i] * self.max_power
                        charge_rate = max(0, min(charge_rate, self.max_power))  # Clamp to valid range
                        charger.update_charge_rate(connector.connector_id, charge_rate)

        for i in range(3600):
            # Step 2: Advance the simulation state
            timestep_duration = self.price_schedule.timestep_duration
            for charger in self.chargers:
                for connector in charger.connectors:
                    connector.deliver_power(timestep_duration)  # Update bus SOCs based on charging rates

            # Update the simulation time
            self.current_time += timedelta(seconds=timestep_duration)
            if self.current_time == self.end_schedule:
                self.is_done = True

            # check for buses arriving/departing
            for bus in self.buses:
                if bus.arrival_time == self.current_time:
                    for charger in self.chargers:
                        res = charger.connect_bus(bus)
                        if res:
                            if verbose:
                                print(f"{self.current_time}: Bus arrived and was connected")
                                bus.print_metrics()
                            break
                if bus.departure_time == self.current_time:
                    for charger in self.chargers:
                        res = charger.disconnect_bus(bus)
                        if res:
                            if verbose:
                                print(f"{self.current_time}: Bus disconnected")
                                bus.print_metrics()
                            break

    def get_current_meterics(self):
       grid_pull = np.sum([charger.current_draw for charger in self.chargers])
       price = self.price_schedule.get_current_price(self.current_time)
       return grid_pull, price

    


if __name__ == "__main__":
    starttime = datetime.now()
    endtime = starttime + timedelta(hours=8)
    simstate = SimState(starttime, endtime)
    simstate.print_metrics()
