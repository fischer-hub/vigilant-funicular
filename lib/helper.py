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


def get_config_home():
     
    # running on windows
    if 'APPDATA' in os.environ:
        confighome = os.environ['APPDATA']
    # running on unix supporting XDG CONFIG
    elif 'XDG_CONFIG_HOME' in os.environ:
        confighome = os.environ['XDG_CONFIG_HOME']
    # just put it in home
    else:
        confighome = os.path.join(os.environ['HOME'], '.config', 'vigilant')
    
    return confighome


def get_savegames():
    '''Returns the list of save game files found in the config directory'''
    savegames = []

    confighome = get_config_home()

    for file in os.listdir(confighome):
        if file.endswith(".slay"):
            savegames.append(file)
        
    return savegames


def load_savegame(savegame):
    
    confighome = get_config_home()

    with open(os.path.join(confighome, savegame), 'r') as file:
        save_dict = yaml.safe_load(file)
    
    print("Loaded savefile: ", os.path.join(confighome, savegame))
    save_dict['savefile'] = os.path.join(confighome, savegame)
    return save_dict


def save_config(config):

    if not config:
         config = {}

    if 'savegame' not in config: 
         config['savegame'] = ''

    savegame = config.pop('savegame')
    confighome = get_config_home()
    
    configfile = os.path.join(confighome, 'config.yaml')
    new_savefile = os.path.join(confighome, f"{str(datetime.datetime.now()).replace(' ', '_').replace(':', '_')}.slay")
    savefile = savegame['savefile'] if 'savefile' in savegame else new_savefile

    with open(configfile, 'w') as file:
        yaml.dump(config, file)

    with open(savefile, 'w') as file:
        yaml.dump(savegame, file)

    if savefile != new_savefile: os.replace(savefile, new_savefile)

    print('saved config to file: ', configfile)
    print('saved savegame to file: ', new_savefile)


def init_save_obj():
     savegame = {'scene1': {'red': False}}
     print('Initializing savegame object.')
     return savegame


def load_config():

     
    confighome = get_config_home()
    
    configfile = os.path.join(confighome, 'config.yaml')
    
    #stdout = sys.stdout

    #with open(os.path.join(confighome, 'log.txt'), 'w') as sys.stdout:
    #    print('Redirecting stdout to: ')#, os.path.join(confighome, 'log.txt'))

    #with open(os.path.join(confighome, 'log_err.txt'), 'w') as sys.stderr:
    #    print('Redirecting stderr to: ')#, os.path.join(confighome, 'log.txt'))
    sys.stderr = open(os.path.join(confighome, 'log_err.txt'), 'w')
    sys.stdout = open(os.path.join(confighome, 'log_out.txt'), 'w')

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

        
    else:
        configfile = os.path.join('lib', 'config.yaml')
        print('Configfile not found, loading default from: ', configfile)
        
        with open(path(configfile), 'r') as file:
            config = yaml.safe_load(file)
        
        #save_config(config)
        config['no_config'] = True

    savegames = get_savegames()
    
    if savegames:
        dates = [ datetime.datetime.fromisoformat(file.split(os.path.sep)[-1].replace('.slay', '').replace('_',' ')) for file in savegames ]
        max_idx = dates.index(max(dates))

        if os.path.isfile(os.path.join(confighome, savegames[max_idx])):
            with open(os.path.join(confighome, savegames[max_idx]), 'r') as file:
                config['savegame'] = yaml.safe_load(file)
            print('Loaded savefile: ', os.path.join(confighome, savegames[max_idx]))
        else:
            print('Savefile not found: ', os.path.join(confighome, savegames[max_idx]))
            config['savegame'] = init_save_obj()

    else:     
        print('No savefiles found in: ', confighome)
        config['savegame'] = init_save_obj()

    return config
    


def check_update(current_version):
    '''Returns true when the latest remote version is different from the current one. Else returns false, also returns false when remote is not reachable.'''
    try:
        response = requests.get("https://api.github.com/repos/fischer-hub/vigilant-funicular/releases/latest").json()
        print(response["name"], current_version)
    except Exception as e:
         print('Failed to check remote version, probs connection issue: ', e)
         return False
    return response["name"] != current_version
         