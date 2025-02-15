import numpy as np
import matplotlib.pyplot as plt

def gaussian_pickup_pattern(cos_theta, std_dev=0.5):
    # print("Running gaussian_pickup_pattern")
    """
    Calculates the Gaussian pickup pattern.
    
    Parameters:
    cos_theta (float): The cosine of the angle between the antenna direction and the vector to the emitter.
    std_dev (float): The standard deviation of the Gaussian pattern.
    
    Returns:
    pickup_pattern (float): The Gaussian pickup pattern value.
    """
    return np.exp(-(1 - cos_theta) / (2 * std_dev**2))

def directional_antenna(field_amplitude, emitter_position, antenna_position, antenna_direction, std_dev=0.5):
    # print("Running directional_antenna")
    """
    Computes the signal strength received by a directional antenna with a Gaussian pickup pattern.
    
    Parameters:
    field_amplitude (float): The amplitude of the field at the emitter position.
    emitter_position (array-like): The (x, y, z) coordinates of the emitter.
    antenna_position (array-like): The (x, y, z) coordinates of the antenna.
    antenna_direction (array-like): The (x, y, z) direction vector the antenna is facing.
    std_dev (float): The standard deviation of the Gaussian pattern.
    
    Returns:
    original_field_strength (float): The original field strength at the antenna position.
    received_signal (float): The signal strength received by the antenna.
    """
    # Calculate the vector from the antenna to the emitter
    vector_to_emitter = np.array(emitter_position) - np.array(antenna_position)
    
    # Normalize the direction vectors
    vector_to_emitter_normalized = vector_to_emitter / np.linalg.norm(vector_to_emitter)
    antenna_direction_normalized = antenna_direction / np.linalg.norm(antenna_direction)
    
    # Calculate the angle between the antenna direction and the vector to the emitter
    cos_theta = np.dot(vector_to_emitter_normalized, antenna_direction_normalized)
    
    # Calculate the Gaussian pickup pattern
    pickup_pattern = gaussian_pickup_pattern(cos_theta, std_dev)
    
    # Calculate the received signal strength
    received_signal = field_amplitude * pickup_pattern
    
    return field_amplitude, received_signal

def plot_antenna_patterns(antenna_directions, std_dev=0.5):
    # print("Running plot_antenna_patterns")
    """
    Plots the 360-degree pickup patterns of multiple directional antennas.
    
    Parameters:
    antenna_directions (list of array-like): A list of (x, y, z) direction vectors for the antennas.
    std_dev (float): The standard deviation of the Gaussian pattern.
    """
    # Define angles for the 360-degree plot
    angles = np.linspace(0, 2 * np.pi, 360)
    
    plt.figure()
    
    for i, antenna_direction in enumerate(antenna_directions):
        # Normalize the antenna direction vector
        antenna_direction_normalized = np.array(antenna_direction) / np.linalg.norm(antenna_direction)
        
        # Calculate the pickup pattern for each angle
        pickup_pattern = []
        for angle in angles:
            # Rotate the antenna direction vector by the current angle
            rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)]
            ])
            rotated_direction = np.dot(rotation_matrix, antenna_direction_normalized[:2])
            
            # Calculate the pickup pattern for the rotated direction
            cos_theta = np.dot(rotated_direction, [1, 0])
            pattern_value = gaussian_pickup_pattern(cos_theta, std_dev)
            pickup_pattern.append(pattern_value)
        
        # Plot the pickup pattern
        plt.polar(angles, pickup_pattern, label=f'Antenna {i+1}')
    
    plt.title('Directional Antenna Pickup Patterns')
    plt.legend()
    plt.show()

def plot_emitter_and_antenna(emitter_position, antenna_position):
    """
    Plots the emitter and antenna in 3D space.
    
    Parameters:
    emitter_position (array-like): The (x, y, z) coordinates of the emitter.
    antenna_position (array-like): The (x, y, z) coordinates of the antenna.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(emitter_position[0], emitter_position[1], emitter_position[2], color='r', s=100, label='Emitter')
    ax.scatter(antenna_position[0], antenna_position[1], antenna_position[2], color='b', s=100, label='Antenna')
    ax.set_xlabel('X axis (m)')
    ax.set_ylabel('Y axis (m)')
    ax.set_zlabel('Z axis (m)')
    ax.legend()
    plt.show()

#plot_antenna_patterns([[1, 0, 0], [0, 1, 0]], std_dev=0.5)

#plot_antenna_patterns([[1, 0, 0], [np.sqrt(2)/2, np.sqrt(2)/2, 0]], std_dev=0.5)