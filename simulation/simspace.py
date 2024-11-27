from bus import Bus
from charger import Charger
from priceSchedule import PriceSchedule

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
        self.start_schedule: datetime       = start_schedule
        self.end_schedule:   datetime       = end_schedule
        self.current_time:   datetime       = self.start_schedule
        self.price_schedule: PriceSchedule  = self.__initialize_price_schedule(timestep_duration, max_rate, min_rate)
        self.chargers:       List[Charger]  = self.__initialize_chargers(num_chargers, 
                                                                         min_power, 
                                                                         max_power,
                                                                         num_connectors)
        self.buses:         List[Bus]      = self.__initialize_buses(num_buses, battery_capacity, desired_soc)


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


if __name__ == "__main__":
    starttime = datetime.now()
    endtime = starttime + timedelta(hours=8)
    simstate = SimState(starttime, endtime)
    simstate.print_metrics()
