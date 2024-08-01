import math, os, sys
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


def path(*args):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    if len(args) == 1:
        if '/tmp/' not in args[0]:
            relative_path = os.path.join(*args[0].split('/'))
        else:
            # we probably mistakenly called path on a path object
            return args[0]
    else:
        relative_path = os.path.join(*args)
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = ''
    print('got: ', args[0], 'returning path : ', os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)