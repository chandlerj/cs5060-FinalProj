from decisionMaker import DecisionMaker
from simspace import SimState
from datetime import timedelta
import typing
class NaiveDM(DecisionMaker):
    def __init__(self, sim_state):
        super().__init__(sim_state)

        self.__calc_charge_rates()

    def update_chargers(self, timesteps) -> None:
        
        for charger in self.state.chargers:
            for connector in charger.connectors:
                connector.deliver_power(timesteps)

    def __calc_charge_rates(self) -> None: 
        right_now = self.state.current_time
        hours_remaining = timedelta(self.state.end_schedule - right_now).seconds // 3600
        for charger in self.state.chargers:
            for connector in charger.connectors:
                if connector.connected_to != None:
                    bus = connector.connected_to
                    soc_delta = bus.battery_capacity - bus.current_soc()
                    charge_needed = abs(soc_delta - bus.desired_soc) 
                    # calculate lowest charge rate which will charge the bus by the desired end time
                    charge_rate = ((charge_needed * bus.battery_capacity) / hours_remaining) * 1000

                    connector.update_charge_rate(charge_rate)
