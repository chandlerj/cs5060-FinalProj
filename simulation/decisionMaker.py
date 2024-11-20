from simspace import SimState

class DecisionMaker:

    def __init__(self, sim_state: SimState):
        self.state: SimState = sim_state

    def update_chargers(self) -> None:
        """
        use the decision maker to update all active connectors
        for all chargers. 
        """
        pass
