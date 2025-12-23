#!/usr/bin/env python3
"""
Directional Acoustics Physics Model

Comprehensive model for analyzing the theoretical limits and feasibility
of directional sound transmission. Implements diffraction physics,
atmospheric absorption, and parametric array acoustics.

This is a physics simulation for understanding acoustic propagation -
useful for analyzing claims about directional audio technology.
"""

import json
import math
from dataclasses import dataclass
from typing import Tuple, Optional
import sys

# Try numpy, fall back to math module
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    # Create minimal numpy-like interface using math
    class NumpyFallback:
        pi = math.pi
        @staticmethod
        def sqrt(x): return math.sqrt(x)
        @staticmethod
        def exp(x): return math.exp(x)
        @staticmethod
        def log10(x): return math.log10(x)
        @staticmethod
        def degrees(x): return math.degrees(x)
        inf = float('inf')
    np = NumpyFallback()


# Physical constants
SPEED_OF_SOUND = 343.0  # m/s at 20°C sea level
AIR_DENSITY = 1.204  # kg/m³ at 20°C
ATMOSPHERIC_PRESSURE = 101325  # Pa
REFERENCE_INTENSITY = 1e-12  # W/m² (threshold of hearing)


@dataclass
class AcousticEnvironment:
    """Environmental parameters affecting sound propagation."""
    temperature_c: float = 20.0
    relative_humidity: float = 50.0
    pressure_pa: float = 101325.0

    @property
    def speed_of_sound(self) -> float:
        """Temperature-corrected speed of sound."""
        return 331.3 * np.sqrt(1 + self.temperature_c / 273.15)

    @property
    def air_density(self) -> float:
        """Temperature and pressure corrected air density."""
        return self.pressure_pa / (287.05 * (self.temperature_c + 273.15))


@dataclass
class AcousticSource:
    """Defines an acoustic source/transducer."""
    aperture_diameter: float  # meters
    frequency: float  # Hz
    power_watts: float  # acoustic power output
    source_type: str = "conventional"  # "conventional" or "parametric"

    @property
    def wavelength(self) -> float:
        return SPEED_OF_SOUND / self.frequency

    @property
    def ka(self) -> float:
        """Dimensionless wavenumber-aperture product (beam directivity factor)."""
        k = 2 * np.pi / self.wavelength
        return k * (self.aperture_diameter / 2)


