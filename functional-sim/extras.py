import numpy as np
import matplotlib.pyplot as plt


# Plot the RF field strength in 3D
def plot_rf_field_strength(field, environment, xlabel='X', ylabel='Y', zlabel='Z', title='3D RF Field Strength'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x, y, z = environment
    sc = ax.scatter(x, y, z, c=field, cmap='viridis')

    plt.colorbar(sc, label='Field Strength')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(title)

    plt.show()

# Get Field strength at a given position
def get_field_strength_at_position(field, space_dim, resolution, position):
    """
    Gets the field strength at a specific position in the 3D space.
    
    Parameters:
    field (ndarray): The RF field strength at each point in the 3D space.
    space_dim (int): The dimension of the 3D space.
    resolution (int): The resolution of the 3D space.
    position (array-like): The (x, y, z) coordinates of the position.
    
    Returns:
    field_strength (float): The field strength at the specified position.
    """
    x, y, z = position
    x_index = int(x / space_dim * (resolution - 1))
    y_index = int(y / space_dim * (resolution - 1))
    z_index = int(z / space_dim * (resolution - 1))
    
    return field[x_index, y_index, z_index]


def calculate_target_angle(pow1, pow2, psi_0=0.5061454830783556, phi=np.pi/4):
    A_const = (-1 * np.log(0.5))
    angTarget = ((psi_0**2/(2*A_const*phi)) * (np.log(pow2)-np.log(pow1)))
    return angTarget



def angle_to_vector(angle, length=1):
    """
    Converts an angle in radians to a 2D vector of a given length.
    
    Parameters:
    angle (float): Angle in radians.
    length (float): Length of the resulting vector. Default is 1.
    
    Returns:
    np.array: 2D vector corresponding to the given angle.
    """
    x = length * np.cos(angle)
    y = length * np.sin(angle)
    return np.array([x, y])


def create_target_data(position, angle, direction):
    target_vector = angle_to_vector(angle)
    target_data = {
        "origin": position,
        "angle": angle,
        "direction": target_vector
    }
    return target_data