from bus import Bus
from decisionMaker import DecisionMaker
from charger import Charger
from datetime import datetime
from priceSchedule import PriceSchedule
from simulation.naiveDM import NaiveDM

class SimState():
    def __init__(self, start_schedule, end_schedule) -> None:
        self.chargers:       list[Charger]  = self.__initialize_chargers()
        self.busses:         list[Bus]      = self.__initialize_buses()
        self.start_schedule: datetime       = start_schedule
        self.end_schedule:   datetime       = end_schedule
        self.current_time:   datetime       = self.start_schedule
        self.price_schedule: PriceSchedule  = self.__initialize_price_schedule(timestep_duration, max_rate, min_rate)
        
        

    
    def __initialize_chargers(self, num_chargers: int, min_power: float, max_power: float, num_connectors: int) -> list[Charger]:
        """
        Initialize a set of chargers which make up a bus deport

        return a list of chargers with the passed in specifications
        """
        pass

    def generatePriceList(self):
        pass

    def __initialize_buses(self):
        pass

    def __initialize_price_schedule(self, timestep_duration, max_rate, min_rate):
        pass
