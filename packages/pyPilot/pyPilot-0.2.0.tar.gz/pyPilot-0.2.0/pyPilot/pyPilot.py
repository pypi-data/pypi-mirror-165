import sys
from os.path import dirname

import numpy as np
import scipy.linalg as la
from numpy import rad2deg, deg2rad, sqrt, sin, arcsin, cos, tan, arctan2
from scipy.spatial.transform import Rotation as R

SRC_DIR = dirname(__file__)
sys.path.append(SRC_DIR)

import pilotUtils
import wgs84


RADIANS = True
DEGREES = False

NED_TO_BODY = True
BODY_TO_NED = False

dRx = 0 # w.r.t. rotation around the x axis
dRy = 1 # w.r.t. rotation around the y axis
dRz = 2 # w.r.t. rotation around the z axis
dtx = 3 # w.r.t. translation around the x axis
dty = 4 # w.r.t. translation around the y axis
dtz = 5 # w.r.t. translation around the z axis


def angle2dcm(angles:            np.ndarray,
              angle_unit:        bool,
              NED_to_body:       bool,
              rotation_sequence: int) -> np.ndarray:
    '''
    Description:
    ------------
    This function converts a vector of euler angles into a Direction Cosine
    Matrix (DCM) given a rotation and frame sequence. In the case of this
    function, the returned DCM maps vectors from one coordinate frame (either
    North-East-Down (NED) or body frame) into the other. This is done by
    multiplying the DCM with the vector to be rotated: v_body = DCM * v_NED.

    https://en.wikipedia.org/wiki/Rotation_matrix
    https://en.wikipedia.org/wiki/Axes_conventions
    https://en.wikipedia.org/wiki/Euler_angles
    
    Arguments:
    ----------
    angles
        Vector of euler angles to describe the rotation
    angle_unit
        Unit of the euler angles (rad or degrees)
    NED_to_body
        Rotate either to or from the NED frame
    rotation_sequence
        The order in which the euler angles are applied
        to the rotation. 321 is the standard rotation
        sequence for aerial navigation
    
    Returns:
    --------
    dcm
        Direction cosine matrix (rotation matix)
    '''
    
    if len(angles.shape) == 1:
        angles = angles.reshape(1, 3)
    
    num_angles = angles.shape[0]
    
    if angle_unit == DEGREES:
        roll  = np.radians(angles[:, 0])
        pitch = np.radians(angles[:, 1])
        yaw   = np.radians(angles[:, 2])
    else:
        roll  = angles[:, 0]
        pitch = angles[:, 1]
        yaw   = angles[:, 2]
    
    # For a single angle, DCM R1 would be:
    # R1 = np.array([[1,          0,         0],
    #                [0,  cos(roll), sin(roll)],
    #                [0, -sin(roll), cos(roll)]])
    
    R1 = np.zeros((num_angles, 3, 3))
    R1[:, 0, 0] = 1
    R1[:, 1, 1] = cos(roll)
    R1[:, 1, 2] = sin(roll)
    R1[:, 2, 1] = -sin(roll)
    R1[:, 2, 2] = cos(roll)

    # For a single angle, DCM R2 would be:
    # R2 = np.array([[cos(pitch), 0, -sin(pitch)],
    #                [0,          1,           0],
    #                [sin(pitch), 0,  cos(pitch)]])
    
    R2 = np.zeros((num_angles, 3, 3))
    R2[:, 0, 0] = cos(pitch)
    R2[:, 0, 2] = -sin(pitch)
    R2[:, 1, 1] = 1
    R2[:, 2, 0] = sin(pitch)
    R2[:, 2, 2] = cos(pitch)

    # For a single angle, DCM R3 would be:
    # R3 = np.array([[ cos(yaw), sin(yaw), 0],
    #                [-sin(yaw), cos(yaw), 0],
    #                [ 0,        0,        1]])
    
    R3 = np.zeros((num_angles, 3, 3))
    R3[:, 0, 0] = cos(yaw)
    R3[:, 0, 1] = sin(yaw)
    R3[:, 1, 0] = -sin(yaw)
    R3[:, 1, 1] = cos(yaw)
    R3[:, 2, 2] = 1

    if rotation_sequence == 321:
        dcms = R1 @ R2 @ R3
    elif rotation_sequence == 312:
        dcms = R2 @ R1 @ R3
    elif rotation_sequence == 231:
        dcms = R1 @ R3 @ R2
    elif rotation_sequence == 213:
        dcms = R3 @ R1 @ R2
    elif rotation_sequence == 132:
        dcms = R2 @ R3 @ R1
    elif rotation_sequence == 123:
        dcms = R3 @ R2 @ R1
    else:
        dcms = R1 @ R2 @ R3

    if not NED_to_body:
        return np.transpose(dcms, axes=(0, 2, 1))

    return dcms

def dcm2angle(dcm:               np.ndarray,
              angle_unit:        bool,
              NED_to_body:       bool,
              rotation_sequence: int) -> np.ndarray:
    '''
    Description:
    ------------
    This function converts a Direction Cosine Matrix (DCM) into the 
    corresponding euler angles.

    https://en.wikipedia.org/wiki/Rotation_matrix
    https://en.wikipedia.org/wiki/Axes_conventions
    https://en.wikipedia.org/wiki/Euler_angles

    Arguments:
    ----------
    dcm
        Direction cosine matrix (rotation matix)
    angle_unit
        Unit of the euler angles (rad or degrees)
    NED_to_body
        Rotate either to or from the NED frame
    rotation_sequence
        The order in which the euler angles are applied
        to the rotation. 321 is the standard rotation
        sequence for aerial navigation

    Returns:
    --------
    angles
        Vector of euler angles to describe the rotation
    '''
    
    if len(dcm.shape) < 3:
        dcm = dcm.reshape(1, 3, 3)
    
    if rotation_sequence == 321:
        if NED_to_body:
            angles = np.hstack([arctan2(dcm[:, 1, [2]], dcm[:, 2, [2]]),  # Roll
                               -arcsin(dcm[:,  0, [2]]),                  # Pitch
                                arctan2(dcm[:, 0, [1]], dcm[:, 0, [0]])]) # Yaw
        else:
            angles = np.hstack([arctan2(dcm[:, 2, [1]], dcm[:, 2, [2]]),  # Roll
                               -arcsin(dcm[:,  2, [0]]),                  # Pitch
                                arctan2(dcm[:, 1, [0]], dcm[:, 0, [0]])]) # Yaw

    if angle_unit == DEGREES:
        angles = rad2deg(angles)

    return angles

