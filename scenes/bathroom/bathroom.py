from src.scene import Scene, Clickable, ChangeScene, Commentable
import pygame as pg
from lib.helper import path
from src.animate import StripAnimate


class Valve(Clickable):
    def __init__(self, rect, player, animation=None, hover_cursor = 1, sound_lst=None, scene = None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.player = player
        self.sound_lst = sound_lst
        self.scene = scene
    
    def on_click(self):
        self.player.move_to(pg.mouse.get_pos(), self.on_arrive)

    def on_arrive(self):

        if 'Rohrzange' in self.player.inventory:
            self.player.stretch()
            sound = pg.mixer.Sound(path(self.sound_lst[1]))
            sound.set_volume(0.8)
            sound.play(maxtime = 1100)
            sound.fadeout(1100)
            self.scene.bg_lst['valve'].pause = False
            self.scene.bg_lst['valve'].default_frame = 4
            self.player.inventory.pop('Rohrzange')
            self.scene.config['savegame']['bathroom']['valve'] = True
        else:
            self.player.talk(self.sound_lst[0])

        return None
    

class Bathroom(Scene):
    def __init__(self, player, cursor, collision_file = None, scale_factor=6, dev=False, config = None):
        super().__init__(player, cursor, collision_file, scale_factor, dev, config)


        # sprites
        #rohrzange = StripAnimate('scenes/elevator/rohrzange.png', img_width = 32, frame_rate = 1, scale_factor = scale_factor, pos = (1081, 687))
        dripping_pipe = StripAnimate('scenes/bathroom/dripping_pipe.png', img_width = 320, frame_rate = 9, scale_factor = scale_factor)
        valve = StripAnimate('scenes/bathroom/valve.png', img_width = 320, frame_rate = 4, scale_factor = scale_factor, pause = True, once = True, cycles=1, default_frame = 4 if self.config['savegame']['bathroom']['valve'] else 0)
        

        
        #clickables        
        valve_clb = Valve(pg.Rect(899, 270, 320, 310), self.player, sound_lst = ['sounds/characters/dr/das_klemmt.ogg', 'sounds/valve.ogg'], scene = self)
        dripping_pipe_clb = Commentable(pg.Rect(3, 129, 370, 400), self.player, sound_lst = 'sounds/characters/dr/wasser_abgestellt.ogg')
        ladder_clb = Commentable(pg.Rect(1550, 0, 200, 390), self.player, sound_lst = 'sounds/characters/dr/wo_die_leiter.ogg')
        

        self.bg_lst = {'bg': 'scenes/bathroom/bg.png', 'pipes': 'scenes/bathroom/pipes.png', 'pipe_shadow': 'scenes/bathroom/pipe_shadow.png',
                       'valve': valve, 'dripping_pipe': dripping_pipe}

        self.bg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.bg_lst.items()}
        self.fg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.fg_lst.items()}

        self.clickable_lst = {'right_change_scene': ChangeScene(pg.Rect(1849, 128, 100, 900), 1, hover_cursor = 4), 'valve': valve_clb, 'dripping_pipe': dripping_pipe_clb,
                              'ladder': ladder_clb}