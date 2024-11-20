from simspace import SimState
from datetime import datetime

import sys
from decisionMaker import DecisionMaker

from naiveDM import NaiveDM

class Main:

    def __init__(self, d_maker: str, num_chargers: int, num_buses: int):
        self.sim_state: SimState      = self.__make_sim_state()
        self.d_maker:   DecisionMaker = self.__make_decision_maker(d_maker, self.sim_state)

    def __make_sim_state(self) -> SimState:
        start_time = datetime.fromisoformat('2024-12-06T19:00:00')
        end_time = datetime.fromisoformat('2024-12-07T05:00:00')
        return SimState(start_time, end_time)    

    def __make_decision_maker(self, d_maker: str, sim_state: SimState):
        if d_maker.lower() == "naive":
            return NaiveDM(sim_state)
        else:
            raise NotImplementedError("")
            
    def run_sim(self):



if __name__ == "__main__":
    main = Main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        
