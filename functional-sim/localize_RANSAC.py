from sklearn.linear_model import RANSACRegressor
import numpy as np

import visualiseTarget as vt  

import localize_RANSAC as ransac_loc

def generate_antenna_data(pairs=10):
    target_data_list = vt.generate_and_get_target_data(num_pairs=pairs, space_dim=500, resolution=100, emitter_position=np.array([360, 120, 250]), emitter_power=20.0, phi=np.pi/4, antena_std_dev=0.3)

    origins = np.array([target["origin"][:2] for target in target_data_list])
    directions = np.array([target["direction"][:2] for target in target_data_list])

    return origins, directions

def convert_to_lines(origins, directions):
    """
    Convert direction vectors to lines (a*x + b*y + c = 0)
    """
    lines = []
    for origin, direction in zip(origins, directions):
#        direction = -direction  # Flip the direction vector
        a, b = -direction[1], direction[0]  # Perpendicular to direction vector
        c = -(a * origin[0] + b * origin[1])
        lines.append([a, b, c])
    return lines

def estimate_emitter_location(origins, directions):
    """
    Estimate the emitter location using RANSAC.
    """
    lines = convert_to_lines(origins, directions)

    # Solve with RANSAC
    X = np.array(lines)[:, :2]  # Coefficients (a, b)
    y = -np.array(lines)[:, 2]  # -c
    ransac = RANSACRegressor().fit(X, y)
    emitter_location = ransac.estimator_.coef_
    return emitter_location

# Generate antenna data
origins, directions = generate_antenna_data(pairs=1000)

# Estimate emitter location
emitter_location = estimate_emitter_location(origins, directions)
print("Estimated emitter location:", emitter_location)
