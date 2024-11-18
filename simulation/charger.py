
from bus import Bus
from connector import Connector

class Charger:

    def __init__(self, charger_id, min_power, max_power, num_connectors):
        self.connectors:  list[Connector] = self.__initialize_connectors(min_power, max_power, num_connectors)
        self.charger_id:  str             = charger_id
        self.meter_count: int             = 0
        self.power_used:  list[float]     = []
        self.current_draw:float           = 0.0
    

    def connect_bus(self, bus: Bus) -> bool:
        """
        Connect bus to available connector.
        If no connectors are available, return False
        else return True after connecting bus
        """
        raise NotImplemented() 

    
    def disconnect_bus(self, bus: Bus) -> bool:
        """
        Disconnect bus from connector
        return False if bus is not on any connectors
        return True if bus disconnected sucessfully
        """
        raise NotImplemented()


    def update_charge_rate(self, connector_id: int, rate: float) -> bool:
        """
        update rate of charge of a specific connector
        return true if connector_id valid and rate within bonuds of
        connector. Return false (and probably raise an exception)
        otherwise.
        """
        raise NotImplemented()
    

    def __initialize_connectors(self, min_power: float, max_power: float, num_connectors: int) -> list[Connector]:
        """
        Create connector objects for the charger. Set the power bounds and
        number of connectors on the charger
        """
        raise NotImplemented()