def angle2quat(angles:            np.ndarray,
               angle_unit:        bool,
               NED_to_body:       bool,
               rotation_sequence: int) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a sequence of euler angles to an equivalent unit quaternion.

    https://eater.net/quaternions
    https://en.wikipedia.org/wiki/Axes_conventions
    https://en.wikipedia.org/wiki/Euler_angles

    Arguments:
    ----------
    angles
        Vector of euler angles to describe the rotation
    angle_unit
        Unit of the euler angles (rad or degrees)
    NED_to_body
        Rotate either to or from the NED frame
    rotation_sequence
        The order in which the euler angles are applied
        to the rotation. 321 is the standard rotation
        sequence for aerial navigation

    Returns:
    --------
    np.ndarray
        Quaternion that describes the rotation
    '''
    
    r = R.from_matrix(angle2dcm(angles, angle_unit, NED_to_body, rotation_sequence))
    
    return r.as_quat()

def quat2angle(quat:              np.ndarray,
               angle_unit:        bool,
               NED_to_body:       bool,
               rotation_sequence: int) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a unit quaternion to the equivalent sequence of euler angles
    about the rotation_sequence axes.

    https://eater.net/quaternions
    https://en.wikipedia.org/wiki/Axes_conventions
    https://en.wikipedia.org/wiki/Euler_angles

    Arguments:
    ----------
    quat
        Quaternion that describes the rotation
    angle_unit
        Unit of the euler angles (rad or degrees)
    NED_to_body
        Rotate either to or from the NED frame
    rotation_sequence
        The order in which the euler angles are applied
        to the rotation. 321 is the standard rotation
        sequence for aerial navigation

    Returns:
    --------
    np.ndarray
        Vector of euler angles to describe the rotation
    '''
    
    r = R.from_quat(quat)

    return dcm2angle(r.as_matrix(), angle_unit, NED_to_body, rotation_sequence)

