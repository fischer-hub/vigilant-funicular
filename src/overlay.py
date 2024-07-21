from src.scene import Scene, Clickable
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


        menu = Menu(pg.Rect((1549, 925, 318, 118)), self.player, self.bg_lst[1], sound = os.path.join('sounds', 'button_click.ogg'))

        self.clickable_lst = [menu]
