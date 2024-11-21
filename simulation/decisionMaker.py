from simspace import SimState

class DecisionMaker:

    def __init__(self, sim_state: SimState):
        self.state: SimState = sim_state

    def update_chargers(self, timesteps) -> None:
        """
        use the decision maker to update all active connectors
        for all chargers. 

        @input
        timesteps - number of timesteps to run simulation
        """
        pass
