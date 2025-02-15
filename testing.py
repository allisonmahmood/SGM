from rf_simulation import setup_3d_space, compute_rf_field_strength, add_antenna, compute_antenna_signal_strength, visualize_all
from antenna import directional_antenna, plot_antenna_pattern

# Define sample values
space_dim = 500
resolution = 50
emitters = [{"position": [250, 250, 250], "power": 100}]
antenna_positions = [[100, 100, 100], [400, 400, 400]]
frequency_value = 2.4  # GHz

# Setup 3D space
X, Y, Z = setup_3d_space(space_dim, resolution)

# Compute RF field strength
field_strength = compute_rf_field_strength(emitters, X, Y, Z)

# Compute antenna signal strength
for antenna_position in antenna_positions:
    signal_strength_db = compute_antenna_signal_strength(emitters, antenna_position, frequency_value)
    print(f"Antenna at {antenna_position} receives signal strength: {signal_strength_db:.2f} dB")

# Visualize all
visualize_all(space_dim, emitters, antenna_positions, field_strength, X, Y, Z)

# Plot antenna pattern
plot_antenna_pattern([1, 0, 0], std_dev=0.8)
