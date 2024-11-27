import numpy as np
from datetime import datetime, timedelta
import sys
class Bus():
    
    def __init__(self, scheduledArrival: datetime, scheduledDeparture: datetime, battery_capacity: float, desired_soc: int):
        self.arrival_time:        datetime      = self.__getTrueArrivalTime(scheduledArrival)
        self.departure_time:      datetime      = self.__getTrueDepartureTime(scheduledDeparture)
        self.battery_capacity:    float         = battery_capacity
        self.__current_capacity:  float         = self.__init_curr_capacity()
        self.desired_soc:         int           = desired_soc
        self.current_soc:         function      = lambda : int((self.__current_capacity / self.battery_capacity) * 100)

    
    def __init_curr_capacity(self, dist_center=150):
        random_val = np.random.normal(dist_center, 10 , 1)[0]
        return random_val


    def __getTrueArrivalTime(self, scheduledArrival):
        """
        Apply noise to the desired arrival time to obtain the true
        arrival time. IE; expected arrival of 7:30PM but with noise
        alters arrival time to 7:34PM
        """
        random_val = abs(int(np.random.normal(0, 10, 1)[0]))
        arrival_offset = timedelta(minutes=random_val)
        true_arrival = scheduledArrival + arrival_offset
        return true_arrival


    def __getTrueDepartureTime(self, scheduledDeparture):
        """
        Apply noise to the desired departure time to obtain the true
        departure time. IE; expected departure of 5:30AM but with noise
        alters departure time to 5:34AM
        """
        random_val = abs(int(np.random.normal(0, 10, 1)[0]))
        arrival_offset = timedelta(minutes=random_val)
        true_departure = scheduledDeparture + arrival_offset
        return true_departure


    def charge(self, amount: float) -> bool:
        """
        add a certain amount of power to the bus in Kw/h
        return True if battery can accept charge
        return False if amount added exceeds amount available
        """
        if (amount + self.__current_capacity) < self.battery_capacity:
            self.__current_capacity += amount
            return True
        else:
            # print("warning: battery is already full", file=sys.stderr)
            self.__current_capacity = self.battery_capacity
            return False


    def print_metrics(self) -> None:
        """
        Print the attributes of the bus
        """
        
        bus_stats = f"""
        arrival time: {self.arrival_time} 
        departure time: {self.departure_time}
        battery capacity: {self.battery_capacity}
        current capacity: {self.__current_capacity}
        desired SOC: {self.desired_soc}
        current SOC: {self.current_soc()}
        """
        print(bus_stats)

if __name__ == "__main__":
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(hours=8)
    testBus = Bus(start_time, end_time, 538, 95)
    testBus.print_metrics()