class DirectionalAcoustics:
    """Model for analyzing directional sound propagation."""

    def __init__(self, environment: Optional[AcousticEnvironment] = None):
        self.env = environment or AcousticEnvironment()

    def diffraction_beamwidth(self, aperture: float, frequency: float) -> float:
        """
        Calculate the -3dB beamwidth due to diffraction limit.

        For a circular aperture:
        θ_3dB ≈ 1.02 * λ/D (radians, first null at 1.22 λ/D)

        Args:
            aperture: Diameter of the sound source (meters)
            frequency: Frequency of sound (Hz)

        Returns:
            Half-angle beamwidth in radians
        """
        wavelength = self.env.speed_of_sound / frequency
        # -3dB beamwidth for circular piston
        theta = 1.02 * wavelength / aperture
        return theta

    def beamwidth_degrees(self, aperture: float, frequency: float) -> float:
        """Beamwidth in degrees."""
        return np.degrees(self.diffraction_beamwidth(aperture, frequency))

    def geometric_spreading_loss(self, distance: float) -> float:
        """
        Intensity reduction due to spherical spreading.

        I(r) = I₀ / r² (inverse square law)

        Args:
            distance: Distance from source (meters)

        Returns:
            Loss factor (multiply by source intensity)
        """
        if distance < 0.1:
            distance = 0.1  # Avoid singularity
        return 1.0 / (distance ** 2)

    def atmospheric_absorption_coefficient(self, frequency: float) -> float:
        """
        Calculate atmospheric absorption coefficient (Np/m).

        Uses ISO 9613-1 model for atmospheric absorption.
        Simplified version - full model requires humidity corrections.

        Args:
            frequency: Frequency in Hz

        Returns:
            Absorption coefficient in Nepers per meter
        """
        # Simplified model coefficients
        T = self.env.temperature_c + 273.15
        T0 = 293.15
        p = self.env.pressure_pa / 101325  # Normalized pressure
        h = self.env.relative_humidity

        # Relaxation frequencies
        fr_O = (p / 101325) * (24 + 4.04e4 * h * (0.02 + h) / (0.391 + h))
        fr_N = (p / 101325) * (T / T0) ** (-0.5) * (
            9 + 280 * h * np.exp(-4.17 * ((T / T0) ** (-1/3) - 1))
        )

        f = frequency
        # Absorption in dB/m (then convert to Np/m)
        alpha_dB = 8.686 * f ** 2 * (
            1.84e-11 * (p / 101325) ** (-1) * (T / T0) ** 0.5 +
            (T / T0) ** (-2.5) * (
                0.01275 * np.exp(-2239.1 / T) / (fr_O + f ** 2 / fr_O) +
                0.1068 * np.exp(-3352.0 / T) / (fr_N + f ** 2 / fr_N)
            )
        )

        return alpha_dB / 8.686  # Convert to Np/m

    def atmospheric_absorption_loss(self, frequency: float, distance: float) -> float:
        """
        Calculate intensity loss due to atmospheric absorption.

        Args:
            frequency: Frequency in Hz
            distance: Propagation distance in meters

        Returns:
            Remaining intensity fraction (0 to 1)
        """
        alpha = self.atmospheric_absorption_coefficient(frequency)
        return np.exp(-2 * alpha * distance)  # Factor of 2 for intensity vs amplitude

    def total_intensity_at_distance(self, source: AcousticSource,
                                     distance: float) -> float:
        """
        Calculate acoustic intensity at a given distance.

        Args:
            source: AcousticSource object
            distance: Distance from source (meters)

        Returns:
            Intensity in W/m²
        """
        # Initial intensity at 1 meter (assume spherical spreading from there)
        I_1m = source.power_watts / (4 * np.pi)

        # Apply losses
        spreading = self.geometric_spreading_loss(distance)
        absorption = self.atmospheric_absorption_loss(source.frequency, distance)

        return I_1m * spreading * absorption

    def spl_at_distance(self, source: AcousticSource, distance: float) -> float:
        """
        Calculate Sound Pressure Level (dB SPL) at distance.

        Args:
            source: AcousticSource object
            distance: Distance from source (meters)

        Returns:
            SPL in dB re 20 µPa
        """
        intensity = self.total_intensity_at_distance(source, distance)
        if intensity <= 0:
            return -np.inf
        return 10 * np.log10(intensity / REFERENCE_INTENSITY)

    def effective_range(self, source: AcousticSource,
                        min_spl: float = 60.0) -> float:
        """
        Calculate effective range where SPL drops below threshold.

        Args:
            source: AcousticSource object
            min_spl: Minimum usable SPL in dB

        Returns:
            Maximum effective range in meters
        """
        # Binary search for distance where SPL = min_spl
        low, high = 1.0, 10000.0

        for _ in range(50):  # Sufficient iterations for convergence
            mid = (low + high) / 2
            spl = self.spl_at_distance(source, mid)

            if spl > min_spl:
                low = mid
            else:
                high = mid

        return mid

    def parametric_array_analysis(self, primary_freq: float,
                                   difference_freq: float,
                                   aperture: float,
                                   power: float) -> dict:
        """
        Analyze parametric (ultrasonic) array performance.

        Parametric arrays use nonlinear acoustic effects to generate
        highly directional audible sound from ultrasonic carriers.

        Args:
            primary_freq: Primary ultrasonic frequency (Hz)
            difference_freq: Desired audible frequency (Hz)
            aperture: Array diameter (meters)
            power: Electrical power (watts)

        Returns:
            Analysis results dictionary
        """
        # Parametric conversion efficiency is very low (typically 0.1-1%)
        conversion_efficiency = 0.005  # Conservative 0.5%
        acoustic_power = power * conversion_efficiency

        # Beamwidth is determined by the ultrasonic frequency
        primary_beamwidth = self.beamwidth_degrees(aperture, primary_freq)

        # The audible difference frequency inherits the ultrasonic directivity
        # (this is the key advantage of parametric arrays)

        source = AcousticSource(
            aperture_diameter=aperture,
            frequency=difference_freq,
            power_watts=acoustic_power,
            source_type="parametric"
        )

        # Effective range is limited by ultrasonic absorption
        ultrasonic_absorption = self.atmospheric_absorption_coefficient(primary_freq)

        return {
            "primary_frequency_hz": primary_freq,
            "difference_frequency_hz": difference_freq,
            "aperture_m": aperture,
            "input_power_w": power,
            "conversion_efficiency": conversion_efficiency,
            "acoustic_power_w": acoustic_power,
            "beamwidth_degrees": primary_beamwidth,
            "ultrasonic_absorption_db_per_m": ultrasonic_absorption * 8.686,
            "effective_range_m": self.effective_range(source, min_spl=50),
            "spl_at_10m": self.spl_at_distance(source, 10),
            "spl_at_50m": self.spl_at_distance(source, 50),
            "spl_at_100m": self.spl_at_distance(source, 100)
        }


