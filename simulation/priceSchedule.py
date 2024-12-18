from datetime import datetime, timedelta, time


class PriceSchedule:
    """
    from chatGPT:
    * Energy charges for large commercial customers are approximately 2.6 to 5.8 cents per kWh, with lower rates for off-peak usage
    * Demand charges (for peak power usage) range from $12 to $15 per kW depending on the time of year and service type
    """
    def __init__(self, timestep_duration, off_peak_rate, on_peak_rate, start_schedule, stop_schedule):
        self.on_peak_rate:      float       = on_peak_rate
        self.off_peak_rate:     float       = off_peak_rate
        self.start_schedule:    datetime    = start_schedule
        self.stop_schedule:     datetime    = stop_schedule
        self.timestep_duration: int         = timestep_duration
        self.num_timesteps:     int         = self.__get_num_timnesteps()
        self.price_schedule:    list[float] = self.__get_price_schedule()


    def __get_num_timnesteps(self):
        return int((self.stop_schedule - self.start_schedule).seconds / self.timestep_duration)
    
    def __get_price_schedule(self):
        """
        iterate through each hour of simulation and append price at that
        hour to price schedule list
        """
        price_schedule = []
        right_now = self.start_schedule
        num_hours = (self.stop_schedule - self.start_schedule).seconds // 3600
        
        for _ in range(num_hours):
            price_schedule.append(self.get_current_price(right_now))
            right_now = right_now + timedelta(hours=1)

        return price_schedule


    def get_current_price(self, curr_datetime: datetime):
        """
        use the prices list to extract the price based on the current time
        return the price float value. Checks if current time is within
        peak pricing window and returns price accordingly.

        On-peak window: 6AM-9AM, 6PM-10PM M-F
        Off-peak window: all other times
        """

        is_weekday = curr_datetime.weekday() < 5

        if not is_weekday:
            return self.off_peak_rate

        curr_timestamp = curr_datetime.time()
        morning_peak = time(6,0), time(9,0)
        evening_peak = time(18, 0), time(22, 0)

        if morning_peak[0] <= curr_timestamp <= morning_peak[1] or\
                evening_peak[0] <= curr_timestamp <= evening_peak[1]:
                    return self.on_peak_rate
        else:
            return self.off_peak_rate


    def print_metrics(self):
        metrics = f"""
        schedule start: {self.start_schedule}
        schedule stop: {self.stop_schedule}
        on peak rate: {self.on_peak_rate}
        off peak rate: {self.off_peak_rate}
        timestep Duration: {self.timestep_duration}
        number of timesteps over start/stop time: {self.num_timesteps}
        price schedule: {self.price_schedule}
        """
        print(metrics)

if __name__ == "__main__":
    # def __init__(self, timestep_duration, off_peak_rate, on_peak_rate, start_schedule, stop_schedule)
    starttime = datetime.now()
    endtime = starttime + timedelta(hours=9)

    test_schedule = PriceSchedule(1, 0.08, 0.24, starttime, endtime)
    test_schedule.print_metrics()
