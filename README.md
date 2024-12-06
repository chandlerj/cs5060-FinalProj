# Bus Charging Simulator

**Contributors**

* Chandler Justice
* Braden Cook
* Wil Stika

### Running the simulator

1. Install Dependencies
``` 
$ pip install gym stable-baselines3 pygad numpy matplotlib
```
2. Choose a Decision Maker
   * Naive
   * Rule-Based
   * RL
3. Run Using the Command
```
$ python simulation/main.py {decision maker} {number of chargers} {number of busses}
```

### Notes on Data Analysis


RESULTS.csv contains relevant data for all electric busses in UTA's fleet for the month of October

analysis.ipynb contains a few figures detailing power consumption from charging on an hour to hour basis

There unfortunately is no data available pertaining to which chargers were used for a charge session and it's hard to guess what charged profiles may have looked like. However, there is a column called 'Time charging' that could be used along with the 'Energy charged' colunm to calculate the rate of charge of a bus over the hour the data comes from.
