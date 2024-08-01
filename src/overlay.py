from src.scene import Scene, Clickable
from src.animate import StripAnimate
import pygame as pg
from lib.helper import path

class Menu(Clickable):
    def __init__(self, rect, player, animation, sound = None, hover_cursor = 0):
        super().__init__(rect, animation, hover_cursor, sound)
        self.player = player
        self.sound = sound

    def on_click(self):
        self.animation.pause = False
        sound = pg.mixer.Sound(path(self.sound))
        sound.play()
        

class InventorySlot(Clickable):
    def __init__(self, rect, cursor, inventory_idx, player, animation = None, sound = None, hover_cursor = 0):
        super().__init__(rect, animation, hover_cursor, sound)
        self.sound = sound
        self.cursor = cursor
        self.player = player
        self.inventory_idx = inventory_idx

    def on_click(self):
        if len(self.player.inventory) > self.inventory_idx:
            self.cursor.cursor_img = StripAnimate(f"sprites/items/{self.player.inventory[self.inventory_idx]}.png", 32)
            self.cursor.item = self.player.inventory[self.inventory_idx]


class Overlay(Scene):
    def __init__(self, player, cursor, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, collision_file, scale_factor, dev)
        self.hide = True
        self.inventory_slot_coord_lst = [(318, 234), (638, 237), (925, 246), (1235, 241), (1542, 250), (329, 467), (646, 474), 
                                         (945, 481), (1240, 482), (1560, 485), (308, 745), (618, 754), (960, 753), (1258, 741), (1579, 744)]
        
        self.inventory_clickable_rects_lst = [ pg.Rect(210, 160, 250, 150), pg.Rect(510, 160, 270, 165), pg.Rect(810, 160, 250, 165),
                                               pg.Rect(1110, 160, 260, 175), pg.Rect(1410, 160, 270, 175), pg.Rect(200, 360, 270, 210),
                                               pg.Rect(520, 370, 270, 210), pg.Rect(820, 390, 270, 200), pg.Rect(1120, 390, 260, 200),
                                               pg.Rect(1430, 390, 280, 200), pg.Rect(180, 640, 280, 190), pg.Rect(480, 660, 280, 200),
                                               pg.Rect(820, 660, 280, 200), pg.Rect(1145, 660, 250, 200), pg.Rect(1445, 650, 270, 220) ]
        
        self.inventory_clickable_rects_lst = { idx: InventorySlot(rect, self.cursor, idx, self.player) for idx, rect in enumerate(self.inventory_clickable_rects_lst) }

        self.inventory_slot_coord_lst_adjusted = [ (pos[0] - (16 * self.scale_factor), pos[1] - (16 * self.scale_factor)) for pos in self.inventory_slot_coord_lst ]


    
        inventory = StripAnimate('sprites/inventory.png', img_width = 320, frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0)
        menu_buttons = StripAnimate('sprites/menu_buttons-sheet.png', img_width = 320, frame_rate = 3, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)

        self.bg_lst = {'inventory': inventory, 'menu_buttons': menu_buttons}
        self.fg_lst = {}


        menu = Menu(pg.Rect((1549, 925, 318, 118)), self.player, menu_buttons, sound = path('sounds', 'button_click.ogg'))
        self.clickable_lst = {'menu': menu}
        self.clickable_lst.update(self.inventory_clickable_rects_lst)


        self.bg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key,layer in self.bg_lst.items()}
        self.fg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key,layer in self.fg_lst.items()}


    def draw_bg(self, surface):
        
        inventory_sprites = [path('sprites', 'items', f"{item}.png") for item in self.player.inventory]
        render_lst = [StripAnimate(layer, 32, self.scale_factor, pos = pos) for layer, pos in zip(inventory_sprites, self.inventory_slot_coord_lst_adjusted)]

        for layer in self.bg_lst.values():
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))

        for layer in render_lst:
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))