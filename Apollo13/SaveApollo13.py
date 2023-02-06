import math
import matplotlib.pyplot
import numpy

earth_mass = 5.97e24 # kg
earth_radius = 6.378e6 # m (at equator)
gravitational_constant = 6.67e-11 # m3 / kg s2
moon_mass = 7.35e22 # kg
moon_radius = 1.74e6 # m
moon_distance = 400.5e6 # m (not a constant irl)
moon_period = 27.3 * 24.0 * 3600. # s
moon_initial_angle = math.pi / 180. * -61. # radian

total_duration = 12. * 24. * 3600. # s
marker_time = 0.5 * 3600. # s
tolerance = 100000. # m



def moon_position(time):
    angle=moon_initial_angle+2*math.pi*time/moon_period
    return numpy.array([moon_distance*numpy.array(math.cos(angle)),moon_distance*numpy.array(math.sin(angle))])

def acceleration(time, position):
    moon_pos=moon_position(time)
    dist_from_moon=position-moon_pos
    dist_from_earth=position
    return -gravitational_constant*(earth_mass/numpy.linalg.norm(dist_from_earth)**3*dist_from_earth+moon_mass/numpy.linalg.norm(dist_from_moon)**3*dist_from_moon)

axes = matplotlib.pyplot.gca()
axes.set_xlabel('Longitudinal position in m')
axes.set_ylabel('Lateral position in m')


def apply_boost():
    
    boost = 10. 
    position_list = [numpy.array([-6.701e6, 0.])] # m
    velocity_list = [numpy.array([0., -10.818e3])] # m / s
    times_list = [0]
    position = position_list[0]
    velocity = velocity_list[0]
    current_time = 0.
    h = 0.1 # s, set as initial step size right now but will store current step size
    h_new = h # s, will store the adaptive step size of the next step
    mcc2_burn_done = False
    dps1_burn_done = False

    while current_time < total_duration:
        if not mcc2_burn_done and current_time>=101104:
            velocity-=7.04/numpy.linalg.norm(velocity)*velocity
            mcc2_burn_done=True
        if not dps1_burn_done and current_time>=212100:
            velocity+=boost/numpy.linalg.norm(velocity)*velocity
            dps1_burn_done=True

        a0=acceleration(current_time,position)
        vE=velocity+h*a0
        pE=position+h*velocity
        vH=velocity+h*0.5*(a0+acceleration(current_time+h,pE))
        pH=position+h*0.5*(velocity+vE)
        velocity=vH
        position=pH
        error=numpy.linalg.norm(pE-pH)+total_duration*numpy.linalg.norm(vE-vH)
        h_new=h*math.sqrt(tolerance/error)
        h_new = min(0.5 * marker_time, max(0.1, h_new)) 
            
        current_time += h
        h = h_new
        position_list.append(position.copy())
        velocity_list.append(velocity.copy())
        times_list.append(current_time)

    return position_list, velocity_list, times_list, boost

position, velocity, current_time, boost = apply_boost()

def plot_path(position_list, times_list):
    axes = matplotlib.pyplot.gca()
    axes.set_xlabel('Longitudinal position in m')
    axes.set_ylabel('Lateral position in m')
    previous_marker_number = -1;
    for position, current_time in zip(position_list, times_list):
         if current_time >= marker_time * previous_marker_number:
            previous_marker_number += 1
            matplotlib.pyplot.scatter(position[0], position[1], s = 2., facecolor = 'r', edgecolor = 'none')
            moon_pos = moon_position(current_time)
            if numpy.linalg.norm(position - moon_pos) < 30. * moon_radius: 
                axes.add_line(matplotlib.lines.Line2D([position[0], moon_pos[0]], [position[1], moon_pos[1]], alpha = 0.3, c = 'g')) 
    axes.add_patch(matplotlib.patches.CirclePolygon((0., 0.), earth_radius, facecolor = 'none', edgecolor = 'b'))
    for i in range(int(total_duration / marker_time)):
        moon_pos = moon_position(i * marker_time)
        axes.add_patch(matplotlib.patches.CirclePolygon(moon_pos, moon_radius, facecolor = 'none', edgecolor = 'g', alpha = 0.7))

    matplotlib.pyplot.axis('equal')

plot_path(position, current_time)
matplotlib.pyplot.show()