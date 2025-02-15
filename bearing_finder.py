import numpy as np

def calculate_A():
    """Calculate the constant A = -ln(0.5) for half-power beamwidth"""
    return -np.log(0.5)

def power_output(phi, psi_0, G0, squint_angle=0):
    """
    Calculate the power output for an antenna with Gaussian characteristic

    Parameters:
    -----------
    phi : float or numpy.ndarray
        Bearing angle in radians
    psi_0 : float
        Half of the half-power beamwidth in radians
    G0 : float
        Antenna boresight gain
    squint_angle : float, optional
        Antenna squint angle (Φ) in radians. Default is 0.

    Returns:
    --------
    float or numpy.ndarray
        Power output
    """
    A = calculate_A()
    return G0 * np.exp(-A * ((phi - squint_angle) / psi_0)**2)

def power_ratio(phi, Phi, psi_0):
    """
    Calculate the ratio P1/P2

    Parameters:
    -----------
    phi : float or numpy.ndarray
        Bearing angle in radians
    Phi : float
        Squint angle in radians
    psi_0 : float
        Half of the half-power beamwidth in radians

    Returns:
    --------
    float or numpy.ndarray
        Power ratio P1/P2
    """
    A = calculate_A()
    return np.exp(A/(psi_0**2) * (Phi**2 - 2*Phi*phi))

def bearing_from_power_db(P1_db, P2_db, Phi, psi_0):
    """
    Calculate bearing angle from power measurements in dB

    Parameters:
    -----------
    P1_db : float or numpy.ndarray
        Power measurement from first antenna in dB
    P2_db : float or numpy.ndarray
        Power measurement from second antenna in dB
    Phi : float
        Squint angle in radians
    psi_0 : float
        Half of the half-power beamwidth in radians

    Returns:
    --------
    float or numpy.ndarray
        Bearing angle in radians
    """
    return (psi_0 / (2 * 6.0202) * Phi * (P2_db - P1_db)) + Phi/2

def bearing_from_power_natural(P1, P2, Phi, psi_0):
    """
    Calculate bearing angle from power measurements in natural units

    Parameters:
    -----------
    P1 : float or numpy.ndarray
        Power measurement from first antenna
    P2 : float or numpy.ndarray
        Power measurement from second antenna
    Phi : float
        Squint angle in radians
    psi_0 : float
        Half of the half-power beamwidth in radians

    Returns:
    --------
    float or numpy.ndarray
        Bearing angle in radians
    """
    A = calculate_A()
    return (psi_0**2 / (2*A)) * Phi * (np.log(P2) - np.log(P1)) + Phi/2

# Example usage
def example_usage():
    # Example parameters
    psi_0 = np.radians(30)  # 30 degrees half-power beamwidth
    Phi = np.radians(45)    # 45 degrees squint angle
    G0 = 1.0                # Unity gain for simplicity

    # Generate test angles
    phi_test = np.linspace(-np.pi/2, np.pi/2, 1000)

    # Calculate power outputs
    P1 = power_output(phi_test, psi_0, G0)
    P2 = power_output(phi_test, psi_0, G0, Phi)

    # Convert to dB
    P1_db = 10 * np.log10(P1)
    P2_db = 10 * np.log10(P2)

    # Calculate bearing angles using both methods
    bearing_db = bearing_from_power_db(P1_db, P2_db, Phi, psi_0)
    bearing_natural = bearing_from_power_natural(P1, P2, Phi, psi_0)

    return phi_test, P1, P2, bearing_db, bearing_natural


res = example_usage()
print(res)
