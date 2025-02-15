import numpy as np
import rf_simulation as rfSim

from testing import create_antenna_pair

import antenna as ant

import extras as ex


def setup_environment(space_dim, resolution, emitter_position, emitter_power):
    #print("Setting up environment")
    environment = rfSim.setup_3d_space(space_dim, resolution)
    emitters = [{"position": emitter_position, "power": emitter_power}]
    field = rfSim.compute_rf_field_strength(emitters, environment[0], environment[1], environment[2])
    return environment, field

def create_antennas(antenna_pairs, phi, antena_std_dev):
    #print("Creating antennas")
    antPos, antDir = create_antenna_pair(antenna_pairs["pos"], antenna_pairs["dis"], antenna_pairs["dir"], angle=phi)
    #ant.plot_antenna_patterns(antDir, antena_std_dev)
    return antPos, antDir

def calculate_signal_strength(field, space_dim, resolution, antPos, antDir, emitter_position, antena_std_dev):
    #print("Calculating signal strength")
    antSignal = []
    for i in range(len(antPos)):
        signal_strength = ex.get_field_strength_at_position(field, space_dim, resolution, antPos[i])
        directional_signal = ant.directional_antenna(signal_strength, emitter_position, antPos[i], antDir[i], std_dev=antena_std_dev)
        antSignal.append(directional_signal)
        #print(f"Antenna {i} signal strength:", directional_signal)
    return antSignal

def calculate_target_vector(antSignal, antenna_pairs, antDir):
    #print("Calculating target vector")
    pow1 = antSignal[0][1]
    pow2 = antSignal[1][1]
    target_angle_from_center = ex.calculate_target_angle(pow1, pow2)
    #print("Target angle from center:", target_angle_from_center)
    targetData = ex.create_target_data(antenna_pairs["pos"], target_angle_from_center, antDir[0])
    #print("Target data:", targetData)
    return targetData

def track(space_dim, resolution, emitter_position, emitter_power, antenna_pairs, phi, antena_std_dev):
    environment, field = setup_environment(space_dim, resolution, emitter_position, emitter_power)
    antPos, antDir = create_antennas(antenna_pairs, phi, antena_std_dev)
    antSignal = calculate_signal_strength(field, space_dim, resolution, antPos, antDir, emitter_position, antena_std_dev)
    targetData = calculate_target_vector(antSignal, antenna_pairs, antDir)
    return targetData


"""
# Example usage
space_dim = 500
resolution = 100
emitter_position = np.array([480, 250, 250])
emitter_power = 20.0
antenna_pairs = {
    "pos": [250, 250, 250],
    "dir": [1, 0, 0],
    "dis": 0.1
}
antena_std_dev = 0.3
phi = np.pi / 4

targetData = main(space_dim, resolution, emitter_position, emitter_power, antenna_pairs, phi, antena_std_dev)

"""