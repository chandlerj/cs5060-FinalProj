from bus import Bus
from charger import Charger
from priceSchedule import PriceSchedule

from datetime import datetime, timedelta
from typing import List

NUM_CHARGERS = 10
NUM_CONNECTORS = 2
MIN_POWER = 0
MAX_POWER = 1
TIMESTEP_DURATION = 1
MAX_RATE = 1
MIN_RATE = 0
BATTERY_CAPACITY = 100
DESIRED_SOC = 1


class SimState():
    def __init__(self, start_schedule, end_schedule) -> None:
        self.start_schedule: datetime       = start_schedule
        self.end_schedule:   datetime       = end_schedule
        self.current_time:   datetime       = self.start_schedule
        self.price_schedule: PriceSchedule  = self.__initialize_price_schedule(TIMESTEP_DURATION, MAX_RATE, MIN_RATE)
        self.chargers:       List[Charger]  = self.__initialize_chargers(NUM_CHARGERS, 
                                                                         MIN_POWER, 
                                                                         MAX_POWER,
                                                                         NUM_CONNECTORS)
        self.busses:         List[Bus]      = self.__initialize_buses()


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


    def __initialize_buses(self) -> List[Bus]:
        bus_list = []
        for _ in range(0, 20):
            bus_list.append(Bus(
                self.start_schedule, 
                self.end_schedule, 
                BATTERY_CAPACITY, 
                DESIRED_SOC
                )
            )
        return bus_list

    def __initialize_price_schedule(self, timestep_duration, max_rate, min_rate) -> PriceSchedule:
        return PriceSchedule(timestep_duration, max_rate, min_rate)
    
    def print_metrics(self):
        sim_stats = f"""
        start datetime: {self.start_schedule}
        end datetime: {self.end_schedule}
        current datetime: {self.current_time}
        """
        print(sim_stats)
        for charger in self.chargers:
            charger.print_metrics()


if __name__ == "__main__":
    starttime = datetime.now()
    endtime = starttime + timedelta(hours=8)
    simstate = SimState(starttime, endtime)
    simstate.print_metrics()
