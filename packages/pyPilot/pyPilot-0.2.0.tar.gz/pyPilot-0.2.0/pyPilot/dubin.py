''' TODO
from enum import IntEnum


class point(object):
    def __init__(self):
        self.maxRoll    = 0 # °
        self.minTurnRad = 0 # m
        self.hitRadius  = 0 # m
        
        self.alt     = 0 # m
        self.speed   = 0 # m/s
        self.heading = 0 # °
        self.lat     = 0 # °
        self.lon     = 0 # °
        
        self.rc_lat = 0 # Right Turn Circle lat °
        self.rc_lon = 0 # Right Turn Circle lon °
        self.lc_lat = 0 # Left Turn Circle lat °
        self.lc_lon = 0 # Left Turn Circle lon °
        self.c_lat  = 0 # Selected Turn Circle lat °
        self.c_lon  = 0 # Selected Turn Circle lon °
        self.e_lat  = 0 # Enter/exit lat °
        self.e_lon  = 0 # Enter/exit lon °


class orbit_dir(IntEnum):
    COUNTER_CLOCKWISE = 0
    CLOCKWISE         = 1


class dubin(IntEnum):
    LSRU = 0 # Left Straight Right Up
    LSRD = 1 # Left Straight Right Down
    RSLU = 2 # Right Straight Left Up
    RSLD = 3 # Right Straight Left Down
    RSRU = 4 # Right Straight Right Up
    RSRD = 5 # Right Straight Right Down
    LSLU = 6 # Left Straight Left Up
    LSLD = 7 # Left Straight Left Down


class dubin_mode(IntEnum):
    TURN_I     = 0 # Initial turn
    STRAIGHT   = 1 # Straight
    TURN_F     = 2 # Final turn
    DISENGAGED = 3 # Disengage dubin-styled navigation


class nav_frame(object):
    def __init__(self):
        self.path = dubin.LSRU # Dubin path type
        self.ni   = point()    # Current point
        self.nf   = point()    # Next point


class navigator(object):
    def process_frame(self, frame: nav_frame) -> nav_frame:
        self.findMTR(frame.ni)
        self.findMTR(frame.nf)
        
        self.findTurnCenters(frame.ni)
        self.findTurnCenters(frame.nf)
        
        self.findPath(frame)
        
        self.findEPts(frame)

    def findMTR(self, curPoint: point) -> float:
        curPoint.minTurnRad = (curPoint.speed * curPoint.speed) / (EARTH_GRAVITY * tan(radians(curPoint.maxRoll)))

    def findTurnCenters(self, curPoint: point) -> list:
        [curPoint.rc_lat, curPoint.rc_lon] = coord(curPoint.lat, curPoint.lon, curPoint.minTurnRad, (curPoint.heading + 90) % 360)
        [curPoint.lc_lat, curPoint.lc_lon] = coord(curPoint.lat, curPoint.lon, curPoint.minTurnRad, (curPoint.heading - 90) % 360)

    def findPath(self, frame: nav_frame) -> dubin:
        dist_ir = distance(frame.ni.rc_lat, frame.ni.rc_lon, frame.nf.lat, frame.nf.lon)
        dist_il = distance(frame.ni.lc_lat, frame.ni.lc_lon, frame.nf.lat, frame.nf.lon)

        if dist_ir <= dist_il:
            frame.ni.c_lat = frame.ni.rc_lat
            frame.ni.c_lon = frame.ni.rc_lon
        else:
            frame.ni.c_lat = frame.ni.lc_lat
            frame.ni.c_lon = frame.ni.lc_lon
            
        dist_fr = distance(frame.nf.rc_lat, frame.nf.rc_lon, frame.ni.lat, frame.ni.lon)
        dist_fl = distance(frame.nf.lc_lat, frame.nf.lc_lon, frame.ni.lat, frame.ni.lon)
    
        if dist_fr <= dist_fl:
            frame.nf.c_lat = frame.nf.rc_lat
            frame.nf.c_lon = frame.nf.rc_lon
        else:
            frame.nf.c_lat = frame.nf.lc_lat
            frame.nf.c_lon = frame.nf.lc_lon
    
        if dist_ir <= dist_il:
            if dist_fr <= dist_fl:
                if frame.nf.alt >= frame.ni.alt:
                    frame.path = dubin.RSRU
                else:
                    frame.path = dubin.RSRD
            else:
                if frame.nf.alt >= frame.ni.alt:
                    frame.path = dubin.RSLU
                else:
                    frame.path = dubin.RSLD
        else:
            if dist_fr <= dist_fl:
                if frame.nf.alt >= frame.ni.alt:
                    frame.path = dubin.LSRU
                else:
                    frame.path = dubin.LSRD
            else:
                if frame.nf.alt >= frame.ni.alt:
                    frame.path = dubin.LSLU
                else:
                    frame.path = dubin.LSLD

    def findEPts(self, frame: nav_frame) -> list:
        theta_cc = heading(frame.ni.c_lat, frame.ni.c_lon, frame.nf.c_lat, frame.nf.c_lon)
        stepSize = 0.001 # °
        distTol  = 1 # m
    
        if (frame.path == dubin.LSRU) or (frame.path == dubin.LSRD):
            theta_i = theta_cc
            theta_f = (theta_i + 180, 360)
    
            [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
            [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
            test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
            [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)
    
            dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
            while dist > distTol:
                theta_i = (theta_i + stepSize) % 360
                theta_f = (theta_i + 180) % 360

                [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)

                dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    		
            frame.ni.e_lat = p0_lat
            frame.ni.e_lon = p0_lon

            frame.nf.e_lat = p2_lat
            frame.nf.e_lon = p2_lon
    	
        elif (frame.path == dubin.RSLU) or (frame.path == dubin.RSLD):
            theta_i = theta_cc
            theta_f = (theta_i + 180) % 360

            [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
            [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

            test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
            [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)

            dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)

            while dist > distTol:
                theta_i = (theta_i - stepSize) % 360
                theta_f = (theta_i + 180) % 360

                [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)

                dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    		
            frame.ni.e_lat = p0_lat
            frame.ni.e_lon = p0_lon

            frame.nf.e_lat = p2_lat
            frame.nf.e_lon = p2_lon
    	
        elif (frame.path == dubin.RSRU) or (frame.path == dubin.RSRD):
            if frame.ni.minTurnRad == frame.nf.minTurnRad:
                [frame.ni.e_lat, frame.ni.e_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, (theta_cc - 90) % 360)
                [frame.nf.e_lat, frame.nf.e_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, (theta_cc - 90) % 360)
    		
            elif frame.ni.minTurnRad > frame.nf.minTurnRad:
                theta_i = (theta_cc - 90) % 360
                theta_f = theta_i

                [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)

                dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)

                while dist > distTol:
                    theta_i = (theta_i + stepSize) % 360
                    theta_f = theta_i

                    [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                    [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                    test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                    [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)

                    dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
                frame.ni.e_lat = p0_lat
                frame.ni.e_lon = p0_lon

                frame.nf.e_lat = p2_lat
                frame.nf.e_lon = p2_lon
    		
            else:
                theta_i = theta_cc
                theta_f = theta_i

                [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)

                dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)

                while dist > distTol:
                    theta_i = (theta_i - stepSize) % 360
                    theta_f = theta_i

                    [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                    [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                    test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                    [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)

                    dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    			
                frame.ni.e_lat = p0_lat
                frame.ni.e_lon = p0_lon

                frame.nf.e_lat = p2_lat
                frame.nf.e_lon = p2_lon
                
        elif (frame.path == dubin.LSLU) or (frame.path == dubin.LSLD):
            if frame.ni.minTurnRad == frame.nf.minTurnRad:
                [frame.ni.e_lat, frame.ni.e_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, (theta_cc + 90) % 360)
                [frame.nf.e_lat, frame.nf.e_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, (theta_cc + 90) % 360)
                
            elif frame.ni.minTurnRad > frame.nf.minTurnRad:
                theta_i = (theta_cc + 90) % 360
                theta_f = theta_i

                [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)

                dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)

                while dist > distTol:
                    theta_i = (theta_i - stepSize) % 360
                    theta_f = theta_i

                    [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                    [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                    test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                    [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)

                    dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    			
                frame.ni.e_lat = p0_lat
                frame.ni.e_lon = p0_lon

                frame.nf.e_lat = p2_lat
                frame.nf.e_lon = p2_lon
    		
            else:
                theta_i = (theta_cc + 90) % 360
                theta_f = theta_i

                [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)

                dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)

                while dist > distTol:
                    theta_i = (theta_i + stepSize) % 360
                    theta_f = theta_i

                    [p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
                    [p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)

                    test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
                    [p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)

                    dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
                frame.ni.e_lat = p0_lat
                frame.ni.e_lon = p0_lon
                
                frame.nf.e_lat = p2_lat
                frame.nf.e_lon = p2_lon
'''