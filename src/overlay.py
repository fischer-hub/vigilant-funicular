from src.scene import Scene, Clickable
from src.animate import StripAnimate
import pygame as pg
import os


class Menu(Clickable):
    def __init__(self, rect, player, animation, sound = None, hover_cursor = 0):
        super().__init__(rect, animation, hover_cursor, sound)
        self.player = player
        self.sound = sound

    def on_click(self):
        self.animation.pause = False
        sound = pg.mixer.Sound(self.sound)
        sound.play()
        

class Overlay(Scene):
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, background_lst, foreground_lst, collision_file, scale_factor, dev)
        self.hide = True
        self.inventory_slot_coord_lst = [(318, 234), (638, 237), (925, 246), (1235, 241), (1542, 250), (329, 467), (646, 474), 
                                         (945, 481), (1240, 482), (1560, 485), (308, 745), (618, 754), (960, 753), (1258, 741), (1579, 744)]
        
        self.inventory_slot_coord_lst_adjusted = [ (pos[0] - (16 * self.scale_factor), pos[1] - (16 * self.scale_factor)) for pos in self.inventory_slot_coord_lst ]


        menu = Menu(pg.Rect((1549, 925, 318, 118)), self.player, self.bg_lst[1], sound = os.path.join('sounds', 'button_click.ogg'))

        self.clickable_lst = [menu]

    def draw_bg(self, surface):
        
        inventory_sprites = [os.path.join('sprites', 'items', f"{item}.png") for item in self.player.inventory]
        render_lst = self.bg_lst + [ StripAnimate(layer, 32, self.scale_factor, pos = pos) for layer, pos in zip(inventory_sprites, self.inventory_slot_coord_lst_adjusted)]

        for layer in render_lst:
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))