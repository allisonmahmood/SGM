from rf_simulation import setup_3d_space, compute_rf_field_strength, add_antenna, compute_antenna_signal_strength, visualize_all
from antenna import directional_antenna
import numpy as np
import os
import matplotlib.pyplot as plt

def initialize_simulation(space_dim, resolution, emitters, antenna_positions, antenna_directions, frequency_value):
    """
    Initializes the simulation by setting up the 3D space, computing RF field strength, and computing antenna signal strength.
    
    Parameters:
    space_dim (int): The dimension of the 3D space.
    resolution (int): The resolution of the 3D space.
    emitters (list): List of emitters with their positions and powers.
    antenna_positions (list): List of (x, y, z) coordinates of the antennas.
    antenna_directions (list): List of (x, y, z) direction vectors for the antennas.
    frequency_value (float): The frequency in GHz.
    
    Returns:
    X, Y, Z (ndarray): The coordinates of the points in the 3D space.
    field_strength (ndarray): The RF field strength at each point in the 3D space.
    antenna_strengths (list): List of signal strengths for the antennas.
    """
    # Setup 3D space
    X, Y, Z = setup_3d_space(space_dim, resolution)

    # Compute RF field strength
    field_strength = compute_rf_field_strength(emitters, X, Y, Z)

    # Compute antenna signal strength
    antenna_strengths = []
    for antenna_position, antenna_direction in zip(antenna_positions, antenna_directions):
        original_strength, signal_strength_db = directional_antenna(100, emitters[0]["position"], antenna_position, antenna_direction)
        antenna_strengths.append(signal_strength_db)
        print(f"Antenna at {antenna_position} original field strength: {original_strength:.2f} dB, picked-up strength: {signal_strength_db:.2f} dB")

    return X, Y, Z, field_strength, antenna_strengths                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

def plot_emitter_and_antennas(emitter_position, antenna_positions, antenna_directions, antenna_strengths, space_dim):
    """
    Plots the emitter and antennas in 3D space.
    
    Parameters:
    emitter_position (array-like): The (x, y, z) coordinates of the emitter.
    antenna_positions (list): List of (x, y, z) coordinates of the antennas.
    antenna_directions (list): List of (x, y, z) direction vectors for the antennas.
    antenna_strengths (list): List of signal strengths for the antennas.
    space_dim (int): The dimension of the 3D space.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(emitter_position[0], emitter_position[1], emitter_position[2], color='r', s=100, label='Emitter')
    min_strength = min(antenna_strengths)
    max_strength = max(antenna_strengths)
    for i, (antenna_position, antenna_direction, strength) in enumerate(zip(antenna_positions, antenna_directions, antenna_strengths)):
        if min_strength == max_strength:
            color = plt.cm.viridis(0.5)  # Use a neutral color if all strengths are the same
        else:
            color = plt.cm.viridis((strength - min_strength) / (max_strength - min_strength))
        ax.scatter(antenna_position[0], antenna_position[1], antenna_position[2], color=color, s=50, label=f'Antenna {i+1}')
        ax.quiver(antenna_position[0], antenna_position[1], antenna_position[2], 
                  antenna_direction[0], antenna_direction[1], antenna_direction[2], 
                  length=50, color=color)
    ax.set_xlabel('X axis (m)')
    ax.set_ylabel('Y axis (m)')
    ax.set_zlabel('Z axis (m)')
    ax.set_xlim([0, space_dim])
    ax.set_ylim([0, space_dim])
    ax.set_zlim([0, space_dim])
    ax.legend()
    plt.show()

def main():
    # Define sample values
    space_dim = 500
    resolution = 50
    emitters = [{"position": np.array([200, 450, 250]), "power": 100}]
    antenna_positions = [np.array([240, 10, 250]), np.array([260, 10, 250]), np.array([180, 10, 200])]
    antenna_directions = [np.array([-1, 1, 0]), np.array([1, 1, 0]), np.array([1, 1, 1])]  # Example directions
    frequency_value = 2.4  # GHz

    # Initialize simulation
    X, Y, Z, field_strength, antenna_strengths = initialize_simulation(space_dim, resolution, emitters, antenna_positions, antenna_directions, frequency_value)

    # Visualize all
    visualize_all(space_dim, emitters, antenna_positions, field_strength, X, Y, Z)

    # Plot emitter and antennas in 3D
    plot_emitter_and_antennas(emitters[0]["position"], antenna_positions, antenna_directions, antenna_strengths, space_dim)

main()