# There are two species of fish. We want to harvest the species 1, but we have a bycatch of species 2.
# Models logistic growth for both species with the constants and the initial values given below.
# A fixed fraction p = 0...1 of this harvest will consist of species 2. 
# It represents the threshold value for fish species 2 to not go extinct. 
# Implemented using the Forward Euler Method.

import matplotlib.pyplot as plt
import numpy
import math

def bycatch():
    maximum_growth_rate_1 = 0.5 # 1 / year
    carrying_capacity_1 = 2.0e6 # tons
    maximum_growth_rate_2 = 0.3 # 1 / year
    carrying_capacity_2 = 1.0e6 # tons    
    harvest_rate = 0.8 * 2.5e5 # rate of catching both kinds of fish, tons / year
    
    p = 0.375 # fraction of bycatch, i.e. fish 2

    end_time = 100. # years
    h = 0.1 # years
    num_steps = int(end_time / h)
    times = h * numpy.array(range(num_steps + 1))

    fish_1 = numpy.zeros(num_steps + 1) # tons
    fish_1[0] = 1.3e6
    fish_2 = numpy.zeros(num_steps + 1) # tons
    fish_2[0] = 7.5e5

    for step in range(num_steps):
        fish_1[step + 1] = fish_1[step]+h*(maximum_growth_rate_1*(1-fish_1[step]/carrying_capacity_1)*fish_1[step]-(1-p)*harvest_rate)
        fish_2[step + 1] = fish_2[step]+h*(maximum_growth_rate_2*(1-fish_2[step]/carrying_capacity_2)*fish_2[step]-p*harvest_rate)

        if fish_1[step + 1] < 0. or fish_2[step + 1] < 0.:
            break

    return step, times, fish_1, fish_2

step, times, fish_1, fish_2 = bycatch()

def plot_fish():
    fish_1_plot = plt.plot(times[:step + 1], fish_1[:step + 1], label='Fish 1')
    fish_2_plot = plt.plot(times[:step + 1], fish_2[:step + 1], label = 'Fish 2')
    plt.legend(('Fish 1', 'Fish 2'), loc='upper right')

    axes = plt.gca()
    axes.set_xlabel('Time in years')
    axes.set_ylabel('Amount of fish in tons')
    plt.xlim(xmin = 0.)
    plt.ylim(ymin = 0.)
    plt.show()
plot_fish()