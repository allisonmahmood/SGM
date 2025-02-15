import numpy as np

class SwitchedArrayRDF:
    def __init__(self, n_antennas=8, radius=1.0):
        """
        Initialize Switched Array RDF system

        Parameters:
        -----------
        n_antennas : int
            Number of antennas in the circular array
        radius : float
            Radius of the antenna array in meters
        """
        self.n_antennas = n_antennas
        self.radius = radius

        # Calculate antenna positions
        self.antenna_angles = np.linspace(0, 2*np.pi, n_antennas, endpoint=False)
        self.positions = np.array([
            [radius * np.cos(angle), radius * np.sin(angle)]
            for angle in self.antenna_angles
        ])

    def simulate_received_power(self, signal_angle, signal_strength=1.0, noise_level=0.1):
        """
        Simulate received power at each antenna

        Parameters:
        -----------
        signal_angle : float
            Angle of arrival in radians
        signal_strength : float
            Incident signal strength
        noise_level : float
            Standard deviation of Gaussian noise

        Returns:
        --------
        numpy.ndarray
            Array of received powers at each antenna
        """
        # Add distance-based attenuation and noise
        distances = np.sqrt(
            (self.positions[:, 0] - self.radius * np.cos(signal_angle))**2 +
            (self.positions[:, 1] - self.radius * np.sin(signal_angle))**2
        ) + 1e-6  # Modify the distance calculation to avoid zero values by adding a small epsilon (1e-6) to the denominator:

        # Calculate received power with inverse square law
        powers = signal_strength / (distances**2)

        # Add noise
        noise = np.random.normal(0, noise_level, self.n_antennas)
        return powers + noise

    def estimate_direction(self, powers):
        """
        Estimate direction from received powers

        Parameters:
        -----------
        powers : numpy.ndarray
            Array of received powers at each antenna

        Returns:
        --------
        float
            Estimated angle of arrival in radians
        float
            Confidence metric (0-1)
        """

        print("Estimating direction for", powers)
        # Find antenna with maximum power
        max_idx = np.argmax(powers)

        # Interpolate between adjacent antennas for better accuracy
        next_idx = (max_idx + 1) % self.n_antennas
        prev_idx = (max_idx - 1) % self.n_antennas

        # Calculate interpolated angle
        delta_angle = 2*np.pi / self.n_antennas
        if powers[next_idx] > powers[prev_idx]:
            ratio = powers[next_idx] / powers[max_idx]
            offset = ratio * delta_angle / 2
            angle = self.antenna_angles[max_idx] + offset
        else:
            ratio = powers[prev_idx] / powers[max_idx]
            offset = ratio * delta_angle / 2
            angle = self.antenna_angles[max_idx] - offset

        # Calculate confidence based on power distribution
        total_power = np.sum(powers)
        confidence = powers[max_idx] / (total_power + 1e-6) # Epsilon to avoid NaN

        return angle, confidence

    def process_measurement(self, signal_angle, snr_db=20):
        """
        Process a complete measurement cycle

        Parameters:
        -----------
        signal_angle : float
            True angle of arrival in radians
        snr_db : float
            Signal-to-noise ratio in dB

        Returns:
        --------
        float
            Estimated angle
        float
            Error in degrees
        float
            Confidence
        """
        # Convert SNR to linear scale
        snr = 10**(snr_db/10)
        noise_level = 1/snr

        # Simulate received powers
        powers = self.simulate_received_power(signal_angle, noise_level=noise_level)

        # Estimate direction
        est_angle, confidence = self.estimate_direction(powers)

        # Calculate error
        error_deg = np.abs(np.degrees(np.angle(
            np.exp(1j * (est_angle - signal_angle))
        )))

        return est_angle, error_deg, confidence

# Example usage
def demo_rdf():
    # Create RDF system with 8 antennas
    rdf = SwitchedArrayRDF(n_antennas=8)

    # Test with signal from 45 degrees
    true_angle = np.radians(45)
    est_angle, error, confidence = rdf.process_measurement(true_angle, snr_db=20)

    print(f"True angle: {np.degrees(true_angle):.1f}°")
    print(f"Estimated angle: {np.degrees(est_angle):.1f}°")
    print(f"Error: {error:.1f}°")
    print(f"Confidence: {confidence:.2f}")

demo_rdf()
