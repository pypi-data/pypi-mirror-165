'''
WGS 84 four defining parameters and several commonly used derived parameters.
All parameters are stored with the exact number of significant digits provided
by the WGS 84 rublished report.
'''


# WGS 84 Defining Parameters
a           = 6378137.0;           # Semi - major Axis[m]
a_sqrd      = a**2;                # Semi - major Axis[m] squared
f           = 1.0 / 298.257223563; # Flattening
omega_E     = 7292115.0e-11;       # Angular velocity of the Earth[rad / s]
omega_E_GPS = 7292115.1467e-11;    # Angular velocity of the Earth[rad / s]
                                         # According to ICD - GPS - 200

GM = 3.986004418e14; # Earth's Gravitational Constant [m^3/s^2]
                     # (mass of earth's atmosphere included)

GM_GPS = 3.9860050e14; # The WGS 84 GM value recommended for GPS receiver usage
                       # by the GPS interface control document(ICD - GPS - 200)
                       # differs from the current refined WGS 84 GM value.

# WGS 84 Ellipsoid Derived Geometric Constants
b              = 6356752.3142;       # Semi - minor axis[m]
b_sqrd         = b**2;               # Semi - minor axis[m] squared
ecc            = 8.1819190842622e-2; # First eccentricity
ecc_sqrd       = ecc**2;             # First eccentricity squared
ecc_prime      = 8.2094437949696e-2; # Second eccentricity
ecc_prime_sqrd = ecc_prime**2;       # Second eccentricity squared
r              = (2*a + b) / 3;      # Arithmetic mean radius [m]