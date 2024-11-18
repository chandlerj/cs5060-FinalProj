from bus import Bus
from typing import Optional
class Connector:

    def __init__(self, connector_id, min_power, max_power, timestep_scale) -> None:
        self.connected_to:        Optional[Bus]  = None
        self.connector_id:        int            = connector_id
        self.min_power_out:       float          = min_power
        self.max_power_out:       float          = max_power
        self.curr_power_delivery: float          = max_power
        self.timestep_scale:      int            = timestep_scale


    def active(self) -> bool:
        return self.connected_to != None


    def connect(self, bus: Bus) -> bool:
        """
        Connect bus to connector. return True if
        another bus is not already connected;
        otherwise, return False
        """
        raise NotImplemented()


    def disconnect(self) -> bool:
        """
        Disconnect bus from connector. return True
        if bus disconnected, return False if no bus
        is correctly connected.
        """
        raise NotImplemented()


    def update_charge_rate(self, rate: float) -> bool:
        """
        Change rate of charge on connector. return true
        if bus connected and charge rate updated.
        return False if no bus connected.

        If requested rate is out of bounds, raise a
        warning that desired rate is out of bounds, and
        print the rate actually set
        """
        raise NotImplemented()


    def deliver_power(self, timesteps: int) -> float:
        """
        simulate delivering power to the bus over n timesteps
        return the amount of power delivered to the bus.
        """
        raise NotImplemented()
