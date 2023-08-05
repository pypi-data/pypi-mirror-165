import numpy as np
from numpy import pi


def wrapToPi(e):
    return (e + pi) % (2 * pi) - pi

def constrain(input, min, max):
    if type(input) is np.ndarray:
        input[input < min] = min
        input[input > max] = max
        
        return input
    
    else:
        if input < min:
            return min
        elif input > max:
            return max
        return input

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min