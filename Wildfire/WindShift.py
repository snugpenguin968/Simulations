# Implements the lateral shift of the fire 
# by the given velocity

import matplotlib.pyplot as plt
import numpy
import math

ambient_temperature = 300. # K
flame_temperature = 1000. # K
velocity = 0.003 # m / s
dx = 0.001 # m
size = 200 # grid units
positions = dx * numpy.arange(size) # m
h = 0.01 # s
end_time = 10.0 # s
num_steps = int(end_time / h)

# This is used to keep track of the data that we want to plot.
data = []

def heat_conduction():
    temperatures_old = ambient_temperature * numpy.ones(size) # K
    for i in range(size):
        temperatures_old[i] += (flame_temperature - ambient_temperature) * 0.5 \
                               * (1. + math.sin(1. * 2. * math.pi * i / size))
    temperatures_new = numpy.copy(temperatures_old) # K

    for step in range(num_steps):
        if step % 100 == 0:
            data.append(([pos for pos in positions], 
                          [temp for temp in temperatures_old]))
        for i in range(1, size - 1):
            temperatures_new[i]=temperatures_old[i]-h*velocity*(0.5*(temperatures_old[i+1]-temperatures_old[i-1]))/dx
        temperatures_old, temperatures_new = temperatures_new, temperatures_old

    return temperatures_old

temperatures = heat_conduction()

def plot_me():
    for (pos, temp) in data:
        plt.plot(pos, temp)
    axes = plt.gca()                
    axes.set_xlabel('Position in m')
    axes.set_ylabel('Temperature in K')
    plt.show()

plot_me()