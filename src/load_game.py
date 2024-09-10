import pygame as pg
from src.scene import Scene, Clickable, Btn
from lib.helper import path, get_savegames, load_savegame
from src.animate import StripAnimate
from src.text import Text
import yaml


class InventorySlot(Clickable):
    def __init__(self, rect, cursor, inventory_idx, player, scale_factor, scene, animation = None, sound = None, hover_cursor = 0):
        super().__init__(rect, animation, hover_cursor, sound)
        self.sound = sound
        self.scene = scene
        self.cursor = cursor
        self.player = player
        self.inventory_idx = inventory_idx
        self.scale_factor = scale_factor

    def on_click(self):
        if len(self.scene.savegame_lst) >= self.inventory_idx:
            self.player.config['savegame'] = load_savegame(self.scene.savegame_lst[self.inventory_idx])
            print('loaded savefile: ', self.player.config['savegame']['savefile'])
            self.player.load()
            return (self.player.config['savegame']['scene'], self.player.destination_pos)
            
        else:
            print('There is no savegame in this slot you brat')



class LoadGame(Scene):
    def __init__(self, player, cursor, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, collision_file, scale_factor, dev)
        self.id = 4
        self.scale_factor = scale_factor
        self.inventory_slot_coord_lst = [(318, 234), (638, 237), (925, 246), (1235, 241), (1542, 250), (329, 467), (646, 474), 
                                         (945, 481), (1240, 482), (1560, 485), (308, 745), (618, 754), (960, 753), (1258, 741), (1579, 744)]

        #self.inventory_slot_coord_lst = [ tuple(int(value * (self.scale_factor / 6)) for value in coord) for coord in self.inventory_slot_coord_lst ]
        
        self.inventory_clickable_rects_lst = [ pg.Rect(210, 160, 250, 150), pg.Rect(510, 160, 270, 165), pg.Rect(810, 160, 250, 165),
                                               pg.Rect(1110, 160, 260, 175), pg.Rect(1410, 160, 270, 175), pg.Rect(200, 360, 270, 210),
                                               pg.Rect(520, 370, 270, 210), pg.Rect(820, 390, 270, 200), pg.Rect(1120, 390, 260, 200),
                                               pg.Rect(1430, 390, 280, 200), pg.Rect(180, 640, 280, 190), pg.Rect(480, 660, 280, 200),
                                               pg.Rect(820, 660, 280, 200), pg.Rect(1145, 660, 250, 200), pg.Rect(1445, 650, 270, 220) ]
        
        
        self.inventory_clickable_rects_lst = { idx: InventorySlot(rect, self.cursor, idx, self.player, self.scale_factor, self) for idx, rect in enumerate(self.inventory_clickable_rects_lst) }

        self.inventory_slot_coord_lst_adjusted = [ (pos[0] - (17 * self.scale_factor), pos[1] - (13 * self.scale_factor)) for pos in self.inventory_slot_coord_lst ]

        self.savegame_lst = get_savegames()

        # sprites
        bg = StripAnimate('scenes/start_screen/bg.png', img_width = 320, frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        inventory = StripAnimate('sprites/inventory.png', img_width = 320, frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0)
        menu_btn = StripAnimate('sprites/menu_btn.png', img_width = 320, frame_rate = 3, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        back_btn = StripAnimate('sprites/back_btn.png', img_width = 320, frame_rate = 3, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        
        back_btn_cl = Btn(pg.Rect((17, 30, 300, 105)), sound = path('sounds', 'button_click.ogg'), animation = back_btn, fct = lambda: (3,(0,0)), scene = self, id = 'back_btn')


        self.bg_lst = {}
        self.fg_lst = {'bg': bg, 'inventory': inventory, 'menu_btn': menu_btn, 'back_btn': back_btn}


        self.clickable_lst.update(self.inventory_clickable_rects_lst)
        self.clickable_lst.update({'back_btn': back_btn_cl})


        self.bg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key,layer in self.bg_lst.items()}
        self.fg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key,layer in self.fg_lst.items()}


    def draw_fg(self, surface):
        
        render_lst = [Text(f"{savegame.split('_')[0]}", pg.Rect(pos[0], pos[1], 0, 0), 3, (255,255,255), self.scale_factor) for savegame, pos in zip(self.savegame_lst, self.inventory_slot_coord_lst_adjusted)]
        render_lst += [Text(f"{savegame.split('_')[1].split('.')[0]}", pg.Rect(pos[0], pos[1] + (13*self.scale_factor), 0, 0), 3, (255,255,255), self.scale_factor) for savegame, pos in zip(self.savegame_lst, self.inventory_slot_coord_lst_adjusted)]

        for layer in self.fg_lst.values():
            if type(layer) is StripAnimate or type(layer) is Text:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))

        for layer in render_lst:
            if type(layer) is StripAnimate or type(layer) is Text:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))