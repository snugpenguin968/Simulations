# Logistic growth of a fish population given a constant harvesting rate. 
# Uses the Forward Euler Method


import matplotlib.pyplot as plt
import numpy
import math

harvest_rates = [2e4, 5e4, 1e5, 2e5] # tons / year

# This is used to keep track of the data that we want to plot.
data = []

def logistic_growth():
    maximum_growth_rate = 0.5 # 1 / year
    carrying_capacity = 2e6 # tons

    end_time = 10. # years
    h = 0.1 # years
    num_steps = int(end_time / h)
    times = h * numpy.array(range(num_steps + 1))

    fish = numpy.zeros(num_steps + 1) # tons
    fish[0] = 2e5

    for harvest_rate in harvest_rates:
        extinct=False
        for step in range(num_steps):
            if extinct:
                next_step=0
            else:
                next_step=fish[step]+h*(maximum_growth_rate*(1-fish[step]/carrying_capacity)*fish[step]-harvest_rate)
                if next_step<=0:
                    extinct=True
                    next_step=0
            fish[step+1]=next_step

        data.append(([time for time in times], [f for f in fish], 
            str(harvest_rate)))

    return fish

fish = logistic_growth()

def plot_me():
    fish_plots = []
    for (times, fish, rate_label) in data:
        fish_plots.append(plt.plot(times, fish, label=rate_label))    
    plt.legend([str(rate) for rate in harvest_rates], loc='upper right')
    axes = plt.gca()
    axes.set_xlabel('Time in years')
    axes.set_ylabel('Amount of fish in tons')
    plt.show()

plot_me()