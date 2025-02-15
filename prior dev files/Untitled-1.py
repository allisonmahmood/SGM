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
emitters = [
    {"position": np.array([250, 250, 500]), "power": 100.0},  # Emitter 1
    {"position": np.array([500, 500, 300]), "power": 50.0}    # Emitter 2
]
antenna_positions = [
    np.array([100, 100, 100]),  # Antenna 1
    np.array([200, 200, 200])   # Antenna 2
]
frequency_value = 2.4  # Frequency in GHz
resolution = 100  # Resolution of the 3D space

def setup_3d_space(space_dim, resolution):
    print("Running setup_3d_space")
    # Define the 3D space using a grid
    x = np.linspace(0, space_dim, resolution)  # resolution points along x-axis
    y = np.linspace(0, space_dim, resolution)  # resolution points along y-axis
    z = np.linspace(0, space_dim, resolution)  # resolution points along z-axis
    X, Y, Z = np.meshgrid(x, y, z)
    return X, Y, Z

def compute_rf_field_strength(emitters, X, Y, Z):
    print("Running compute_rf_field_strength")
    """
    Computes the RF field strength at each point in the 3D space.
    
    Parameters:
    emitters (list): List of emitters with their positions and powers.
    X, Y, Z (ndarray): The coordinates of the points in the 3D space.
    
    Returns:
    field_strength (ndarray): The RF field strength at each point in the 3D space.
    """
    field_strength = np.zeros_like(X)
    for emitter in emitters:
        distance = np.sqrt((X - emitter["position"][0])**2 + (Y - emitter["position"][1])**2 + (Z - emitter["position"][2])**2)
        field_strength += emitter["power"] / (distance + 1e-6)  # Avoid division by zero
    return field_strength

def add_antenna(ax, position, label):
    print("Running add_antenna")
    """
    Adds an antenna at the specified position in the 3D space.
    
    Parameters:
    position (array-like): The (x, y, z) coordinates of the antenna.
    label (str): The label for the antenna.
    """
    ax.scatter(position[0], position[1], position[2], color='b', s=100, label=label)
    print("Antenna added")

def compute_antenna_signal_strength(emitters, antenna_position, frequency_value):
    print("Running compute_antenna_signal_strength")
    """
    Computes the signal strength received by the antenna.
    
    Parameters:
    emitters (list): List of emitters with their positions and powers.
    antenna_position (array-like): The (x, y, z) coordinates of the antenna.
    frequency_value (float): The frequency in GHz.
    
    Returns:
    signal_strength_db (float): The signal strength received by the antenna in dB.
    """
    total_power = 0
    for emitter in emitters:
        # Calculate the distance between the emitter and the antenna
        distance = np.sqrt(np.sum((emitter["position"] - antenna_position)**2))
        
        # Calculate the wavelength in meters
        wavelength = 3e8 / (frequency_value * 1e9)
        
        # Calculate the path loss using the Friis transmission equation
        path_loss = (4 * np.pi * distance / wavelength)**2
        
        # Calculate the received power
        total_power += emitter["power"] / path_loss
    
    # Calculate the received power in dB
    signal_strength_db = 10 * np.log10(total_power)
    
    return signal_strength_db

def visualize_all(space_dim, emitters, antenna_positions, field_strength, X, Y, Z):
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
    for emitter in emitters:
        ax.scatter(emitter["position"][0], emitter["position"][1], emitter["position"][2], color='r', s=100)
    for i, antenna_position in enumerate(antenna_positions):
        add_antenna(ax, antenna_position, f'Antenna {i+1}')
    sc = ax.scatter(X, Y, Z, c=np.log10(field_strength), cmap='viridis', marker='o', vmin=0, vmax=np.log10(max(emitter["power"] for emitter in emitters)))
    print("Visualization setup complete")
    plt.colorbar(sc, ax=ax, label='Log Field Strength (dB)')
    print("Colorbar added")
    plt.savefig(os.path.join(output_dir, '3d_space_visualization.png'))
    print("Visualization saved")
    plt.close()

# Main execution
print("Starting main execution")
X, Y, Z = setup_3d_space(space_dim, resolution)
field_strength = compute_rf_field_strength(emitters, X, Y, Z)
visualize_all(space_dim, emitters, antenna_positions, field_strength, X, Y, Z)

# Compute and print the signal strength received by each antenna
for i, antenna_position in enumerate(antenna_positions):
    signal_strength_db = compute_antenna_signal_strength(emitters, antenna_position, frequency_value)
    print(f"Signal strength received by Antenna {i+1}: {signal_strength_db:.2f} dB")
print("Done!")