class FeasibilityAnalyzer:
    """Analyze feasibility of specific directional audio scenarios."""

    def __init__(self):
        self.model = DirectionalAcoustics()

    def analyze_scenario(self, description: str,
                         frequency: float,
                         distance: float,
                         target_spl: float,
                         max_aperture: float = 2.0,
                         max_power: float = 1000.0) -> dict:
        """
        Analyze if a scenario is physically feasible.

        Args:
            description: Scenario description
            frequency: Target frequency (Hz)
            distance: Required range (meters)
            target_spl: Required SPL at target (dB)
            max_aperture: Maximum practical aperture (meters)
            max_power: Maximum practical power (watts)

        Returns:
            Feasibility analysis
        """
        result = {
            "scenario": description,
            "target_frequency_hz": frequency,
            "target_distance_m": distance,
            "target_spl_db": target_spl,
            "constraints": {
                "max_aperture_m": max_aperture,
                "max_power_w": max_power
            }
        }

        # Calculate required source intensity at 1m
        spreading = self.model.geometric_spreading_loss(distance)
        absorption = self.model.atmospheric_absorption_loss(frequency, distance)
        total_loss = spreading * absorption

        target_intensity = REFERENCE_INTENSITY * 10 ** (target_spl / 10)
        required_intensity_1m = target_intensity / total_loss
        required_power = required_intensity_1m * 4 * np.pi

        result["required_power_w"] = required_power
        result["power_feasible"] = required_power <= max_power

        # Calculate required aperture for reasonable directivity
        wavelength = SPEED_OF_SOUND / frequency
        # For 10° beamwidth: aperture ≈ 5.8 * wavelength
        required_aperture_10deg = 5.8 * wavelength

        result["wavelength_m"] = wavelength
        result["aperture_for_10deg_beam_m"] = required_aperture_10deg
        result["aperture_feasible"] = required_aperture_10deg <= max_aperture

        # Achievable beamwidth with max aperture
        achievable_beamwidth = self.model.beamwidth_degrees(max_aperture, frequency)
        result["achievable_beamwidth_degrees"] = achievable_beamwidth

        # Overall feasibility
        result["feasible"] = result["power_feasible"] and result["aperture_feasible"]

        # Add explanation
        if not result["feasible"]:
            issues = []
            if not result["power_feasible"]:
                issues.append(f"Requires {required_power:.1f}W, max is {max_power}W")
            if not result["aperture_feasible"]:
                issues.append(
                    f"Requires {required_aperture_10deg:.1f}m aperture for 10° beam, "
                    f"max is {max_aperture}m"
                )
            result["infeasibility_reasons"] = issues

        return result

    def generate_comprehensive_report(self) -> dict:
        """Generate comprehensive feasibility report for various scenarios."""
        scenarios = [
            ("Whisper at 10m (500Hz)", 500, 10, 30),
            ("Conversation at 50m (1kHz)", 1000, 50, 60),
            ("Loud speech at 100m (2kHz)", 2000, 100, 70),
            ("Voice at 500m (1kHz)", 1000, 500, 60),
            ("Low frequency (100Hz) at 100m", 100, 100, 60),
            ("High frequency (8kHz) at 50m", 8000, 50, 60),
        ]

        report = {
            "analysis_type": "directional_audio_feasibility",
            "environment": {
                "temperature_c": 20,
                "humidity_percent": 50,
                "pressure_pa": 101325
            },
            "scenarios": []
        }

        for desc, freq, dist, spl in scenarios:
            analysis = self.analyze_scenario(desc, freq, dist, spl)
            report["scenarios"].append(analysis)

        # Parametric array analysis
        report["parametric_array"] = self.model.parametric_array_analysis(
            primary_freq=40000,  # 40 kHz carrier
            difference_freq=1000,  # 1 kHz audible
            aperture=0.3,  # 30 cm array
            power=100  # 100W electrical
        )

        return report


