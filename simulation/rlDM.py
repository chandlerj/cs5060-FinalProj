from decisionMaker import DecisionMaker
from datetime import timedelta
import gym
from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import numpy as np
import matplotlib.pyplot as plt

class rlDM(DecisionMaker):

    def __init__(self, sim_state):
        super().__init__(sim_state)
        self.num_buses          = len(self.state.buses)
        self.num_time_slots     = self.__get_num_time_slots()
        self.energy_demands     = self.__get_energy_demands()
        self.grid_limit         = 300 # TODO: arbitrary value, test best input
        self.time_slot_duration = 1   # TODO: another arbitrary value, currently assumes time slots are hours
        self.electricity_prices = self.state.price_schedule.price_schedule
        self.arrival_times, self.departure_times    = self.__get_bus_times()
        self.charge_rate        = self.__get_charge_rates()
        self.cost               = 0.0

        # train the model upon initialization of the DM
        # Create environment
        self.env = make_vec_env(lambda: BusDepotEnv(self.state), n_envs=1)

        # Initialize and train PPO
        self.model = PPO("MlpPolicy", self.env, verbose=1)
        print("training RL model...")
        self.state.print_metrics()
        self.model.learn(total_timesteps=10000)
        print("model is ready for prediction")
        self.state.reset_simulation()

    def plot_bus_charge_rates(self):
        for i, row in enumerate(self.charge_rate):
            plt.plot(row, label=f"bus {i}")
        plt.xlabel("hour of charge session")
        plt.ylabel("power to deliver (kW)")
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def plot_total_charge_rate(self):
        totals = [0 for _ in self.charge_rate[0]]
        for charge_rate in self.charge_rate:
            for i, element in enumerate(charge_rate):
                totals[i] += element
        plt.plot(totals)
        plt.xlabel("hour of charge session")
        plt.ylabel("total power delivered (kWh)")
        plt.grid(True)
        plt.show()

    def update_chargers(self, timestep) -> None:
        """
        update connector with charge rate and then
        deliver power to bus over timesteps
        """
        # Get the current observation
        observation = self.env.envs[0].unwrapped.get_observation()  # Assuming single env
        action, _ = self.model.predict(observation, deterministic=True)
        
        self.state.apply_action(action, verbose=True)
        for i, act in enumerate(action):
            charge_rate = act * self.state.max_power
            self.charge_rate[i][timestep] = charge_rate
            self.cost += charge_rate * self.electricity_prices[timestep]

    def print_metrics(self):
        metrics = f"""
        number of buses: {self.num_buses}
        number of time slots: {self.num_time_slots}
        energy demand (per bus): {self.energy_demands}
        total grid pull limit: {self.grid_limit}
        time slot duration (hours): {self.time_slot_duration}
        electricity prices: {self.electricity_prices}
        bus arrival times: {self.arrival_times}
        bus departure times: {self.departure_times}
        charge rates for each bus:\n {self.charge_rate}
        """
        print(metrics)

    def __get_bus_times(self):

        arrival_times = []
        departure_times = []

        for bus in self.state.buses:
            arrival_times.append(bus.arrival_time)
            departure_times.append(bus.departure_time)

        return arrival_times, departure_times

    def __get_num_time_slots(self):
        """
        From the simstate stand and end schedule times, get the 
        number of hours in the simstate
        """
        return (self.state.end_schedule - self.state.start_schedule).seconds // 3600


    def __get_energy_demands(self):
        """
        calculate the energy demands for each bus based on their
        desired state of charge
        """
        energy_demands = []

        for bus in self.state.buses:
            energy_demands.append(bus.battery_capacity * (bus.desired_soc - bus.current_soc()))

        return energy_demands

    

    def __get_charge_rates(self):
        # Dummy rates before training
        return np.zeros((self.num_buses, self.num_time_slots))


# custom gym env for training RL model (Chat GPT helped on this one)
class BusDepotEnv(gym.Env):
    def __init__(self, sim_state):
        super().__init__()
        self.sim_state = sim_state
        self.num_buses = len(sim_state.buses)
        
        # Define action and observation spaces
        self.action_space = spaces.Box(
            low=0, high=1, shape=(self.num_buses,), dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(self.num_buses * 2 + 2,), dtype=np.float32
        )

    def reset(self):
        # Reset the simulation to its initial state
        self.sim_state.reset_simulation()
        return self.get_observation()

    def step(self, action):
        # Apply the action to the simulation
        self.sim_state.apply_action(action) 
        
        # Get the next state, reward, and done flag
        observation = self.get_observation()
        reward = self.calculate_reward()
        done = self.sim_state.is_done 
        info = {}  # Additional data if needed
        return observation, reward, done, info

    def render(self, mode='human'):
        # Optional: Visualize the simulation state
        pass

    def get_observation(self):
        # Example: Combine SOC and grid consumption as the observation
        socs = [bus.current_soc() for bus in self.sim_state.buses]
        departures = [int((bus.departure_time - self.sim_state.current_time).total_seconds() // 60) for bus in self.sim_state.buses]
        grid_pull, energy_price = self.sim_state.get_current_meterics()
        return np.array(socs + departures + [grid_pull, energy_price], dtype=np.float32)

    def calculate_reward(self):
        unmet_soc_penalty = sum(
            max(0, bus.desired_soc - bus.current_soc()) for bus in self.sim_state.buses
        ) / len(self.sim_state.buses)
        ideal_grid_pull = 0
        for bus in self.sim_state.buses:
            time_to_departure = max(0, int((bus.departure_time - self.sim_state.current_time).total_seconds() // 3600)) 
            capacity = bus.battery_capacity
            current_charge = bus.get_current_capacity()
            if time_to_departure != 0:
                ideal_grid_pull += (capacity - current_charge) // time_to_departure

        grid_pull, energy_price = self.sim_state.get_current_meterics()
        rate_penalty = np.abs(ideal_grid_pull - grid_pull) / len(self.sim_state.buses)
        energy_cost = grid_pull * energy_price
        return - unmet_soc_penalty - (energy_cost / 10) - rate_penalty # reward for being close to the naive approach
    
    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]


