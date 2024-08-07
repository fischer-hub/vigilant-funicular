import math, os, sys, yaml, datetime
from scipy.interpolate import CubicSpline
import pickle
import numpy as np
import requests


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
    #print('got: ', args[0], 'returning path : ', os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


#def scale_rect(rect, scale_factor):

def load_config():
     
    # running on windows
    if 'APPDATA' in os.environ:
        confighome = os.environ['APPDATA']
    # running on unix supporting XDG CONFIG
    elif 'XDG_CONFIG_HOME' in os.environ:
        confighome = os.environ['XDG_CONFIG_HOME']
    # just put it in home
    else:
        confighome = os.path.join(os.environ['HOME'], '.config')
    
    configfile = os.path.join(confighome, 'vigilant', 'config.yaml')

    if os.path.isfile(configfile):
        with open(configfile, 'r') as file:
            config = yaml.safe_load(file)
        
        if not config:
             print("Found config file but the file is empty: ", configfile)
             config = {'no_config': True}
        else:
             # select latest save for now
             print("Loaded config file: ", configfile)
             config['no_config'] = False

        config['savegame'] = {}
        return config
        
    else:
        os.makedirs(os.path.dirname(configfile), exist_ok=True)
        with open(configfile, 'w'): pass

        return {}


def save_config(config):

    if not config:
         config = {}

    if 'savegame' not in config: 
         config['savegame'] = ''

    savegame = config.pop('savegame')

    # running on windows
    if 'APPDATA' in os.environ:
        confighome = os.environ['APPDATA']
    # running on unix supporting XDG CONFIG
    elif 'XDG_CONFIG_HOME' in os.environ:
        confighome = os.environ['XDG_CONFIG_HOME']
    # just put it in home
    else:
        confighome = os.path.join(os.environ['HOME'], '.config')
    
    configfile = os.path.join(confighome, 'vigilant', 'config.yaml')
    savefile = os.path.join(confighome, 'vigilant', f"{str(datetime.datetime.now()).replace(' ', '_')}.slay")

    with open(configfile, 'w') as file:
        yaml.dump(config, file)

    with open(savefile, 'w') as file:
        yaml.dump(savegame, file)

    print('saved config to file: ', configfile)
    print('saved savegame to file: ', savefile)


def check_update(current_version):
    '''Returns true when the latest remote version is different from the current one. Else returns false, also returns false when remote is not reachable.'''
    try:
        response = requests.get("https://api.github.com/repos/fischer-hub/vigilant-funicular/releases/latest").json()
        print(response["name"], current_version)
    except:
         print('Failed to check remote version, probs connection issue, got response: ', response)
         return False
    return response["name"] != current_version
         

def get_savegames():
     
    savegames = []

    # running on windows
    if 'APPDATA' in os.environ:
        confighome = os.environ['APPDATA']
    # running on unix supporting XDG CONFIG
    elif 'XDG_CONFIG_HOME' in os.environ:
        confighome = os.environ['XDG_CONFIG_HOME']
    # just put it in home
    else:
        confighome = os.path.join(os.environ['HOME'], '.config', 'vigilant')

    for file in os.listdir(confighome):
        if file.endswith(".slay"):
            savegames.append(file)
        
    return savegames