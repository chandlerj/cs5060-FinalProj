

class Bus():
    
    def __init__(self, scheduledArrival, scheduledDeparture):
        self.arrivalTime = self.getTrueArrivalTime(scheduledArrival)
        self.departureTime = self.getTrueDepartureTime(scheduledDeparture)

    def getTrueArrivalTime(self, scheduledArrival):
        pass

    def getTrueDepartureTime(self, scheduledDeparture):
        pass
