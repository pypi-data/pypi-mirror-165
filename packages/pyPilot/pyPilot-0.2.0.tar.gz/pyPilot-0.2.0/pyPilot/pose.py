import sys
from os.path import dirname

import numpy as np
from numpy import rad2deg

SRC_DIR = dirname(__file__)
sys.path.append(SRC_DIR)

from pyPilot.pyPilot import DEGREES, RADIANS, NED_TO_BODY, poseMat, \
                            reversePoseMat, lla2ecef, dcm2angle, dcm2quat, \
                            transformPt, ned2lla, lla2ned, ecef2ned_dcm, \
                            ecef2lla, pose2dcm, pose2t


def payload2vehicle(pay, x):
	return transformPt(pay.v_P_p(), x).squeeze()

def vehicle2payload(pay, x):
	return transformPt(pay.p_P_v(), x).squeeze()

def sensor2vehicle(pay, sen, x):
	return transformPt(pay.v_P_p() @ sen.p_P_s(), x).squeeze()

def vehicle2sensor(pay, sen, x):
	return transformPt(sen.s_P_p() @ pay.p_P_v(), x).squeeze()

def sensor2payload(pay, sen, x):
	return transformPt(sen.p_P_s(), x).squeeze()

def payload2sensor(pay, sen, x):
	return transformPt(sen.s_P_p(), x).squeeze()


class vehicle_pose():
    def __init__(self, id):
        self._vehicleID = id
        
        self._lla = np.zeros(3) # dd, dd, m

        self._e_t_e_v = np.zeros(3) # translation vector (in m) from ECEF frame to vehicle's local level/NED frame in the ECEF frame
        self._n_R_e   = np.eye(3)   # dcm from ECEF frame to vehicle's local level/NED frame
        self._v_R_n   = np.eye(3)   # dcm from vehicle's local level/NED frame to vehicle's body frame
        self._n_P_e   = np.eye(4)   # pose matrix that maps points from the ECEF frame to the vehicle's local level/NED frame https://en.wikipedia.org/wiki/Affine_transformation
        self._v_P_e   = np.eye(4)   # pose matrix that maps points from the ECEF frame to the vehicle's body frame https://en.wikipedia.org/wiki/Affine_transformation
    
    def vehicleID(self):
        return self._vehicleID
    
    def e_t_e_v(self):
        return self._e_t_e_v
    
    def v_t_v_e(self):
        return -self._e_t_e_v
    
    def n_R_e(self):
        return self._n_R_e
    
    def e_R_n(self):
        return self._n_R_e.T
    
    def v_R_n(self):
        return self._v_R_n
    
    def n_R_v(self):
        return self._v_R_n.T
    
    def n_P_e(self):
        return self._n_P_e
    
    def e_P_n(self):
        return reversePoseMat(self._n_P_e).squeeze()
    
    def v_P_e(self):
        return self._v_P_e
    
    def e_P_v(self):
        return reversePoseMat(self._v_P_e).squeeze()
    
    def lla(self):
        return self._lla
    
    def ecef(self):
        return lla2ecef(self._lla, DEGREES).squeeze()
    
    def euler(self):
        return dcm2angle(self._v_R_n, DEGREES, NED_TO_BODY, 321).squeeze()
    
    def quat(self):
        return dcm2quat(self._v_R_n).squeeze()

    def body2ned(self, x):
        return self._v_R_n.T @ x
    
    def ned2body(self, x):
        return self._v_R_n @ x
    
    def body2ecef(self, x):
        return transformPt(self.e_P_v(), x)
    
    def ecef2body(self, x):
        return transformPt(self._v_P_e, x)
    
    def body2lla(self, x):
        return ned2lla(self._v_R_n.T @ x, self._lla, DEGREES)
    
    def lla2body(self, x):
        return self._v_R_n @ lla2ned(x, self._lla, DEGREES)
    
    def update_dcm(self, _v_R_n_):
        self._v_R_n = _v_R_n_
        self._v_P_e = poseMat(self._v_R_n @ self._n_R_e, self._e_t_e_v).squeeze()

    def update_loc_lla(self, _lla_, angle_unit):
        if angle_unit == RADIANS:
            self._lla = np.hstack([rad2deg(_lla_[0]),
                                   rad2deg(_lla_[1]),
                                   _lla_[2]])
        
        else:
            self._lla = _lla_

        self._e_t_e_v = lla2ecef(self._lla, DEGREES).squeeze()
        self._n_R_e   = ecef2ned_dcm(self._lla, DEGREES).squeeze()
        self._n_P_e   = poseMat(self._n_R_e, self._e_t_e_v).squeeze()
        self._v_P_e   = poseMat(self._v_R_n @ self._n_R_e, self._e_t_e_v).squeeze()

    def update_loc_ecef(self, _ecef_):
        self._lla     = ecef2lla(_ecef_, DEGREES).squeeze()
        self._e_t_e_v = _ecef_
        self._n_R_e   = ecef2ned_dcm(self._lla, DEGREES).squeeze()
        self._n_P_e   = poseMat(self._n_R_e, self._e_t_e_v).squeeze()
        self._v_P_e   = poseMat(self._v_R_n @ self._n_R_e, self._e_t_e_v).squeeze()


