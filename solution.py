
Antenna transmission line calc · PY
"""
Transmission Line & Quarter-Wave Antenna Engineering Calculator
=================================================================
Covers:
  - Wavelength / quarter-wavelength calculation
  - Coaxial & parallel-wire characteristic impedance (Z0)
  - Quarter-wave transformer matching
  - Impedance transformation through a lossless line
  - Reflection coefficient & SWR
  - Physical monopole/dipole length approximations
"""
 
import cmath
import math
 
C = 3e8  # speed of light, m/s
 
 
# ---------------------------------------------------------------------
# 1. Wavelength & Quarter-Wavelength
# ---------------------------------------------------------------------
def wavelength(freq_hz, velocity_factor=1.0):
    """Return wavelength (m) given frequency (Hz) and velocity factor."""
    return (C * velocity_factor) / freq_hz
 
 
def quarter_wave_length(freq_hz, velocity_factor=1.0):
    """Return physical quarter-wavelength (m)."""
    return wavelength(freq_hz, velocity_factor) / 4
 
 
# ---------------------------------------------------------------------
# 2. Characteristic Impedance (Z0)
# ---------------------------------------------------------------------
def z0_coax(D_outer, d_inner, epsilon_r=1.0):
    """Coax characteristic impedance. D, d in same units (e.g. mm)."""
    return (138 / math.sqrt(epsilon_r)) * math.log10(D_outer / d_inner)
 
 
def z0_twin_lead(spacing, wire_diameter, epsilon_r=1.0):
    """Parallel two-wire line characteristic impedance."""
    return (276 / math.sqrt(epsilon_r)) * math.log10((2 * spacing) / wire_diameter)
 
 
# ---------------------------------------------------------------------
# 3. Quarter-Wave Transformer Matching
# ---------------------------------------------------------------------
def quarter_wave_transformer_z0(z_in, z_load):
    """
    Required Z0 of a quarter-wave matching section
    to match z_in (source/feed) to z_load (antenna).
    """
    return math.sqrt(z_in * z_load)
 
 
def input_impedance_quarter_wave(z0, z_load):
    """
    Impedance seen looking into a quarter-wave line
    of characteristic impedance z0 terminated in z_load.
    (Works with complex z_load too.)
    """
    return (z0 ** 2) / z_load
 
 
# ---------------------------------------------------------------------
# 4. General Transmission Line Input Impedance (any length)
# ---------------------------------------------------------------------
def input_impedance_line(z0, z_load, length, wavelength_m):
    """
    General lossless transmission line input impedance formula:
    Zin = Z0 * (ZL + j*Z0*tan(beta*l)) / (Z0 + j*ZL*tan(beta*l))
    length and wavelength_m must be in the same units.
    """
    beta = 2 * math.pi / wavelength_m
    bl = beta * length
    zl = complex(z_load)
    numerator = zl + 1j * z0 * math.tan(bl)
    denominator = z0 + 1j * zl * math.tan(bl)
    return z0 * (numerator / denominator)
 
 
# ---------------------------------------------------------------------
# 5. Reflection Coefficient & SWR
# ---------------------------------------------------------------------
def reflection_coefficient(z_load, z0):
    zl = complex(z_load)
    return (zl - z0) / (zl + z0)
 
 
def swr(z_load, z0):
    gamma = abs(reflection_coefficient(z_load, z0))
    if gamma >= 1:
        return float('inf')
    return (1 + gamma) / (1 - gamma)
 
 
# ---------------------------------------------------------------------
# 6. Physical Antenna Element Length Approximations
# ---------------------------------------------------------------------
def monopole_quarter_wave_ft(freq_mhz):
    """Practical quarter-wave monopole length in feet (accounts for end effect)."""
    return 234 / freq_mhz
 
 
def monopole_quarter_wave_m(freq_mhz):
    """Practical quarter-wave monopole length in meters."""
    return 71.3 / freq_mhz
 
 
def dipole_half_wave_ft(freq_mhz):
    """Practical half-wave dipole length in feet."""
    return 468 / freq_mhz
 
 
def dipole_half_wave_m(freq_mhz):
    """Practical half-wave dipole length in meters."""
    return 143 / freq_mhz
 
 
# ---------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------
if __name__ == "__main__":
    freq = 100e6  # 100 MHz
    vf = 0.66     # RG-58 velocity factor
 
    lam = wavelength(freq, vf)
    qw = quarter_wave_length(freq, vf)
    print(f"Frequency: {freq/1e6:.1f} MHz, velocity factor: {vf}")
    print(f"Wavelength: {lam:.3f} m")
    print(f"Quarter wavelength: {qw:.3f} m ({qw*100:.1f} cm)\n")
 
    z_in = 50
    z_load = 300  # e.g. folded dipole feed impedance
    z0_match = quarter_wave_transformer_z0(z_in, z_load)
    print(f"Quarter-wave transformer Z0 to match {z_in} ohm to {z_load} ohm: "
          f"{z0_match:.2f} ohm\n")
 
    # Check SWR before/after matching
    print(f"SWR of {z_load} ohm load on {z_in} ohm line (no match): "
          f"{swr(z_load, z_in):.2f}:1")
    print(f"SWR of {z_load} ohm load on {z0_match:.2f} ohm matching section: "
          f"{swr(z_load, z0_match):.2f}:1\n")
 
    freq_mhz = 100
    print(f"Practical quarter-wave monopole @ {freq_mhz} MHz: "
          f"{monopole_quarter_wave_m(freq_mhz):.3f} m "
          f"({monopole_quarter_wave_ft(freq_mhz):.3f} ft)")
    print(f"Practical half-wave dipole @ {freq_mhz} MHz: "
          f"{dipole_half_wave_m(freq_mhz):.3f} m "
          f"({dipole_half_wave_ft(freq_mhz):.3f} ft)")
 