def quat2dcm(quat: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a single unit quaternion to one DCM.

    https://eater.net/quaternions
    https://en.wikipedia.org/wiki/Rotation_matrix
    https://en.wikipedia.org/wiki/Axes_conventions

    Arguments:
    ----------
    quat
        Quaternion that describes the rotation

    Returns:
    --------
    np.ndarray
        DCM that rotates vectors from one coordinate frame to the other
    '''
    
    r = R.from_quat(quat)
    
    return r.as_matrix()

def dcm2quat(dcm: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a DCM to a unit quaternion.

    https://eater.net/quaternions
    https://en.wikipedia.org/wiki/Rotation_matrix
    https://en.wikipedia.org/wiki/Axes_conventions

    Arguments:
    ----------
    dcm
        Direction cosine matrix (rotation matix)

    Returns:
    --------
    np.ndarray
        Quaternion that describes the rotation
    '''
    
    r = R.from_matrix(dcm)
    
    return r.as_quat()

def vec2dcm(vec: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a Rodrigues rotation vector to a DCM.

    **NOTE: The Rodrigues vector's rotation angle must be in RADIANS.**

    https://courses.cs.duke.edu/fall13/compsci527/notes/rodrigues.pdf
    https://en.wikipedia.org/wiki/Rotation_matrix

    Arguments:
    ----------
    vec
        Rodrigues rotation vector

    Returns:
    --------
    np.ndarray
        Direction cosine matrix (rotation matix)
    '''

    r = R.from_rotvec(vec)
    
    return r.as_matrix()

def dcm2vec(dcm: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a DCM to a Rodrigues rotation vector.

    https://courses.cs.duke.edu/fall13/compsci527/notes/rodrigues.pdf
    https://en.wikipedia.org/wiki/Rotation_matrix

    Arguments:
    ----------
    dcm
        Direction cosine matrix (rotation matix)

    Returns:
    --------
    np.ndarray
        Rodrigues rotation vector (rotation angle is in RADIANS)
    '''
    
    r = R.from_matrix(dcm)
    
    return r.as_rotvec()

def vec2quat(vec: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a Rodrigues rotation vector to a quaternion.

    **NOTE: The Rodrigues vector's rotation angle must be in RADIANS.**

    https://courses.cs.duke.edu/fall13/compsci527/notes/rodrigues.pdf
    https://eater.net/quaternions

    Arguments:
    ----------
    vec
        Rodrigues rotation vector

    Returns:
    --------
    np.ndarray
        Quaternion that describes the rotation
    '''
    
    r = R.from_rotvec(vec)
    
    return r.as_quat()

def quat2vec(quat: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a quaternion to a Rodrigues rotation vector.

    https://courses.cs.duke.edu/fall13/compsci527/notes/rodrigues.pdf
    https://eater.net/quaternions

    Arguments:
    ----------
    quat
        Quaternion that describes the rotation

    Returns:
    --------
    vec
        Rodrigues rotation vector (rotation angle is in RADIANS)
    '''
    
    r = R.from_quat(quat)
    
    return r.as_rotvec()

def vec2angle(vec:               np.ndarray,
              angle_unit:        bool,
              NED_to_body:       bool,
              rotation_sequence: int) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a Rodrigues rotation vector to a vector of euler angles.

    **NOTE: The Rodrigues vector's rotation angle must be in RADIANS.**

    https://courses.cs.duke.edu/fall13/compsci527/notes/rodrigues.pdf
    https://en.wikipedia.org/wiki/Axes_conventions
    https://en.wikipedia.org/wiki/Euler_angles

    Arguments:
    ----------
    vec
        Rodrigues rotation vector
    angle_unit
        Unit of the euler angles (rad or degrees)
    NED_to_body
        Rotate either to or from the NED frame
    rotation_sequence
        The order in which the euler angles are applied
        to the rotation. 321 is the standard rotation
        sequence for aerial navigation

    Returns:
    --------
    np.ndarray
        Vector of euler angles
    '''
    
    return dcm2angle(vec2dcm(vec),
                     angle_unit,
                     NED_to_body,
                     rotation_sequence)

def angle2vec(angles:            np.ndarray,
              angle_unit:        bool,
              NED_to_body:       bool,
              rotation_sequence: int) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a vector of euler angles to a Rodrigues rotation vector.

    https://courses.cs.duke.edu/fall13/compsci527/notes/rodrigues.pdf
    https://en.wikipedia.org/wiki/Axes_conventions
    https://en.wikipedia.org/wiki/Euler_angles

    Arguments:
    ----------
    angles
        Vector of euler angles
    angle_unit
        Unit of the euler angles (rad or degrees)
    NED_to_body
        Rotate either to or from the NED frame
    rotation_sequence
        The order in which the euler angles are applied
        to the rotation. 321 is the standard rotation
        sequence for aerial navigation

    Returns:
    --------
    np.ndarray
        Rodrigues rotation vector (rotation angle is in RADIANS)
    '''
    
    return dcm2vec(angle2dcm(angles, angle_unit, NED_to_body, rotation_sequence))

def earthGeoRad(_lat:       np.ndarray,
                angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate Earth's geocentric radius at a given geodetic latitude in
    meters. "The geocentric radius is the distance from the Earth's
    center to a point on the spheroid surface at geodetic latitude".

    https://en.wikipedia.org/wiki/Earth_radius
    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    _lat
        Angle of latitude
    angle_unit
        Unit of the latitude angle (rad or degrees)

    Returns:
    --------
    np.ndarray
        Earth's geocentric radius in meters at a given latitude in meters
    '''
    
    if type(_lat) is not np.ndarray:
        lat = np.array(_lat)
    
    else:
        lat = _lat.copy()
    
    if len(lat.shape) == 1:
        lat = lat.reshape(1, 1)

    if angle_unit == DEGREES:
        lat = deg2rad(lat)

    num = (wgs84.a_sqrd * cos(lat))**2 + (wgs84.b_sqrd * sin(lat))**2
    den = (wgs84.a * cos(lat))**2 + (wgs84.b * sin(lat))**2

    return sqrt(num / den)

def earthRad(_lat:       np.ndarray,
             angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate Earth's radius of curvature in the prime vertical (East -
    West) - denoted as N - and meridian (North - South) - denoted as
    M - at a given latitude.

    https://en.wikipedia.org/wiki/Radius_of_curvature
    https://en.wikipedia.org/wiki/Earth_radius
    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    _lat
        Angle of latitude
    angle_unit
        Unit of the latitude angle (rad or degrees)

    Returns:
    --------
    np.ndarray
        Earth's radii of curvature { N, M } in meters at a given latitude
    '''
    
    if type(_lat) is not np.ndarray:
        lat = np.array(_lat)
    
    else:
        lat = _lat.copy()
    
    if len(lat.shape) == 1:
        lat = lat.reshape(1, 1)

    if angle_unit == DEGREES:
        lat = deg2rad(lat)

    R_N = wgs84.a / sqrt(1 - (wgs84.ecc_sqrd * sin(lat)**2))
    R_M = (wgs84.a * (1 - wgs84.ecc_sqrd)) / (1 - (wgs84.ecc_sqrd * sin(lat)**2))**1.5
    
    return np.hstack([R_N.reshape(R_N.size, 1),  # Earth's prime-vertical radius of curvature
                      R_M.reshape(R_N.size, 1)]) # Earth's meridional radius of curvature

def earthAzimRad(lat:        np.ndarray,
                 _azimuth:   float,
                 angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate azimuthal radius at a given latitude. This is the
    Earth's radius of cuvature at a given latitude in the
    direction of a given asimuth.

    https://en.wikipedia.org/wiki/Radius_of_curvature
    https://en.wikipedia.org/wiki/Earth_radius
    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    _lat
        Angle of latitude
    angle_unit
        Unit of the latitude angle (rad or degrees)

    Returns:
    --------
    np.ndarray
        Earth's azimuthal radius in meters at a given latitude and azimuth
    '''
    
    if type(lat) is not np.ndarray:
        lat = np.array(lat)
    
    if type(_azimuth) is not np.ndarray:
        azimuth = np.array(_azimuth)
    
    else:
        azimuth = _azimuth.copy()

    if angle_unit == DEGREES:
        azimuth = deg2rad(azimuth)

    eradvec = earthRad(lat, angle_unit)
    N = eradvec[:, [0]]
    M = eradvec[:, [1]]

    return 1 / ((cos(azimuth)**2 / M) + (sin(azimuth)**2 / N))

def earthRate(_lat:       np.ndarray,
              angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate Earth's angular velocity in m/s resolved in the NED frame at a given
    latitude.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    _lat
        Angle of latitude
    angle_unit
        Unit of the latitude angle (rad or degrees)

    Returns:
    --------
    np.ndarray
        Earth's angular velocity resolved in the NED frame at a given latitude
    '''
    
    if type(_lat) is not np.ndarray:
        lat = np.array(_lat)
    
    else:
        lat = _lat.copy()
    
    if len(lat.shape) == 1:
        lat = lat.reshape(1, 1)

    if angle_unit == DEGREES:
        lat = deg2rad(lat)

    n =  wgs84.omega_E * cos(lat)
    e =  np.zeros(n.shape)
    d = -wgs84.omega_E * sin(lat)
    
    return np.hstack([n.reshape(n.size, 1),  # North velocity component
                      e.reshape(e.size, 1),  # East velocity component
                      d.reshape(d.size, 1)]) # Down velocity component

def llaRate(vned:       np.ndarray,
            lla:        np.ndarray,
            angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the latitude, longitude, and altitude (LLA) angular rates
    given the locally tangent velocity in the NED frame and latitude.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    vned
        Velocity vector in m/s in the NED frame
    lla
        LLA coordinate (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees) (this also affects the output units
        (rad/s or degrees/s)

    Returns:
    --------
    lla_dot
        LLA angular rates given the locally tangent velocity
        in the NED frame and latitude
    '''
    
    if len(vned.shape) == 1:
        vned = vned.reshape(1, 3)
        
    if len(lla.shape) == 1:
        lla = lla.reshape(1, 3)

    VN = vned[:, [0]]
    VE = vned[:, [1]]
    VD = vned[:, [2]]
    
    lat = lla[:, [0]]
    alt = lla[:, [2]]

    eradvec = earthRad(lat, angle_unit)
    Rew = eradvec[:, [0]]
    Rns = eradvec[:, [1]]

    if angle_unit == DEGREES:
        lat = deg2rad(lat)
    
    alt = alt.reshape(alt.size, 1)
    lat = lat.reshape(lat.size, 1)

    if angle_unit == RADIANS:
        lla_dot = np.hstack([VN / (Rns + alt),            # North component angular rate
                             VE / (Rew + alt) / cos(lat), # East component angular rate
                            -VD])                         # Down component angular rate
    
    else:
        lla_dot = np.hstack([rad2deg(VN / (Rns + alt)),            # North component angular rate
                             rad2deg(VE / (Rew + alt) / cos(lat)), # East component angular rate
                            -VD])                                  # Down component angular rate

    return lla_dot

def navRate(vned:       np.ndarray,
            lla:        np.ndarray,
            angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the navigation/transport angular rates given the locally tangent
    velocity in the NED frame and latitude. The navigation/transport rate is
    the angular velocity of the NED frame relative to the ECEF frame.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    vned
        Velocity vector in m/s in the NED frame
    lla
        LLA coordinate (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees) (this also affects the output units
        (rad/s or degrees/s)

    Returns:
    --------
    rho
        Navigation/transport angular rates in the ECEF frame given
        the locally tangent velocity in the NED frame and latitude
    '''
    
    if len(vned.shape) == 1:
        vned = vned.reshape(1, 3)
        
    if len(lla.shape) == 1:
        lla = lla.reshape(1, 3)
    
    VN = vned[:, [0]]
    VE = vned[:, [1]]

    lat = lla[:, [0]]
    alt = lla[:, [2]]

    eradvec = earthRad(lat, angle_unit)
    Rew = eradvec[:, [0]]
    Rns = eradvec[:, [1]]

    if angle_unit == DEGREES:
        lat = deg2rad(lat)
        
    Rew = Rew.reshape(Rew.size, 1)
    Rns = Rns.reshape(Rns.size, 1)
    alt = alt.reshape(alt.size, 1)
    lat = lat.reshape(lat.size, 1)
    
    if angle_unit == RADIANS:
        rho = np.hstack([VE / (Rew + alt),             # ECEF-X component angular rate
                        -VN / (Rns + alt),             # ECEF-Y component angular rate
                        -VE * tan(lat) / (Rew + alt)]) # ECEF-Z component angular rate
    
    else:
        rho = np.hstack([rad2deg(VE / (Rew + alt)),              # ECEF-X component angular rate
                         rad2deg(-VN / (Rns + alt)),             # ECEF-Y component angular rate
                         rad2deg(-VE * tan(lat) / (Rew + alt))]) # ECEF-Z component angular rate

    return rho

def lla2ecef(lla:        np.ndarray,
             angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a LLA coordinate to an ECEF coordinate.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system
    https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system

    Arguments:
    ----------
    lla
        LLA coordinate (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees)

    Returns:
    --------
    ecef
        ECEF coordinate in meters
    '''
    
    if len(lla.shape) == 1:
        lla = lla.reshape(1, 3)

    lat = lla[:, [0]]
    lon = lla[:, [1]]
    alt = lla[:, [2]]

    eradvec = earthRad(lat, angle_unit)
    Rew = eradvec[:, [0]]

    if angle_unit == DEGREES:
        lat = deg2rad(lat)
        lon = deg2rad(lon)

    ecef = np.hstack([(Rew + alt) * cos(lat) * cos(lon),
                      (Rew + alt) * cos(lat) * sin(lon),
                      ((1 - wgs84.ecc_sqrd) * Rew + alt) * sin(lat)])

    return ecef

def ecef2lla(ecef:       np.ndarray,
             angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Convert an ECEF coordinate to a LLA coordinate.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system
    https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system
    https://www.mathworks.com/help/aeroblks/ecefpositiontolla.html

    Arguments:
    ----------
    ecef
        ECEF coordinate in meters
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees)

    Returns:
    --------
    lla
        LLA coordinate (altitude in meters)
    '''
    
    if len(ecef.shape) == 1:
        ecef = ecef.reshape(1, 3)

    x = ecef[:, [0]]
    y = ecef[:, [1]]
    z = ecef[:, [2]]

    x_sqrd = x**2
    y_sqrd = y**2

    lon = arctan2(y, x)
    lat = np.ones(lon.shape) * 400

    s      = sqrt(x_sqrd + y_sqrd)
    beta   = arctan2(z, (1 - wgs84.f) * s)
    mu_bar = arctan2(z + (((wgs84.ecc_sqrd * (1 - wgs84.f)) / (1 - wgs84.ecc_sqrd)) * wgs84.a * sin(beta)**3),
                     s - (wgs84.ecc_sqrd * wgs84.a * cos(beta)**3))

    while ~(np.abs(lat - mu_bar) <= 1e-10).all():
        lat    = mu_bar
        beta   = arctan2((1 - wgs84.f) * sin(lat),
                         cos(lat))
        mu_bar = arctan2(z + (((wgs84.ecc_sqrd * (1 - wgs84.f)) / (1 - wgs84.ecc_sqrd)) * wgs84.a * sin(beta)**3),
                         s - (wgs84.ecc_sqrd * wgs84.a * cos(beta)**3))

    lat = mu_bar

    N = wgs84.a / sqrt(1 - (wgs84.ecc_sqrd * sin(lat)**2))
    h = (s * cos(lat)) + ((z + (wgs84.ecc_sqrd * N * sin(lat))) * sin(lat)) - N

    if angle_unit == DEGREES:
        lat = rad2deg(lat)
        lon = rad2deg(lon)
    
    lat = lat.reshape(lat.size, 1)
    lon = lon.reshape(lon.size, 1)
    h   = h.reshape(h.size, 1)

    lla = np.hstack([lat,
                     lon,
                     h])

    return lla

def ecef2ned_dcm(lla:        np.ndarray,
                 angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Find the direction cosine matrix that describes the rotation from the ECEF
    coordinate frame to the NED frame given a lat/lon/alt location.

    https://www.mathworks.com/help/aeroblks/directioncosinematrixeceftoned.html
    https://en.wikipedia.org/wiki/Rotation_matrix
    https://en.wikipedia.org/wiki/Geographic_coordinate_system
    https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system

    Arguments:
    ----------
    lla
        LLA coordinate (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees)

    Returns:
    --------
    C
        ECEF to NED DCM
    '''
    
    if len(lla.shape) == 1:
        lla = lla.reshape(1, 3)

    lat = lla[:, [0]]
    lon = lla[:, [1]]

    if angle_unit == DEGREES:
        lat = deg2rad(lat)
        lon = deg2rad(lon)

    C = np.zeros((lla.shape[0], 3, 3))

    C[:, 0, 0] = -sin(lat) * cos(lon)
    C[:, 0, 1] = -sin(lat) * sin(lon)
    C[:, 0, 2] = cos(lat)

    C[:, 1, 0] = -sin(lon)
    C[:, 1, 1] = cos(lon)
    C[:, 1, 2] = np.zeros(lon.shape)

    C[:, 2, 0] = -cos(lat) * cos(lon)
    C[:, 2, 1] = -cos(lat) * sin(lon)
    C[:, 2, 2] = -sin(lat)

    return C

def ecef2ned(ecef:       np.ndarray,
             lla_ref:    np.ndarray,
             angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Convert an ECEF coordinate to a NED coordinate.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system
    https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system

    Arguments:
    ----------
    ecef
        ECEF coordinate in meters
    lla_ref
        LLA coordinate of the NED frame origin (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees)

    Returns:
    --------
    ned
        NED coordinate in meters
    '''
    
    if len(ecef.shape) == 1:
        ecef = ecef.reshape(1, 3)
    
    if len(lla_ref.shape) == 1:
        lla_ref = lla_ref.reshape(1, 3)
    
    ecef_ref = lla2ecef(lla_ref, angle_unit)
    C        = ecef2ned_dcm(lla_ref, angle_unit)

    return C @ (ecef - ecef_ref)

def lla2ned(lla:        np.ndarray,
            lla_ref:    np.ndarray,
            angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a LLA coordinate to a NED coordinate.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    lla
        LLA coordinate (altitude in meters)
    lla_ref
        LLA coordinate of the NED frame origin (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees)

    Returns:
    --------
    ned
        NED coordinate in meters
    '''

    ecef = lla2ecef(lla, angle_unit)
    ned  = ecef2ned(ecef, lla_ref, angle_unit)

    return ned

def ned2ecef(ned:        np.ndarray,
             lla_ref:    np.ndarray,
             angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a NED coordinate to an ECEF coordinate.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system
    https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system

    Arguments:
    ----------
    ned
        NED coordinate in meters
    lla_ref
        LLA coordinate of the NED frame origin (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees)

    Returns:
    --------
    ecef
        ECEF coordinate in meters
    '''
    
    if len(ned.shape) == 1:
        ned = ned.reshape(1, 3)
    
    if len(lla_ref.shape) == 1:
        lla_ref = lla_ref.reshape(1, 3)

    lat_ref = lla_ref[:, 0]
    lon_ref = lla_ref[:, 1]

    if angle_unit == DEGREES:
        lat_ref = deg2rad(lat_ref)
        lon_ref = deg2rad(lon_ref)

    C = np.zeros((ned.shape[0], 3, 3))

    C[:, 0, 0] = -sin(lat_ref) * cos(lon_ref)
    C[:, 0, 1] = -sin(lat_ref) * sin(lon_ref)
    C[:, 0, 2] =  cos(lat_ref)

    C[:, 1, 0] = -sin(lon_ref)
    C[:, 1, 1] =  cos(lon_ref)
    C[:, 1, 2] =  np.zeros(lon_ref.shape)

    C[:, 2, 0] = -cos(lat_ref) * cos(lon_ref)
    C[:, 2, 1] = -cos(lat_ref) * sin(lon_ref)
    C[:, 2, 2] = -sin(lat_ref)

    ecef = np.transpose(C, axes=(0, 2, 1)) @ ned

    return ecef

def ned2lla(ned:        np.ndarray,
            lla_ref:    np.ndarray,
            angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Convert a NED coordinate to a LLA coordinate.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    ned
        NED coordinate in meters
    lla_ref
        LLA coordinate of the NED frame origin (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees)

    Returns:
    --------
    lla
        LLA coordinate (altitude in meters)
    '''

    ecef     = ned2ecef(ned, lla_ref, angle_unit)
    ecef_ref = lla2ecef(lla_ref, angle_unit)
    ecef    += ecef_ref

    lla = ecef2lla(ecef, angle_unit)

    return lla

def poseMat(dcm: np.ndarray,
            t:   np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Create a 4x4 pose matrix that can be used to apply an affine transform of a
    3 dimensional vector/point from one coordinate frame to another. The two
    coordinate frames do not need to be colocated.

    https://en.wikipedia.org/wiki/Affine_transformation

    Arguments:
    ----------
    dcm
        Direction cosine matrix that describes the rotation
        between the two coordinate frames
    t
        Translation vector between the origins of the two
        coordinate frames (unit of distance is arbitrary - 
        up to the user to decide)

    Returns:
    --------
    poseMatrix
        4x4 pose matrix for affine coordinate frame transforms
    '''
    
    if len(dcm.shape) < 3:
        dcm = dcm.reshape(1, 3, 3)
    
    if len(t.shape) < 3:
        t = t.reshape(1, 1, 3)

    poseMatrix = np.zeros((dcm.shape[0], 4, 4))
    
    poseMatrix[:, :3, :3] = dcm
    poseMatrix[:, :3,  3] = np.transpose(t, axes=(0, 2, 1)).squeeze()
    poseMatrix[:,  3,  3] = 1

    return poseMatrix

def pose2dcm(poseMatrix: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Extract the DCM from a given pose matrix.

    https://en.wikipedia.org/wiki/Affine_transformation
    https://en.wikipedia.org/wiki/Rotation_matrix

    Arguments:
    ----------
    poseMatrix
        4x4 pose matrix for affine coordinate frame
        transforms

    Returns:
    --------
    dcm
        DCM extracted from pose matrix
    '''
    
    if len(poseMatrix.shape) < 3:
        poseMatrix = poseMatrix.reshape(1, 4, 4)
    
    dcm = poseMatrix[:, :3, :3]

    return dcm

def pose2t(poseMatrix: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Extract translation vector from a given pose matrix.

    https://en.wikipedia.org/wiki/Affine_transformation

    Arguments:
    ----------
    poseMatrix
        4x4 pose matrix for affine coordinate frame
        transforms

    Returns:
    --------
    t
        Translation vector extracted from pose matrix
    '''
    
    if len(poseMatrix.shape) < 3:
        poseMatrix = poseMatrix.reshape(1, 4, 4)
    
    t = poseMatrix[:, :3, 3]

    return t

def reversePoseMat(poseMatrix: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Create a reversed 4x4 pose matrix.

    https://en.wikipedia.org/wiki/Affine_transformation

    Arguments:
    ----------
    poseMatrix
        4x4 pose matrix for affine coordinate frame
        transforms

    Returns:
    --------
    inv_poseMatrix
        Reversed 4x4 pose matrix for affine coordinate frame
        transforms
    '''
    
    dcm = pose2dcm(poseMatrix)
    t   = pose2t(poseMatrix).T
    t   = t.reshape(t.shape[1], 3, 1)
        
    dcm_T = np.transpose(dcm, axes=(0, 2, 1))
    t_T   = np.transpose(dcm_T @ -t, axes=(0, 2, 1))

    inv_poseMatrix = poseMat(dcm_T, t_T)
    
    return inv_poseMatrix

def skew(w: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Make a skew symmetric matrix from a 3 element vector. Skew
    symmetric matrices are often used to easily take cross products.

    https://en.wikipedia.org/wiki/Skew-symmetric_matrix

    Arguments:
    ----------
    w
        3 element vector

    Returns:
    --------
    C
        Skew symmetric matrix of vector w
    '''
    
    if len(w.shape) == 1:
        w = w.reshape(1, 3)
    
    C = np.zeros((w.shape[0], 3, 3))

    C[:, 0, 1] = -w[:, 2]
    C[:, 0, 2] =  w[:, 1]
    C[:, 1, 0] =  w[:, 2]
    C[:, 1, 2] = -w[:, 0]
    C[:, 2, 0] = -w[:, 1]
    C[:, 2, 1] =  w[:, 0]

    return C

def poseMatDeriv(poseMatrix: np.ndarray,
                 derivType:  np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Compute the matrix derivative of the given pose matrix w.r.t the given variable.
    The possible variables include:
    * dRx - w.r.t. rotation around the x axis
    * dRy - w.r.t. rotation around the y axis
    * dRz - w.r.t. rotation around the z axis
    * dtx - w.r.t. translation along the x axis
    * dty - w.r.t. translation along the y axis
    * dtz - w.r.t. translation along the z axis

    This operation is often used when constructing Jacobian matrices for optimization
    problems (i.e. least squares/GN optimization)

    https://en.wikipedia.org/wiki/Affine_transformation
    https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant
    https://en.wikipedia.org/wiki/Gauss%E2%80%93Newton_algorithm

    Arguments:
    ----------
    poseMatrix
        4x4 pose matrix for affine coordinate frame
        transforms
    derivType
        Variable to take the derivative w.r.t.

    Returns:
    --------
    poseMatrix
        Pose matrix derivative
    '''
    
    if len(poseMatrix.shape) < 3:
        poseMatrix = poseMatrix.reshape(1, 4, 4)
    
    dcm       = pose2dcm(poseMatrix)
    derivPose = np.zeros(poseMatrix.shape)
    vec       = np.zeros((poseMatrix.shape[0], 3))
    
    if derivType == dRx:
        vec[:, 0] = 1
        
        derivPose[:, :2, :2] = skew(vec) @ dcm

    if derivType == dRy:
        vec[:, 1] = 1
        
        derivPose[:, :2, :2] = skew(vec) @ dcm

    if derivType == dRz:
        vec[:, 2] = 1
        
        derivPose[:, :2, :2] = skew(vec) @ dcm

    if derivType == dtx:
        vec[:, 0] = 1
        
        tempPose = np.zeros(poseMatrix.shape)
        tempPose[:, 3, :2] = vec

        derivPose = tempPose @ poseMatrix

    if derivType == dty:
        vec[:, 1] = 1
        
        tempPose = np.zeros(poseMatrix.shape)
        tempPose[:, 3, :2] = vec

        derivPose = tempPose @ poseMatrix

    if derivType == dtz:
        vec[:, 2] = 1
        
        tempPose = np.zeros(poseMatrix.shape)
        tempPose[:, 3, :2] = vec

        derivPose = tempPose @ poseMatrix

    return derivPose

def transformPt(poseMatrix: np.ndarray,
                x:          np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Applies an affine transformation to vector/point x described by the given pose
    matrix. This affine transformation converts the vector/point x from it's
    initial coordinate frame to another. A common use of this function would be
    to convert a 3D point in an airplane's sensor's body frame into the airplane's
    body frame (and vice versa).

    https://en.wikipedia.org/wiki/Affine_transformation

    Arguments:
    ----------
    poseMatrix
        4x4 pose matrix for affine coordinate frame
        transforms
    x
        The vector/point to be transformed

    Returns:
    --------
    new_x
        The vector/point transformed to the new coordinate frame
    '''
    
    if len(poseMatrix.shape) < 3:
        poseMatrix = poseMatrix.reshape(1, 4, 4)
    
    if len(x.shape) < 3:
        x = x.reshape(1, 1, 3)
    
    x_1 = np.ones((x.shape[0], x.shape[1], 4))
    x_1[:, :, :3] = x
    
    new_x_1 = np.transpose((poseMatrix @ np.transpose(x_1, axes=(0, 2, 1))), axes=(0, 2, 1))
    new_x   = new_x_1[:, :, :3].squeeze()

    return new_x

def bearingLla(lla_1:      np.ndarray,
               lla_2:      np.ndarray,
               angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the bearing between two LLA coordinates.

    http://www.movable-type.co.uk/scripts/latlong.html
    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    lla_1
        First LLA coordinate (altitude in meters)
    lla_2
        Second LLA coordinate (altitude in meters)
    angle_unit
        Unit of the latitude, longitude, and bearing
        angles (rad or degrees)

    Returns:
    --------
    bearing
        The bearing between the two given LLA coordinates
    '''
    
    if len(lla_1.shape) == 1:
        lla_1 = lla_1.reshape(1, 3)
    
    if len(lla_2.shape) == 1:
        lla_2 = lla_2.reshape(1, 3)
    
    lat_1 = lla_1[:, [0]]
    lon_1 = lla_1[:, [1]]

    lat_2 = lla_2[:, [0]]
    lon_2 = lla_2[:, [1]]

    if angle_unit == DEGREES:
        lat_1 = deg2rad(lat_1)
        lon_1 = deg2rad(lon_1)

        lat_2 = deg2rad(lat_2)
        lon_2 = deg2rad(lon_2)

    deltaLon = lon_2 - lon_1

    x = cos(lat_2) * sin(deltaLon)
    y = (cos(lat_1) * sin(lat_2)) - (sin(lat_1) * cos(lat_2) * cos(deltaLon))
    
    if angle_unit == DEGREES:
        return (rad2deg(arctan2(x, y)) + 360) % 360
    return pilotUtils.wrapToPi(arctan2(x, y))

def bearingNed(ned_1: np.ndarray,
               ned_2: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the bearing between two NED coordinates.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    ned_1
        First NED coordinate in meters
    ned_2
        Second NED coordinate in meters
    angle_unit
        Unit of the latitude, longitude, and bearing
        angles (rad or degrees)

    Returns:
    --------
    bearing
        The bearing between the two given LLA coordinates
    '''
    
    if len(ned_1.shape) == 1:
        ned_1 = ned_1.reshape(1, 3)
    
    if len(ned_2.shape) == 1:
        ned_2 = ned_2.reshape(1, 3)
    
    n_1 = ned_1[:, [0]]
    e_1 = ned_1[:, [1]]

    n_2 = ned_2[:, [0]]
    e_2 = ned_2[:, [1]]

    x = e_2 - e_1
    y = n_2 - n_1

    return (rad2deg(arctan2(x, y)) + 360) % 360

def distanceLla(lla_1:      np.ndarray,
                lla_2:      np.ndarray,
                angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the arc distance between two LLA coordinates.

    http://www.movable-type.co.uk/scripts/latlong.html
    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    lla_1
        First LLA coordinate (altitude in meters)
    lla_2
        Second LLA coordinate (altitude in meters)
    angle_unit
        Unit of the latitude and longitude angles (rad
        or degrees)

    Returns:
    --------
    dist
        The distance between the two given LLA coordinates in meters
    '''
    
    if len(lla_1.shape) == 1:
        lla_1 = lla_1.reshape(1, 3)
    
    if len(lla_2.shape) == 1:
        lla_2 = lla_2.reshape(1, 3)
    
    lat_1 = lla_1[:, [0]]
    lon_1 = lla_1[:, [1]]

    lat_2 = lla_2[:, [0]]
    lon_2 = lla_2[:, [1]]

    if angle_unit == DEGREES:
        lat_1 = deg2rad(lat_1)
        lon_1 = deg2rad(lon_1)

        lat_2 = deg2rad(lat_2)
        lon_2 = deg2rad(lon_2)

    deltaLat = lat_2 - lat_1
    deltaLon = lon_2 - lon_1

    _a = (sin(deltaLat / 2) * sin(deltaLat / 2)) + cos(lat_1) * cos(lat_2) * (sin(deltaLon / 2)) * (sin(deltaLon / 2))

    azimuth = bearingLla(lla_1, lla_2, angle_unit)
    radius  = earthAzimRad(lat_1, azimuth, angle_unit)

    return 2 * radius * arctan2(sqrt(_a), sqrt(1 - _a))

def distanceNed(ned_1: np.ndarray,
                ned_2: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the total distance between two NED coordinates.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    ned_1
        First NED coordinate in meters
    ned_2
        Second NED coordinate in meters

    Returns:
    --------
    dist
        The total distance between the two given NED coordinates
    '''
    
    if len(ned_1.shape) == 1:
        ned_1 = ned_1.reshape(1, 3)
    
    if len(ned_2.shape) == 1:
        ned_2 = ned_2.reshape(1, 3)
    
    ned_diff = ned_2 - ned_1
    
    return la.norm(ned_diff, axis=1)[:, np.newaxis]

def distanceNedHoriz(ned_1: np.ndarray,
                     ned_2: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the horizontal distance between two NED coordinates.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    ned_1
        First NED coordinate in meters
    ned_2
        Second NED coordinate in meters

    Returns:
    --------
    dist
        The horizontal distance between the two given NED coordinates
    '''
    
    if len(ned_1.shape) == 1:
        ned_1 = ned_1.reshape(1, 3)
    
    if len(ned_2.shape) == 1:
        ned_2 = ned_2.reshape(1, 3)
    
    ned_diff = (ned_2 - ned_1)[:, :2]

    return la.norm(ned_diff, axis=1)[:, np.newaxis]

def distanceNedVert(ned_1: np.ndarray,
                    ned_2: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the vertical distance between two NED coordinates.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    ned_1
        First NED coordinate in meters
    ned_2
        Second NED coordinate in meters

    Returns:
    --------
    dist
        The vertical distance between the two given NED coordinates
    '''
    
    if len(ned_1.shape) == 1:
        ned_1 = ned_1.reshape(1, 3)
    
    if len(ned_2.shape) == 1:
        ned_2 = ned_2.reshape(1, 3)
    
    dist = (ned_2 - ned_1)[:, 3]
    
    return dist

def distanceEcef(ecef_1: np.ndarray,
                 ecef_2: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the total distance between two ECEF coordinates.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system
    https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system

    Arguments:
    ----------
    ecef_1
        First ECEF coordinate in meters
    ecef_2
        Second ECEF coordinate in meters

    Returns:
    --------
    dist
        The total distance between the two given ECEF coordinates
    '''
    
    if len(ecef_1.shape) == 1:
        ecef_1 = ecef_1.reshape(1, 3)
    
    if len(ecef_2.shape) == 1:
        ecef_2 = ecef_2.reshape(1, 3)
    
    ecef_diff = ecef_2 - ecef_1
    
    return la.norm(ecef_diff, axis=1)[:, np.newaxis]

def elevationLla(lla_1:      np.ndarray,
                 lla_2:      np.ndarray,
                 angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the elevation angle between two LLA coordinates.

    http://www.movable-type.co.uk/scripts/latlong.html
    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    lla_1
        First LLA coordinate (altitude in meters)
    lla_2
        Second LLA coordinate (altitude in meters)
    angle_unit
        Unit of the latitude, longitude, and elevation
        angles (rad or degrees)

    Returns:
    --------
    elevation
        The elevation angle between the two given LLA coordinates
    '''
    
    if len(lla_1.shape) == 1:
        lla_1 = lla_1.reshape(1, 3)
    
    if len(lla_2.shape) == 1:
        lla_2 = lla_2.reshape(1, 3)
    
    lat_1 = lla_1[:, [0]]
    lon_1 = lla_1[:, [1]]
    alt_1 = lla_1[:, [2]]

    lat_2 = lla_2[:, [0]]
    lon_2 = lla_2[:, [1]]
    alt_2 = lla_2[:, [2]]

    if angle_unit == DEGREES:
        lat_1 = deg2rad(lat_1)
        lon_1 = deg2rad(lon_1)

        lat_2 = deg2rad(lat_2)
        lon_2 = deg2rad(lon_2)

    dist   = distanceLla(lla_1, lla_2, angle_unit)
    height = alt_2 - alt_1

    return rad2deg(arctan2(height, dist))

def elevationNed(ned_1: np.ndarray,
                 ned_2: np.ndarray) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate the elevation angle between two NED coordinates.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    ned_1
        First NED coordinate (altitude in meters)
    ned_2
        Second NED coordinate (altitude in meters)

    Returns:
    --------
    elevation
        The elevation angle between the two given NED coordinates
    '''
    
    if len(ned_1.shape) == 1:
        ned_1 = ned_1.reshape(1, 3)
    
    if len(ned_2.shape) == 1:
        ned_2 = ned_2.reshape(1, 3)
    
    d_1 = -ned_1[:, [2]]
    d_2 = -ned_2[:, [2]]

    dist   = distanceNed(ned_1, ned_2)
    height = d_2 - d_1

    return rad2deg(arctan2(height, dist))

def LDAE2lla(lla:        np.ndarray,
             dist:       np.ndarray,
             _azimuth:   np.ndarray,
             _elevation: np.ndarray,
             angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate a LLA coordinate based on a given LLA coordinate, distance,
    azimuth, and elevation angle.

    http://www.movable-type.co.uk/scripts/latlong.html
    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    lla
        LLA coordinate (altitude in meters)
    dist
        "As the crow flies" distance between the two
        LLA coordinates in meters
    _azimuth
        Azimuth angle between the two LLA coordinates
    _elevation
        Elevation angle between the two LLA coordinates
    angle_unit
        Unit of the latitude, longitude, azimuth, and
        elevation angles (rad or degrees)

    Returns:
    --------
    new_lla
        New LLA coordinate (altitude in meters)
    '''
    
    if type(dist) is not np.ndarray:
        dist = np.array(dist)
    
    if type(_azimuth) is not np.ndarray:
        _azimuth = np.array(_azimuth)
    
    if type(_elevation) is not np.ndarray:
        _elevation = np.array(_elevation)
    
    if len(lla.shape) == 1:
        lla = lla.reshape(1, 3)
    
    if len(dist.shape) == 1:
        dist = dist.reshape(1, 3)
    
    if len(_azimuth.shape) == 1:
        azimuth = _azimuth.reshape(1, 3)
    else:
        azimuth = _azimuth.copy()
    
    if len(_elevation.shape) == 1:
        elevation = _elevation.reshape(1, 3)
    else:
        elevation = _elevation.copy()
    
    lat = lla[:, [0]]
    lon = lla[:, [1]]
    alt = lla[:, [2]]

    if angle_unit == DEGREES:
        lat = deg2rad(lat)
        lon = deg2rad(lon)

        azimuth   = deg2rad(azimuth)
        elevation = deg2rad(elevation)

    radius   = earthAzimRad(lat, _azimuth, angle_unit)
    adj_dist = dist / radius

    lat_2 = arcsin(sin(lat) * cos(adj_dist) + cos(lat) * sin(adj_dist) * cos(azimuth))
    lon_2 = lon + arctan2(sin(azimuth) * sin(adj_dist) * cos(lat),
                          cos(adj_dist) - sin(lat) * sin(lat_2))

    if angle_unit == DEGREES:
        new_lla = np.hstack([rad2deg(lat_2),
                             rad2deg(lon_2),
                             alt + (dist * tan(elevation))])
    else:
        new_lla = np.hstack([lat_2,
                             lon_2,
                             alt + (dist * tan(elevation))])

    return new_lla

def NDAE2ned(ned:        np.ndarray,
             dist:       np.ndarray,
             _azimuth:   np.ndarray,
             _elevation: np.ndarray,
             angle_unit: bool) -> np.ndarray:
    '''
    Description:
    ------------
    Calculate a NED coordinate based on a given NED coordinate, distance,
    azimuth, and elevation angle.

    https://en.wikipedia.org/wiki/Geographic_coordinate_system

    Arguments:
    ----------
    ned
        NED coordinate in meters
    dist
        Horizontal distance between the two
        NED coordinates in meters
    _azimuth
        Azimuth angle between the two NED coordinates
    _elevation
        Elevation angle between the two NED coordinates
    angle_unit
        Unit of the azimuth and elevation angles (rad
        or degrees)

    Returns:
    --------
    new_ned
        New NED coordinate in meters
    '''
    
    if type(dist) is not np.ndarray:
        dist = np.array(dist)
    
    if type(_azimuth) is not np.ndarray:
        _azimuth = np.array(_azimuth)
    
    if type(_elevation) is not np.ndarray:
        _elevation = np.array(_elevation)
    
    if len(ned.shape) == 1:
        ned = ned.reshape(1, 3)
    
    if len(dist.shape) == 1:
        dist = dist.reshape(1, 3)
    
    if len(_azimuth.shape) == 1:
        azimuth = _azimuth.reshape(1, 3)
    else:
        azimuth = _azimuth.copy()
    
    if len(_elevation.shape) == 1:
        elevation = _elevation.reshape(1, 3)
    else:
        elevation = _elevation.copy()
    
    n = ned[:, [0]]
    e = ned[:, [1]]
    d = ned[:, [2]]

    if angle_unit == DEGREES:
        azimuth   = deg2rad(azimuth)
        elevation = deg2rad(elevation)

    new_ned = np.hstack([n + (dist * cos(azimuth)),
                         e + (dist * sin(azimuth)),
                         d + (dist * tan(elevation))])

    return new_ned
