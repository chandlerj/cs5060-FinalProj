from bus import Bus
from typing import Optional

import numpy as np
import sys
from datetime import datetime, timedelta

class Connector:

    def __init__(self, connector_id, min_power, max_power, timestep_scale) -> None:
        self.connected_to:        Optional[Bus]  = None             # Bus which is connected to charger
        self.connector_id:        int            = connector_id     # identifyer for the connector
        self.min_power_out:       float          = min_power        # minimum power which charger can deliver (Kw/H)
        self.max_power_out:       float          = max_power        # maximum power which charger can deliver (Kw/H)
        self.curr_power_delivery: float          = max_power        # current desired charge rate (Kw/H)
        self.timestep_scale:      int            = timestep_scale   # number of seconds each timestep represents

    def active(self) -> bool:
        return self.connected_to != None


    def connect(self, bus: Bus) -> bool:
        """
        Connect bus to connector. return True if
        another bus is not already connected;
        otherwise, return False
        """
        if self.active():
            return False
        else:
            self.connected_to = bus
            return True

    def disconnect(self) -> bool:
        """
        Disconnect bus from connector. return True
        if bus disconnected, return False if no bus
        is correctly connected.
        """
        if self.active():
            self.connected_to = None
            return True
        else: 
            return False


    def update_charge_rate(self, rate: float) -> bool:
        """
        Change rate of charge on connector. return true
        if bus connected and charge rate updated.
        return False if no bus connected.

        If requested rate is out of bounds, raise a
        warning that desired rate is out of bounds, and
        print the rate actually set
        """
        if not self.active():
            print("Warning: Attempted to update the charge rate on an inactive connector", file=sys.stderr)
            return False
        if self.min_power_out <= rate <= self.max_power_out:
            self.curr_power_delivery = rate
        elif self.min_power_out > rate:
            print(f"Warning: proposed charge rate ({rate}) is below minimum ({self.min_power_out}). setting charge rate to {self.min_power_out}", file=sys.stderr)
            self.curr_power_delivery = self.min_power_out
        elif self.max_power_out < rate:
            print(f"Warning: proposed charge rate ({rate}) is above maximum ({self.max_power_out}). setting charge rate to {self.max_power_out}", file=sys.stderr)
            self.curr_power_delivery = self.max_power_out
        return True

    def deliver_power(self, timesteps: int) -> float:
        """
        simulate delivering power to the bus over n timesteps
        return the amount of power delivered to the bus.
        """
        power_delivered = 0.0
        if not self.active():
            # print("Warning: Attempted to deliver power to inactive charger", file=sys.stderr)
            return power_delivered
        # calculate power delivered per timestep
        power_per_timestep = (self.curr_power_delivery / 3600 ) * self.timestep_scale

        for _ in range(timesteps):
            # add randomness to power delivery to emulate real charger behavior
            random_val = np.random.normal(0, 0.01)
            power_for_timestep = (power_per_timestep) + random_val
            self.connected_to.charge(power_for_timestep)
            power_delivered += power_for_timestep
        return power_delivered
    def print_metrics(self) -> None:
        charger_stats = f"""
        Connector ID: {self.connector_id}
        Connected to: {self.connected_to}
        Minimum Power Delivery: {self.min_power_out}
        Maximum Power Delivery: {self.max_power_out}
        Current Power Delivery: {self.curr_power_delivery}
        Timestep scale (seconds): {self.timestep_scale}
        """
        print(charger_stats)
   
if __name__ == "__main__":
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(hours=8)
    test_bus= Bus(
                    0,
            start_time, 
                   end_time, 
                     538, 
                          95)
    
    test_connector = Connector(0, 20, 120, 1)
    test_connector.connect(test_bus)
    
    print("BUS METRICS")
    test_bus.print_metrics()

    test_connector.update_charge_rate(60)
    print("CONNECTOR METRICS")
    test_connector.print_metrics()
    
    print("Charging bus for 100 seconds")
    for i in range(100):
        power_delivered = test_connector.deliver_power(1)
        # print(f"timestep {i}: delivered {power_delivered} in {test_connector.timestep_scale} seconds")
    test_bus.print_metrics()

