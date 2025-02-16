import numpy as np

import visualiseTarget as vt

def estimate_emitter_location(antennas, angles, weights=None):
    """
    antennas: list of (x, y) positions for N antennas
    angles: list of angles θ_i (radians) for each antenna
    weights: list of weights (default: uniform)
    """
    A = []
    b = []
    for (x_i, y_i), theta_i in zip(antennas, angles):
        sin_theta = np.sin(theta_i)
        cos_theta = np.cos(theta_i)
        A.append([sin_theta, -cos_theta])
        b.append(sin_theta * x_i - cos_theta * y_i)
    
    A = np.array(A)
    b = np.array(b)
    
    if weights is not None:
        W = np.diag(weights)
        A_weighted = W @ A
        b_weighted = W @ b
    else:
        A_weighted = A
        b_weighted = b
    
    # Solve (A^T A) u = A^T b
    u = np.linalg.lstsq(A_weighted, b_weighted, rcond=None)[0]
    return u




def target_lock(pairs = 10):
    target_data_list = vt.generate_and_get_target_data(num_pairs=pairs, space_dim=500, resolution=100, emitter_position=np.array([360, 120, 250]), emitter_power=20.0, phi=np.pi/4, antena_std_dev=0.3)

    locs_of_antenna = [target["origin"][0:2] for target in target_data_list]
    ang_of_antenna = [target["angle"] for target in target_data_list]

    emitter_location = estimate_emitter_location(locs_of_antenna, ang_of_antenna)

    print("with", pairs, "pairs of antennas, the estimated emitter location is", emitter_location)

    return emitter_location

