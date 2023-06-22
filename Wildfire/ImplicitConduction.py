# Models heat conduction in a wire made up of 100 segments with an implicit method

import matplotlib.pyplot as plt
import numpy
import math

ambient_temperature = 300. # K
flame_temperature = 1000. # K
thermal_diffusivity = 10. * 0.001 ** 2 # m2 / s
dx = 0.001 # m
size = 100 # grid units
positions = dx * numpy.arange(size) # m

h = 0.5 # s
end_time = 10.0 # s
num_steps = int(end_time / h)

def heat_conduction_implicit():
    temperatures_old = ambient_temperature * numpy.ones(size) # K
    for i in range(4 * size // 10, 5 * size // 10):
        temperatures_old[i] = flame_temperature
    temperatures_new = numpy.copy(temperatures_old) # K

    c = h * thermal_diffusivity / dx ** 2
    coefficients = numpy.zeros([size, size])

    for i in range(1,size-1):
        coefficients[i,i]=1+2*c
    for i in range(0,size-1):
        coefficients[i,i+1]=-c
        coefficients[i+1,i]=-c
    coefficients[0,0]=1+c
    coefficients[-1,-1]=1+c

    for step in range(num_steps):

        temperatures_new=numpy.linalg.solve(coefficients,temperatures_old)
        temperatures_old,temperatures_new=temperatures_new,temperatures_old

    return temperatures_old

temperatures = heat_conduction_implicit()

def heat_plot():
    plt.plot(positions, temperatures)
    axes = plt.gca()                
    axes.set_xlabel('Position in m')
    axes.set_ylabel('Temperature in K')
    plt.show()

heat_plot()