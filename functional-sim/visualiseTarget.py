import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import rf_simulation as rfSim

from testing import create_antenna_pair

import antenna as ant

import extras as ex

from targetVector import track
import random


import localize_RANSAC as ransac_loc


# Fixed Location
emitter_position = np.array([360, 290, 250])

# Dynamic Location
antenna_pairs = {
    "pos": [250, 250, 250],
    "dir": [1, 0, 0],
    "dis": 0.1
}

# Target vectors
measured_vectors = [{"origin" : [0,0,0], "direction" : [0,0,0]}]


#----------------------#

# Environment set
space_dim = 500
resolution = 100

# Emitter set
emitter_power = 20.0

# Antenna pattern
antena_std_dev = 0.3
psi_0 = 0.5061454830783556
phi = np.pi/4



#----------------------#
#----------------------#

# Step 1: Get target vectors

def generate_antenna_pairs(num_pairs=4, pos_limits=(0, 500), dir_limits=(-1, 1), dis=0.1):
    antenna_pairs = []
    for _ in range(num_pairs):
        pos = [random.uniform(*pos_limits) for _ in range(2)] + [250]
        dir = [random.uniform(*dir_limits) for _ in range(2)] + [0]
        antenna_pairs.append({
            "pos": pos,
            "dir": dir,
            "dis": dis
        })
    return antenna_pairs

def get_target_data(space_dim, resolution, emitter_position, emitter_power, antenna_pairs, phi, antena_std_dev):
    target_data_list = []
    for antenna_pair in antenna_pairs:
        target_data = track(space_dim, resolution, emitter_position, emitter_power, antenna_pair, phi, antena_std_dev)
        target_data_list.append(target_data)
    return target_data_list



# Step 5: Intercept target vectors to estimate source location



# Step 6: Plot results
def plot_target_vectors(target_data_list, emitter_position):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot emitter
    ax.scatter(emitter_position[0], emitter_position[1], emitter_position[2], color='r', s=100, label='Emitter')
    
    # Plot target vectors
    for target_data in target_data_list:
        origin = target_data["origin"]
        direction = np.append(target_data["direction"], 0)
        line_length = 1000  # Adjust as needed
        line_end = origin + direction * line_length
        ax.plot([origin[0], line_end[0]], [origin[1], line_end[1]], [origin[2], line_end[2]], color='b')
        
        # Add arrow to indicate direction
        ax.quiver(line_end[0], line_end[1], line_end[2], -direction[0], -direction[1], -direction[2], length=line_length, color='b', arrow_length_ratio=0.1, pivot='tail')
        
        # Add green line segment
        arrowhead_length = 0.1 * line_length
        arrowhead_end = origin + direction * (line_length + arrowhead_length)
        ax.plot([line_end[0], arrowhead_end[0]], [line_end[1], arrowhead_end[1]], [line_end[2], arrowhead_end[2]], color='g')
    
    ax.set_xlabel('X axis (m)')
    ax.set_ylabel('Y axis (m)')
    ax.set_zlabel('Z axis (m)')
    ax.legend()
    
    # Set the view to top-down perspective
    ax.view_init(elev=90, azim=-90)
    
    plt.show()


def generate_and_get_target_data(num_pairs, space_dim, resolution, emitter_position, emitter_power, phi, antena_std_dev):
    # Generate antenna pairs
    antenna_pairs = generate_antenna_pairs(num_pairs=num_pairs)
    
    # Get target data
    target_data_list = get_target_data(space_dim, resolution, emitter_position, emitter_power, antenna_pairs, phi, antena_std_dev)
    
    return target_data_list

def target_to_origin_direction(target_data_list):
    origins = np.array([target["origin"][:2] for target in target_data_list])
    directions = np.array([target["direction"][:2] for target in target_data_list])
    return origins, directions

# Example usage
target_data_list = generate_and_get_target_data(10, space_dim, resolution, emitter_position, emitter_power, phi, antena_std_dev)

# Plot the target vectors and emitter
#plot_target_vectors(target_data_list, emitter_position)