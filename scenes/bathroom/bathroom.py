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
        if self.scene.config['savegame']['bathroom']['valve']:
            self.scene.bg_lst.pop('valve')
            self.scene.bg_lst['valve_falling'] = self.animation
            self.scene.bg_lst['valve_falling'].pause = False
            self.scene.bg_lst['valve_falling'].default_frame = 3

        else:

            if 'Rohrzange' in self.scene.cursor.item:
            #if True:
                self.player.stretch()
                sound = pg.mixer.Sound(path(self.sound_lst[1]))
                sound.set_volume(0.8)
                sound.play(maxtime = 1100)
                sound.fadeout(1100)
                self.scene.bg_lst['valve'].pause = False
                self.scene.bg_lst['valve'].default_frame = 4
                #self.player.inventory.remove('Rohrzange')
                self.scene.config['savegame']['bathroom']['valve'] = True
                self.scene.cursor.item = ''
            else:
                self.player.stretch()
                self.player.talk(self.sound_lst[0])

        return None
    

class Bathroom(Scene):
    def __init__(self, player, cursor, collision_file = None, scale_factor=6, dev=False, config = None):
        self.id = 2
        super().__init__(player, cursor, collision_file, scale_factor, dev, config)


        # sprites
        #rohrzange = StripAnimate('scenes/elevator/rohrzange.png', img_width = 32, frame_rate = 1, scale_factor = scale_factor, pos = (1081, 687))
        dripping_pipe = StripAnimate('scenes/bathroom/dripping_pipe.png', img_width = 320, frame_rate = 9, scale_factor = scale_factor)
        valve = StripAnimate('scenes/bathroom/valve.png', img_width = 320, frame_rate = 4, scale_factor = scale_factor, pause = True, once = True, cycles=1, default_frame = 4 if self.config['savegame']['bathroom']['valve'] else 0)
        valve_falling = StripAnimate('scenes/bathroom/valve_falling.png', img_width = 320, frame_rate = 8, scale_factor = scale_factor, pause = True, once = True, cycles=1)
        spider = StripAnimate('scenes/bathroom/spider.png', img_width = 320, frame_rate = 12, scale_factor = scale_factor, pause = True, once = True, cycles=1)
        

        
        #clickables        
        valve_clb = Valve(pg.Rect(899, 270, 320, 310), self.player, sound_lst = ['sounds/characters/dr/das_klemmt.ogg', 'sounds/valve.ogg'], scene = self, animation = valve_falling)
        dripping_pipe_clb = Commentable(pg.Rect(3, 129, 370, 400), self.player, sound_lst = 'sounds/characters/dr/wasser_abgestellt.ogg')
        ladder_clb = Commentable(pg.Rect(1550, 0, 200, 390), self.player, sound_lst = 'sounds/characters/dr/wo_die_leiter.ogg')
        spider_clb = Clickable(pg.Rect((690, 390, 30, 30)), hover_cursor = 1, animation = spider)

        self.bg_lst = {'bg': 'scenes/bathroom/bg.png', 'pipes': 'scenes/bathroom/pipes.png', 'pipe_shadow': 'scenes/bathroom/pipe_shadow.png',
                       'valve': valve, 'dripping_pipe': dripping_pipe, 'spider': spider}

        self.bg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.bg_lst.items()}
        self.fg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.fg_lst.items()}

        self.clickable_lst = {'right_change_scene': ChangeScene(pg.Rect(1849, 128, 100, 900), 1, hover_cursor = 4), 'valve': valve_clb, 'dripping_pipe': dripping_pipe_clb,
                              'ladder': ladder_clb, 'spider': spider_clb}