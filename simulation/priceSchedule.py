from datetime import datetime


class PriceSchedule:
    """
    from chatGPT:
    * Energy charges for large commercial customers are approximately 2.6 to 5.8 cents per kWh, with lower rates for off-peak usage
    * Demand charges (for peak power usage) range from $12 to $15 per kW depending on the time of year and service type
    """
    def __init__(self, timestep_duration, max_rate, min_rate):
        self.prices   = []
        self.max_rate = max_rate
        self.min_rate = min_rate
        self.start_schedule: datetime
        self.stop_schedule: datetime
        self.timestep_duration = timestep_duration
        self.num_timesteps = lambda _: int((self.stop_schedule - self.start_start_schedule).seconds() / timestep_duration)

    
    def get_current_price(self, curr_time):
        """
            use the prices list to extract the price based on the current time

            return the price float value
        """
        pass

    def generatePriceList(self):
        pass