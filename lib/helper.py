import math, os, sys, yaml, datetime, urllib.request, platform
from scipy.interpolate import CubicSpline
import pickle
import numpy as np
import requests, shutil
import pygame as pg


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
            if ' ' in file:
                print('Invalid filename, contains whitespace in datetime string, deleting.')
                os.remove(file)
            else:
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

    savegame = config['savegame']
    confighome = get_config_home()
    
    configfile = os.path.join(confighome, 'config.yaml')
    new_savefile = os.path.join(confighome, f"{str(datetime.datetime.now()).replace(' ', '_').replace(':', 'colon')}.slay")
    savefile = savegame['savefile'] if 'savefile' in savegame else new_savefile

    with open(configfile, 'w') as file:
        yaml.dump(config, file)

    with open(savefile, 'w') as file:
        yaml.dump(savegame, file)

    if savefile != new_savefile: os.replace(savefile, new_savefile)

    print('saved config to file: ', configfile)
    print('saved savegame to file: ', new_savefile)


def init_save_obj():
     savegame = {'scene1': {'red': False},
                 'bathroom': {'valve': False},
                 'inventory': []}
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
    #if len(sys.argv) > 1 and not 'log' in sys.argv:
    #    sys.stderr = open(os.path.join(confighome, 'log_err.txt'), 'w')
    #    sys.stdout = open(os.path.join(confighome, 'log_out.txt'), 'w')

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

    """    savegames = get_savegames()
    
    if savegames:
        dates = [ datetime.datetime.fromisoformat(file.split(os.path.sep)[-1].replace('.slay', '').replace('_',':').replace('colon', ':')) for file in savegames ]
        max_idx = dates.index(max(dates))

        if os.path.isfile(os.path.join(confighome, savegames[max_idx])):
            with open(os.path.join(confighome, savegames[max_idx]), 'r') as file:
                config['savegame'] = yaml.safe_load(file)
            print('Loaded savefile: ', os.path.join(confighome, savegames[max_idx]))
        else:
            print('Savefile not found: ', os.path.join(confighome, savegames[max_idx]))
            config['savegame'] = init_save_obj()

    else:     
        print('No savefiles found in: ', confighome) """
    
    if any("slay" in arg for arg in sys.argv):
        config['savegame'] = merge_dicts(load_savegame([x for x in sys.argv if 'slay' in x][0]), init_save_obj())
    else:
        # new game case
        config['savegame'] = init_save_obj()

    return config
    

def check_update(current_version):
    '''Returns true when the latest remote version is different from the current one. Else returns false, also returns false when remote is not reachable.'''
    try:
        print('Checking repository for updates..')
        response = requests.get("https://api.github.com/repos/fischer-hub/vigilant-funicular/releases/latest").json()
        print(f"Latest version is: {response['name']}, current version is: {current_version}")
    except Exception as e:
         print('Failed to check remote version, probs connection issue: ', e)
         return False
    return response["name"] != current_version


def merge_dicts(a: dict, b: dict, path=[], level=1):
    print(f"Merging savegame template with loaded savegame on recursion level {level}:")
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], path + [str(key)], level=level+1)
            elif a[key] != b[key]:
                print(f"Key '{key}' exists in both savegames but has different values. Keeping value of loaded savegame: '{a[key]}', template savegame '{b[key]}'")
        else:
            print(f"Savegame key '{key}' not found in loaded savegame, defaulting to template value {b[key]}.")
            a[key] = b[key]
    return a


def update_game():
    osname = platform.system()

    if 'Linux' in osname:
        osname = 'ubuntu'
        executablename = 'vigilant'
    elif 'Darwin' in osname:
        executablename = 'vigilant'
        osname = 'macos'
    elif 'Windows' in osname:
        osname = 'windows'
        executablename = 'vigilant.exe'
    else:
        print(f"Failed to update game executable. Could not detect operating system since platform.system returns unknown value: {osname}.")
        return
    
    try:
        urllib.request.urlretrieve(f"https://github.com/fischer-hub/vigilant-funicular/releases/latest/download/vigilant-{osname}-latest", "vigilant_update")
    except Exception as e:
        print(f"Failed to update game executable, download returned: {e}\nFrom url: https://github.com/fischer-hub/vigilant-funicular/releases/latest/download/vigilant-{osname}-latest")
        return
    
    if os.path.isfile(executablename):
        os.remove(executablename)
        shutil.move('vigilant_update', executablename)
    else:
        print(f"Could not remove old executable file because it does not exist: {executablename}.")
        return

    if getattr(sys, 'frozen', False):
                print(f"Restarting game in frozen mode to apply executable update..")
                pg.quit()
                os.system(sys.executable)
                sys.exit()

    else:
        print(f"Updating of the executable is only supported for the bundled version. You see to run the  script version. Please pull the update from the repository.")
        # maybe put this as a warn message on screen
        #os.execv(sys.executable, ['python'] + sys.argv + [self.scene.savegame_lst[self.inventory_idx]])            