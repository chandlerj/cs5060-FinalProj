import numpy as np

class simState():

    def __init__(self, ) -> None:
        self.hour = [i for i in range(0, 24, 1)]
        self.chargers = []
        self.busses = []
        self.busSchedules = []
        self.prices = []
        self.expDemand = []

    def generateDemandList(self):
        """
        Generates a list of expected power in GW.
        Adds in Brownian noise 
        @Input  - season: 0 for summer, 1 for winter
        @Output - List of floats representing expected grid demand
        """
        pass

    def generatePriceList(self):
        pass

    def generateBusSchedule(self):
        pass