class payload_pose():
    def __init__(self, vid, pid):
        self._vehicleID = vid
        self._payloadID = pid
        
        self._v_t_v_p = np.zeros(3) # translation vector (in m) from vehicle CG to payload in the vehicle's body frame
        self._p_R_v   = np.eye(3)   # dcm from vehicle's body frame to payload's body frame
        self._p_P_v   = np.eye(4)   # pose matrix that maps points from the vehicle's body frame to the payload's body frame https://en.wikipedia.org/wiki/Affine_transformation
    
    def vehicleID(self):
        return self._vehicleID
    
    def payloadID(self):
        return self._payloadID
    
    def v_t_v_p(self):
        return self._v_t_v_p
    
    def p_t_p_v(self):
        return -self._v_t_v_p
    
    def p_R_v(self):
        return self._p_R_v
    
    def v_R_p(self):
        return self._p_R_v.T
    
    def p_P_v(self):
        return self._p_P_v
    
    def v_P_p(self):
        return reversePoseMat(self._p_P_v).squeeze()
    
    def update_v_t_v_p(self, _v_t_v_p_):
        self._v_t_v_p = _v_t_v_p_
        self._p_P_v   = poseMat(self._p_R_v, self._v_t_v_p).squeeze()
    
    def update_p_t_p_v(self, _p_t_p_v_):
        self._v_t_v_p = -_p_t_p_v_
        self._p_P_v   = poseMat(self._p_R_v, self._v_t_v_p).squeeze()
    
    def update_p_R_v(self, _p_R_v_):
        self._p_R_v = _p_R_v_
        self._p_P_v = poseMat(self._p_R_v, self._v_t_v_p).squeeze()
    
    def update_v_R_p(self, _v_R_p_):
        self._p_R_v = _v_R_p_.T
        self._p_P_v = poseMat(self._p_R_v, self._v_t_v_p).squeeze()
    
    def update_p_P_v(self, _p_P_v_):
        self._p_P_v   = _p_P_v_
        self._p_R_v   = pose2dcm(self._p_P_v).squeeze()
        self._v_t_v_p = pose2t(self._p_P_v).squeeze()
    
    def update_v_P_p(self, _v_P_p_):
        self._p_P_v   = reversePoseMat(_v_P_p_).squeeze()
        self._p_R_v   = pose2dcm(self._p_P_v).squeeze()
        self._v_t_v_p = pose2t(self._p_P_v).squeeze()


class sensor_pose():
    def __init__(self, vid, pid, sid):
        self._vehicleID = vid
        self._payloadID = pid
        self._sensorID  = sid
        
        self._p_t_p_s = np.zeros(3) # translation vector (in m) from payload to sensor in the payload's body frame
        self._s_R_p   = np.eye(3)   # dcm from payload's body frame to sensor's body frame
        self._s_P_p   = np.eye(4)   # pose matrix that maps points from the payload's body frame to the sensor's body frame https://en.wikipedia.org/wiki/Affine_transformation

    def sensorID(self):
        return self._sensorID

    def p_t_p_s(self):
        return self._p_t_p_s

    def s_t_s_p(self):
        return -self._p_t_p_s

    def s_R_p(self):
        return self._s_R_p

    def p_R_s(self):
        return self._s_R_p.T

    def s_P_p(self):
        return self._s_P_p

    def p_P_s(self):
        return reversePoseMat(self._s_P_p).squeeze()

    def update_p_t_p_s(self, _p_t_p_s_):
        self._p_t_p_s = _p_t_p_s_
        self._s_P_p   = poseMat(self._s_R_p, self._p_t_p_s).squeeze()

    def update_s_t_s_p(self, _s_t_s_p_):
        self._p_t_p_s = -_s_t_s_p_
        self._s_P_p   = poseMat(self._s_R_p, self._p_t_p_s).squeeze()

    def update_s_R_p(self, _s_R_p_):
        self._s_R_p = _s_R_p_
        self._s_P_p = poseMat(self._s_R_p, self._p_t_p_s).squeeze()

    def update_p_R_s(self, _p_R_s_):
        self._s_R_p = _p_R_s_.T
        self._s_P_p = poseMat(self._s_R_p, self._p_t_p_s).squeeze()

    def update_s_P_p(self, _s_P_p_):
        self._s_P_p   = _s_P_p_
        self._s_R_p   = pose2dcm(self._s_P_p).squeeze()
        self._p_t_p_s = pose2t(self._s_P_p).squeeze()

    def update_p_P_s(self, _p_P_s_):
        self._s_P_p   = reversePoseMat(_p_P_s_).squeeze()
        self._s_R_p   = pose2dcm(self._s_P_p).squeeze()
        self._p_t_p_s = pose2t(self._s_P_p).squeeze()
