from rf_simulation import setup_3d_space, compute_rf_field_strength, add_antenna, compute_antenna_signal_strength, visualize_all
from antenna import directional_antenna
import numpy as np
import os
import matplotlib.pyplot as plt

from bearing_finder import bearing_from_power_db, bearing_from_power_natural

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

def create_antenna_pair(base_position, distance, direction, angle=np.pi/4):
    """
    Creates a pair of antennas a set distance apart facing a specified direction with a specified angle between them.
    
    Parameters:
    base_position (array-like): The (x, y, z) coordinates of the base position.
    distance (float): The distance between the two antennas.
    direction (array-like): The (x, y, z) direction vector the antennas are facing.
    angle (float): The angle between the antennas in radians. Default is 45 degrees (pi/4).
    
    Returns:
    antenna_positions (list): List of (x, y, z) coordinates of the antennas.
    antenna_directions (list): List of (x, y, z) direction vectors for the antennas.
    """
    direction = np.array(direction) / np.linalg.norm(direction)
    perpendicular_direction = np.cross(direction, [0, 0, 1])
    if np.linalg.norm(perpendicular_direction) == 0:
        perpendicular_direction = np.cross(direction, [0, 1, 0])
    perpendicular_direction = perpendicular_direction / np.linalg.norm(perpendicular_direction)
    
    antenna_positions = [
        base_position + (distance / 2) * perpendicular_direction,
        base_position - (distance / 2) * perpendicular_direction
    ]
    
    rotation_matrix = np.array([
        [np.cos(angle/2), -np.sin(angle/2), 0],
        [np.sin(angle/2), np.cos(angle/2), 0],
        [0, 0, 1]
    ])
    
    antenna_directions = [
        np.dot(rotation_matrix, direction),
        np.dot(rotation_matrix.T, direction)
    ]
    
    return antenna_positions, antenna_directions

def plot_bearing_vs_angle(antenna1_strength, antenna2_strength, fixed_angle=np.pi/4):
    """
    Plots the bearing values as the angle changes between 0 and pi.
    
    Parameters:
    antenna1_strength (float): The signal strength of the first antenna.
    antenna2_strength (float): The signal strength of the second antenna.
    fixed_angle (float): The fixed angle between the antennas.
    """
    angles = np.linspace(0, 2*np.pi, 100)
    bearings = [bearing_from_power_db(antenna1_strength, antenna2_strength, fixed_angle, angle) for angle in angles]
    
    plt.figure()
    plt.plot(angles, bearings)
    plt.xlabel('Angle (radians)')
    plt.ylabel('Bearing')
    plt.title('Bearing vs Angle')
    plt.show()

def main(emitter_position=np.array([200, 450, 250]), antenna_positions=None, antenna_directions=None):
    # Define default values if not provided
    if antenna_positions is None or antenna_directions is None:
        base_position = np.array([250, 250, 250])
        distance = 20
        direction = [1, 0, 0]
        antenna_positions, antenna_directions = create_antenna_pair(base_position, distance, direction)

    # Define other sample values
    space_dim = 500
    resolution = 50
    emitters = [{"position": emitter_position, "power": 100}]
    frequency_value = 2.4  # GHz

    # Initialize simulation
    X, Y, Z, field_strength, antenna_strengths = initialize_simulation(space_dim, resolution, emitters, antenna_positions, antenna_directions, frequency_value)

    # Calc bearing back

    antenna1_strength = antenna_strengths[0]
    antenna2_strength = antenna_strengths[1]

    print("db based: ")
    print(bearing_from_power_db(antenna1_strength, antenna2_strength, np.pi/4, 0.9))
    print("natural based: ")
    print(bearing_from_power_natural(antenna1_strength, antenna2_strength, np.pi/4, 0.9))

    # Plot bearing vs angle
    plot_bearing_vs_angle(antenna1_strength, antenna2_strength)

    # Visualize all
    visualize_all(space_dim, emitters, antenna_positions, field_strength, X, Y, Z)

    # Plot emitter and antennas in 3D
    plot_emitter_and_antennas(emitter_position, antenna_positions, antenna_directions, antenna_strengths, space_dim)


#main(emitter_position=[100,250,80])

#main()

#psi0_actual = 0.9