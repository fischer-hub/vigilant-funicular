import math
from scipy.interpolate import CubicSpline
import pickle
import numpy as np

dev = False

def set_dev(mode):
    global dev
    dev = mode

def sign(x):
    return (x > 0) - (x < 0)


def record_collision_points(p1, p2, scale_factor, screen, fn):
                    
                    cs = CubicSpline(p1, p2)
                    x_fit = [math.ceil(x) for x in np.linspace(0, 320 *scale_factor, 320 *scale_factor)]
                    y_fit = [math.ceil(x) for x in cs(x_fit)]
                    
                    print('recorded data points: ', p1, p2)

                    for x, y in zip(x_fit, y_fit):
                        screen.set_at((x, y), "red")
                        
                    with open((fn), "wb") as fp:
                        pickle.dump(y_fit, fp)
                        print('saved collision y coords to: ', fn)