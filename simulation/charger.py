
from bus import Bus
from connector import Connector

import sys
from datetime import datetime, timedelta

class Charger:

    def __init__(self, charger_id, min_power, max_power, num_connectors, timestep_scale):
        self.connectors:  list[Connector] = self.__initialize_connectors(min_power, max_power, num_connectors, timestep_scale)
        self.charger_id:  str             = charger_id
        self.meter_count: int             = 0
        self.current_draw:float           = 0.0
    

    def connect_bus(self, bus: Bus) -> bool:
        """
        Connect bus to available connector.
        If no connectors are available, return False
        else return True after connecting bus
        """
        for connector in self.connectors:
            if connector.active():
                continue
            else:
                connector.connected_to = bus
                return True

        # no connectors are available
        print("error: This charger has no available connectors", file=sys.stderr)
        return False
    
    def disconnect_bus(self, bus: Bus) -> bool:
        """
        Disconnect bus from connector
        return False if bus is not on any connectors
        return True if bus disconnected sucessfully
        """
        for connector in self.connectors:
            if connector.connected_to == bus:
                connector.connected_to = None
                return True
            else:
                continue

        # Bus not on any connectors
        print("error: Bus could not be found on any connectors", file=sys.stderr)
        return False

    def update_charge_rate(self, connector_id: int, rate: float) -> bool:
        """
        update rate of charge of a specific connector
        return true if connector_id valid and rate within bonuds of
        connector. Return false (and probably raise an exception)
        otherwise.
        """
        if len(self.connectors) - 1 < connector_id or connector_id < 0:
            print(f"Error: connector requested out of range. Valid IDs in range (0-{len(self.connectors) - 1}) ")
            return False 

        self.connectors[connector_id].update_charge_rate(rate)
        return True

    def __initialize_connectors(self, min_power: float, max_power: float, num_connectors: int, timestep_scale) -> list[Connector]:
        """
        Create connector objects for the charger. Set the power bounds and
        number of connectors on the charger
        """
        connectors = []

        for i in range(num_connectors):
            connectors.append(Connector(i, min_power, max_power, timestep_scale))

        return connectors
    

    def print_metrics(self):
        charger_metrics = f"""
        Charger ID: {self.charger_id}
        Charger Connectors: {self.connectors}
        Meter Count: {self.meter_count}
        Current Draw: {self.current_draw}
        """
        print(charger_metrics)

if __name__ == "__main__":
    test_charger = Charger("new charger", 20, 150, 2, 1)
    print("CHARGER METRICS")
    test_charger.print_metrics()

    start_time = datetime.now()
    end_time = datetime.now() + timedelta(hours=8)
    
    print("Connecting bus to charger")
    testBus = Bus(start_time, end_time, 538, 95)
    testBus.print_metrics()
    test_charger.connect_bus(testBus)
    
    print("Connector stats after connecting bus")
    for connector in test_charger.connectors:
       connector.print_metrics()


    print("Disconnecting Bus")
    test_charger.disconnect_bus(testBus)

    print("Connector stats after disconnecting bus")
    for connector in test_charger.connectors:
       connector.print_metrics()


