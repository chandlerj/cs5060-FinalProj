from time import datetime

class Bus():
    
    def __init__(self, scheduledArrival: datetime, scheduledDeparture: datetime, battery_capacity: float):
        self.arrivalTime:        datetime      = self.__getTrueArrivalTime(scheduledArrival)
        self.departureTime:      datetime      = self.__getTrueDepartureTime(scheduledDeparture)
        self.battery_capacity:   float         = battery_capacity
        self.__current_capacity: float         = self.init_curr_capacity()
        self.current_soc:        float         = lambda _: int((self.__current_capacity / self.battery_capacity) * 100)


    def __getTrueArrivalTime(self, scheduledArrival):
        """
        Apply noise to the desired arrival time to obtain the true
        arrival time. IE; expected arrival of 7:30PM but with noise
        alters arrival time to 7:34PM
        """
        pass

    def __getTrueDepartureTime(self, scheduledDeparture):
        """
        Apply noise to the desired departure time to obtain the true
        departure time. IE; expected departure of 5:30AM but with noise
        alters departure time to 5:34AM
        """
        pass

    def charge(amount: float) -> bool:
        """
        add a certain amount of power to the bus in Kw/h
        return True if battery can accept charge
        return False if amount added exceeds amount available
        """