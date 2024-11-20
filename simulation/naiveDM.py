from decisionMaker import DecisionMaker
from simspace import SimState
import typing
class NaiveDM(DecisionMaker):
    def __init__(self, sim_state):
        super().__init__(sim_state)

        self.__charge_rates :typing.Mapping[str, float] = self.__calc_charge_rates() 

    def update_chargers(self) -> None:
        pass 


    def __calc_charge_rates(self) -> typing.Dict[str, float]: 
        for charger in self.state.chargers:
            for connector in charger.connectors:
                if connector.active():
                    bus = connector.connected_to
                    soc_delta = bus.current_soc
                    
        return {}
