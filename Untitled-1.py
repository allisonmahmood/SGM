# Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Ensure the directory exists
output_dir = '/Users/allisonmahmood/Documents/GitHub/SGM/tests2'
os.makedirs(output_dir, exist_ok=True)

# Options for locations and parameters
space_dim = 500  # 500m x 500m x 500m
emitter_position = np.array([250, 250, 500])  # Center of the space
antenna_position = np.array([100, 100, 100])  # Example position
frequency_value = 2.4  # Frequency in GHz
emitter_power = 100.0  # Power of the emitter
resolution = 300  # Resolution of the 3D space

def setup_3d_space(space_dim, resolution):
    print("Running setup_3d_space")
    # Define the 3D space using a grid
    x = np.linspace(0, space_dim, resolution)  # resolution points along x-axis
    y = np.linspace(0, space_dim, resolution)  # resolution points along y-axis
    z = np.linspace(0, space_dim, resolution)  # resolution points along z-axis
    X, Y, Z = np.meshgrid(x, y, z)
    return X, Y, Z

def compute_rf_field_strength(emitter_position, X, Y, Z, emitter_power):
    print("Running compute_rf_field_strength")
    """
    Computes the RF field strength at each point in the 3D space.
    
    Parameters:
    emitter_position (array-like): The (x, y, z) coordinates of the emitter.
    X, Y, Z (ndarray): The coordinates of the points in the 3D space.
    emitter_power (float): The power of the emitter.
    
    Returns:
    field_strength (ndarray): The RF field strength at each point in the 3D space.
    """
    distance = np.sqrt((X - emitter_position[0])**2 + (Y - emitter_position[1])**2 + (Z - emitter_position[2])**2)
    field_strength = emitter_power / (distance + 1e-6)  # Avoid division by zero
    return field_strength

def add_antenna(ax, position, label):
    print("Running add_antenna")
    """
    Adds an antenna at the specified position in the 3D space.
    
    Parameters:
    position (array-like): The (x, y, z) coordinates of the antenna.
    label (str): The label for the antenna.
    """
    ax.scatter(position[0], position[1], position[2], color='b', s=resolution)
    print("Antenna added")

def compute_antenna_signal_strength(emitter_position, antenna_position, frequency_value, emitter_power):
    print("Running compute_antenna_signal_strength")
    """
    Computes the signal strength received by the antenna.
    
    Parameters:
    emitter_position (array-like): The (x, y, z) coordinates of the emitter.
    antenna_position (array-like): The (x, y, z) coordinates of the antenna.
    frequency_value (float): The frequency in GHz.
    emitter_power (float): The power of the emitter.
    
    Returns:
    signal_strength_db (float): The signal strength received by the antenna in dB.
    """
    # Calculate the distance between the emitter and the antenna
    distance = np.sqrt(np.sum((emitter_position - antenna_position)**2))
    
    # Calculate the wavelength in meters
    wavelength = 3e8 / (frequency_value * 1e9)
    
    # Calculate the path loss using the Friis transmission equation
    path_loss = (4 * np.pi * distance / wavelength)**2
    
    # Calculate the received power in dB
    received_power_db = 10 * np.log10(emitter_power / path_loss)
    
    return received_power_db

def visualize_all(space_dim, emitter_position, antenna_position, field_strength, X, Y, Z):
    print("Running visualize_all")
    # Visualize everything together in a single plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X axis (m)')
    ax.set_ylabel('Y axis (m)')
    ax.set_zlabel('Z axis (m)')
    ax.set_xlim([0, space_dim])
    ax.set_ylim([0, space_dim])
    ax.set_zlim([0, space_dim])
    ax.scatter(emitter_position[0], emitter_position[1], emitter_position[2], color='r', s=100)
    add_antenna(ax, antenna_position, 'Antenna 1')
    sc = ax.scatter(X, Y, Z, c=np.log10(field_strength), cmap='viridis', marker='o', vmin=0, vmax=np.log10(emitter_power))
    print("Visualization setup complete")
    plt.colorbar(sc, ax=ax, label='Log Field Strength (dB)')
    print("Colorbar added")
    plt.savefig(os.path.join(output_dir, '3d_space_visualization.png'))
    print("Visualization saved")
    plt.close()

# Main execution
print("Starting main execution")
X, Y, Z = setup_3d_space(space_dim, resolution)
field_strength = compute_rf_field_strength(emitter_position, X, Y, Z, emitter_power)
visualize_all(space_dim, emitter_position, antenna_position, field_strength, X, Y, Z)

# Compute and print the signal strength received by the antenna
signal_strength_db = compute_antenna_signal_strength(emitter_position, antenna_position, frequency_value, emitter_power)
print(f"Signal strength received by the antenna: {signal_strength_db:.2f} dB")
print("Done!")