from src.scene import Scene, Clickable, ChangeScene, Commentable
import pygame as pg
from lib.helper import path
from src.animate import StripAnimate


class Bathroom(Scene):
    def __init__(self, player, cursor, collision_file = None, scale_factor=6, dev=False):
        super().__init__(player, cursor, collision_file, scale_factor, dev)
        self.id = 2


        # sprites
        #rohrzange = StripAnimate('scenes/elevator/rohrzange.png', img_width = 32, frame_rate = 1, scale_factor = scale_factor, pos = (1081, 687))
        
        #clickables
        #rohrzange_clickable = Collectable(pg.Rect(1131, 717, 20* self.scale_factor, 20*self.scale_factor), self.player, sound_lst = ['sounds/characters/dr/eine_rohrzange.ogg'], scene = self, list_name = 'rohrzange', item_id_lst = ['Rohrzange'])

        self.bg_lst = {'bg': 'scenes/bathroom/bg.png', 'pipes': 'scenes/bathroom/pipes.png', 'pipe_shadow': 'scenes/bathroom/pipe_shadow.png',
                       'valve': 'scenes/bathroom/valve.png'}

        self.bg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.bg_lst.items()}
        self.fg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.fg_lst.items()}

