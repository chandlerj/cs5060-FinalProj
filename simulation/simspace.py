from bus import Bus
from charger import Charger
from datetime import datetime
from priceSchedule import PriceSchedule

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
        self.chargers:       list[Charger]  = self.__initialize_chargers(NUM_CHARGERS, MIN_POWER, MAX_POWER,
                                                                         NUM_CONNECTORS)
        self.busses:         list[Bus]      = self.__initialize_buses()
        self.start_schedule: datetime       = start_schedule
        self.end_schedule:   datetime       = end_schedule
        self.current_time:   datetime       = self.start_schedule
        self.price_schedule: PriceSchedule  = self.__initialize_price_schedule(TIMESTEP_DURATION, MAX_RATE, MIN_RATE)

    def __initialize_chargers(self, num_chargers: int, min_power: float, max_power: float, num_connectors: int)\
            -> list[Charger]:
        """
        Initialize a set of chargers which make up a bus deport
        """
        charger_list = []
        for charger in range(0, num_chargers):
            charger_list[charger] = Charger(charger, min_power, max_power, num_connectors)
        """
        return a list of chargers with the passed in specifications
        """
        return charger_list

    def generatePriceList(self):
        pass

    def __initialize_buses(self) -> list[Bus]:
        bus_list = []
        for bus in range(0, 20):
            bus_list[bus] = Bus(self.start_schedule, self.end_schedule, BATTERY_CAPACITY, DESIRED_SOC)
        return bus_list

    def __initialize_price_schedule(self, timestep_duration, max_rate, min_rate) -> PriceSchedule:
        return PriceSchedule(timestep_duration, max_rate, min_rate)
