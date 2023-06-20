# P-type controller with a factor of 100,000 and 
# clamping the result to the range 0 to 200.
import matplotlib.pyplot as plt
import numpy
import math

h = 0.005 # s
mass_quarter_car = 250. # kg
mass_effective_wheel = 20. # kg
g = 9.81 # m / s2

end_time = 5. # s
num_steps = int(end_time / h)

w = numpy.zeros(num_steps + 1) # 1 / s
v = numpy.zeros(num_steps + 1) # m / s
x = numpy.zeros(num_steps + 1) # m
times = h * numpy.array(range(num_steps + 1))

### Uncomment the line below before running, but comment it out before submitting!
### @show_plot(8, 10)
def plot_me():
    axes_x = plt.subplot(411)
    axes_v = plt.subplot(412)
    axes_w = plt.subplot(413)
    axes_s = plt.subplot(414)

    def friction_coeff(slip):
        return 1.1 * (1. - math.exp(-20. * slip)) - 0.4 * slip

    def p_control(actual_value, target_value):
        return min(200.,max(0.,100000.*(target_value-actual_value)))

    def wheel_slip():
        x[0] = 0.
        v[0] = 120. * 1000. / 3600. # 120 km / h
        w[0] = v[0]

        for step in range(num_steps):
            if v[step] < 0.01:
                break
            s = max(0., 1. - w[step] / v[step])
            force = friction_coeff(s) * mass_quarter_car * g
            v[step + 1] = v[step] - h * force / mass_quarter_car
            x[step + 1] = x[step] + h * v[step]
            
            w[step + 1] = w[step] + h * (force / mass_effective_wheel - p_control(s,0.2))

            w[step + 1] = max(0., w[step + 1])

            axes_x.plot(times[:step], x[:step])
            axes_v.plot(times[:step], v[:step])
            axes_w.plot(times[:step], w[:step])
            axes_s.plot(times[:step], 1. - w[:step] / v[:step])

            axes_x.set_ylabel('Position\nin m', multialignment = 'center')
        axes_v.set_ylabel('Car velocity\nin m/s', multialignment = 'center')
        axes_w.set_ylabel('Wheel velocity\nin m/s', multialignment = 'center')
        axes_s.set_ylabel('Wheel\nslip', multialignment = 'center')
        axes_s.set_xlabel('Time in s')
        axes_s.set_ylim(0., 1.)
    
        return x, v, w

    return wheel_slip()

plot_me()
plt.show()