from simspace import SimState
from datetime import datetime, timedelta

import sys
from decisionMaker import DecisionMaker

from naiveDM import NaiveDM
from rtsoDM import rtsoDM

class Main:

    def __init__(self, d_maker: str, num_chargers: int, num_buses: int):
        self.sim_state: SimState      = self.__make_sim_state()
        self.d_maker:   DecisionMaker = self.__make_decision_maker(d_maker, self.sim_state)

    def __make_sim_state(self) -> SimState:
        start_time = datetime.fromisoformat('2024-12-06T19:00:00')
        end_time = datetime.fromisoformat('2024-12-07T06:00:00')
        return SimState(start_time, end_time)    

    def __make_decision_maker(self, d_maker: str, sim_state: SimState):
        if d_maker.lower() == "naive":
            return NaiveDM(sim_state)
        # TODO: Replace these with the actual simulation environments
        elif d_maker.lower() == "rule-based":
            return rtsoDM(sim_state)
        elif d_maker.lower() == "rl":
            return DecisionMaker(sim_state)
        else:
            raise NotImplementedError(f"Decision maker ${d_maker} is not a valid decision maker")
            
    def run_sim(self):
        total_timesteps = self.sim_state.price_schedule.num_timesteps
        timestep_scale = self.sim_state.price_schedule.timestep_duration
        for timestep in range(total_timesteps):
            
            # update current time in simulation
            self.sim_state.current_time = self.sim_state.current_time + timedelta(seconds=timestep_scale)
            # update rate of charge
            self.d_maker.update_chargers(1)

            #print(f"Current time: {self.sim_state.current_time}")
            # check for buses arriving/departing
            for bus in self.sim_state.buses:
                if bus.arrival_time == self.sim_state.current_time:
                            self.__find_open_connector(bus)
                if bus.departure_time == self.sim_state.current_time:
                    for charger in self.sim_state.chargers:
                        res = charger.disconnect_bus(bus)
                        if res:
                            print(f"{self.sim_state.current_time}: Bus disconnected\n{bus.print_metrics()}")
                            break
    
    def __check_bus_connected(self, bus):
        for charger in self.sim_state.chargers:
            for connector in charger.connectors:
                if connector.connected_to != None and connector.connected_to == bus:
                    return True
        return False

    def __find_open_connector(self, bus):
        for charger in self.sim_state.chargers:
            res = charger.connect_bus(bus)
            if res:
                print(f"{self.sim_state.current_time}: Bus arrived and was connected")
                break



if __name__ == "__main__":
    if len(sys.argv) == 4:
#                   decision maker  number of chargers  number of busses 
        main = Main(sys.argv[1],    int(sys.argv[2]),   int(sys.argv[3]))
    else:
        main = Main("rule-based", 5, 4)
        print("DECISON MAKER METRICS")
        main.d_maker.print_metrics()
        main.sim_state.print_metrics()
    main.run_sim()