def main():
    print("Directional Acoustics Physics Model")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python acoustics_model.py report     - Generate full feasibility report")
        print("  python acoustics_model.py analyze    - Interactive analysis")
        print("  python acoustics_model.py range <freq> <power> <aperture>")
        print("                                       - Calculate effective range")
        print()
        return

    cmd = sys.argv[1].lower()
    analyzer = FeasibilityAnalyzer()

    if cmd == "report":
        report = analyzer.generate_comprehensive_report()
        print("\nFeasibility Report")
        print("-" * 50)
        print(json.dumps(report, indent=2))

        # Save to file
        with open("acoustics_feasibility_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        print("\nReport saved to acoustics_feasibility_report.json")

    elif cmd == "analyze":
        model = DirectionalAcoustics()

        print("\nInteractive Analysis")
        print("-" * 30)

        freq = float(input("Frequency (Hz): ") or "1000")
        dist = float(input("Distance (m): ") or "100")
        power = float(input("Power (W): ") or "100")
        aperture = float(input("Aperture (m): ") or "0.5")

        source = AcousticSource(
            aperture_diameter=aperture,
            frequency=freq,
            power_watts=power
        )

        print(f"\nResults:")
        print(f"  Wavelength: {SPEED_OF_SOUND/freq:.3f} m")
        print(f"  Beamwidth: {model.beamwidth_degrees(aperture, freq):.1f}°")
        print(f"  SPL at {dist}m: {model.spl_at_distance(source, dist):.1f} dB")
        print(f"  Effective range (60dB): {model.effective_range(source, 60):.1f} m")

    elif cmd == "range":
        if len(sys.argv) < 5:
            print("Usage: python acoustics_model.py range <freq> <power> <aperture>")
            return

        freq = float(sys.argv[2])
        power = float(sys.argv[3])
        aperture = float(sys.argv[4])

        model = DirectionalAcoustics()
        source = AcousticSource(
            aperture_diameter=aperture,
            frequency=freq,
            power_watts=power
        )

        print(f"\nSource: {freq}Hz, {power}W, {aperture}m aperture")
        print(f"Effective range (60dB): {model.effective_range(source, 60):.1f} m")
        print(f"Effective range (50dB): {model.effective_range(source, 50):.1f} m")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
