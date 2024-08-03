from src.scene import Scene, Clickable, ChangeScene, Commentable
import pygame as pg
from lib.helper import path
from src.animate import StripAnimate


class SizeMeter(Clickable):
    '''A class implementing a clickable object that triggers the main player talk function, given a sound (comment) to play at the same time.'''
    def __init__(self, rect, scene, idx, animation = None, hover_cursor = 0, sound_lst=None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.scene = scene
        self.idx = idx
    
    def on_click(self):
        self.scene.fg_lst['size_meter'].index = self.idx
        return None
    

class Btn(Clickable):
    def __init__(self, rect, animation = None, sound = None, hover_cursor = 0):
        super().__init__(rect, animation, hover_cursor, sound)
        self.sound = sound

    def on_click(self):
        self.animation.pause = False
        sound = pg.mixer.Sound(path(self.sound))
        sound.play()


class StartScreen(Scene):
    def __init__(self, player, cursor, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, collision_file, scale_factor, dev)
        self.id = 3

        self.player_spawn = (-100, -100)
        

        # sprites
        bg = StripAnimate('scenes/start_screen/bg.png', img_width = 320, frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        start_button = StripAnimate('scenes/start_screen/start_button.png', img_width = 320, frame_rate = 3, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        update_button = StripAnimate('scenes/start_screen/update_button.png', img_width = 320, frame_rate = 3, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        new_game = StripAnimate('scenes/start_screen/new_game.png', img_width = 320, frame_rate = 3, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        size_meter = StripAnimate('scenes/start_screen/size_meter.png', img_width = 320, frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 1, pause = True, once = True)
        caution_msg = StripAnimate('scenes/start_screen/caution_message.png', img_width = 320, frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)


        # clickables
        start_button_clickable = Btn(pg.Rect(460, 120, 1050, 220), sound = path('sounds', 'button_click.ogg'), animation = start_button)
        new_game_button_clickable = Btn(pg.Rect((460, 440, 1050, 220)), sound = path('sounds', 'button_click.ogg'), animation = new_game)
        update_button_clickable = Btn(pg.Rect((460, 770, 1050, 220)), sound = path('sounds', 'button_click.ogg'), animation = update_button)

        self.clickable_lst = { '1': SizeMeter(pg.Rect(1670, 290, 90, 65), self, 1), '2': SizeMeter(pg.Rect(1670, 395, 90, 65), self, 2), '3': SizeMeter(pg.Rect(1670, 495, 90, 65), self, 3),
                               '4': SizeMeter(pg.Rect(1670, 610, 90, 65), self, 4), '5': SizeMeter(pg.Rect(1675, 730, 90, 70), self, 5), '6': SizeMeter(pg.Rect(1680, 840, 90, 70), self, 6),
                               }

        self.bg_lst = {}
        self.fg_lst = {'bg': bg, 'start_button': start_button, 'update_button': update_button, 'size_meter': size_meter,
                       'new_game': new_game}
        
        self.clickable_lst.update({'start_button': start_button_clickable, 'update_button_clickable': update_button_clickable, 'new_game_button_clickable': new_game_button_clickable})
