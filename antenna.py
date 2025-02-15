import numpy as np
import matplotlib.pyplot as plt

def gaussian_pickup_pattern(cos_theta, std_dev=0.5):
    print("Running gaussian_pickup_pattern")
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
    print("Running directional_antenna")
    """
    Computes the signal strength received by a directional antenna with a Gaussian pickup pattern.
    
    Parameters:
    field_amplitude (float): The amplitude of the field at the emitter position.
    emitter_position (array-like): The (x, y, z) coordinates of the emitter.
    antenna_position (array-like): The (x, y, z) coordinates of the antenna.
    antenna_direction (array-like): The (x, y, z) direction vector the antenna is facing.
    std_dev (float): The standard deviation of the Gaussian pattern.
    
    Returns:
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
    
    return received_signal

def plot_antenna_pattern(antenna_direction, std_dev=0.5):
    print("Running plot_antenna_pattern")
    """
    Plots the 360-degree pickup pattern of the directional antenna.
    
    Parameters:
    antenna_direction (array-like): The (x, y, z) direction vector the antenna is facing.
    std_dev (float): The standard deviation of the Gaussian pattern.
    """
    # Normalize the antenna direction vector
    antenna_direction_normalized = antenna_direction / np.linalg.norm(antenna_direction)
    
    # Define angles for the 360-degree plot
    angles = np.linspace(0, 2 * np.pi, 360)
    
    # Calculate the pickup pattern for each angle
    pickup_pattern = []
    for angle in angles:
        # Rotate the antenna direction vector by the current angle
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        rotated_direction = np.dot(rotation_matrix, antenna_direction_normalized)
        
        # Calculate the pickup pattern for the rotated direction
        cos_theta = np.dot(rotated_direction, antenna_direction_normalized)
        pattern_value = gaussian_pickup_pattern(cos_theta, std_dev)
        pickup_pattern.append(pattern_value)
    
    # Plot the pickup pattern
    plt.figure()
    plt.polar(angles, pickup_pattern)
    plt.title('Directional Antenna Pickup Pattern')
    plt.show()

# plot_antenna_pattern([50, 13, 0], std_dev=0.5)