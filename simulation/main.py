import matplotlib.pyplot as plt

from simspace import SimState
from datetime import datetime, timedelta

import sys
from decisionMaker import DecisionMaker

from naiveDM import NaiveDM
from rtsoDM import rtsoDM
from rlDM import rlDM

class Main:

    def __init__(self, d_maker: str, num_chargers: int, num_buses: int):
        self.sim_state: SimState      = self.__make_sim_state(num_chargers=num_chargers, num_buses=num_buses)
        self.d_maker:   DecisionMaker = self.__make_decision_maker(d_maker, self.sim_state)
        self.num_buses = num_buses
        self.time_points = []
        self.soc_data = [[] for _ in range(num_buses)]
        self.charge_rate_data = [[] for _ in range(num_buses)]

    def __make_sim_state(self, num_chargers, num_buses) -> SimState:
        start_time = datetime.fromisoformat('2024-12-06T19:00:00')
        end_time = datetime.fromisoformat('2024-12-07T06:00:00')
        return SimState(start_time, end_time, num_chargers=num_chargers, num_buses=num_buses)    

    def __make_decision_maker(self, d_maker: str, sim_state: SimState):
        if d_maker.lower() == "naive":
            return NaiveDM(sim_state)
        # TODO: Replace these with the actual simulation environments
        elif d_maker.lower() == "rule-based":
            return rtsoDM(sim_state)
        elif d_maker.lower() == "rl":
            return rlDM(sim_state)
        else:
            raise NotImplementedError(f"Decision maker ${d_maker} is not a valid decision maker")
            
    def run_sim(self):
        total_timesteps = self.sim_state.price_schedule.num_timesteps
        timestep_scale = self.sim_state.price_schedule.timestep_duration
        if type(self.d_maker) == rlDM:
            for timestep in range(total_timesteps//3600):

                # update plot data for state of charge
                self.time_points.append(timestep)
                for i, bus in enumerate(self.sim_state.buses):
                    self.soc_data[i].append(bus.current_soc())

                self.d_maker.update_chargers(timestep)
        else:
            for timestep in range(total_timesteps):

                # update plot data for state of charge
                self.time_points.append(timestep)
                for i, bus in enumerate(self.sim_state.buses):
                    self.soc_data[i].append(bus.current_soc())

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


        # Plotting
        plt.figure(figsize=(10, 6))

        for i, soc in enumerate(self.soc_data):
            plt.plot(self.time_points, soc, label=f'Bus {i+1}')  # Plot SOC for each bus

        # Add labels, legend, and grid
        plt.xlabel('Timestep')
        plt.ylabel('State of Charge (SOC)')
        plt.title('SOC vs Time for Each Bus')
        plt.legend()
        plt.grid(True)

        # Display the plot
        plt.show()
            
        
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
        main = Main("rule-based", 8, 16)
        print("DECISON MAKER METRICS")
    main.run_sim()
    main.d_maker.plot_bus_charge_rates()
    main.d_maker.plot_total_charge_rate()

    if type(main.d_maker) == rtsoDM or type(main.d_maker) == NaiveDM:
        print(f"COST TO CHARGE: ${main.d_maker.cost}")

