from src.scene import Scene, Clickable, ChangeScene
import pygame as pg
import os

class GreySlot(Clickable):
    def __init__(self, rect, player, sound, animation=None, hover_cursor = 2):
        super().__init__(rect, animation, hover_cursor, sound)
        self.player = player

    def on_click(self):

        self.player.talk(self.sound)


class Scene1(Scene):
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, background_lst, foreground_lst, collision_file, scale_factor, dev)
        
        #greslot = GreySlot(pg.Rect((1200, 620, 130, 52)), self.player, os.path.join('sounds', 'characters', 'dr', 'test.ogg'))
        greslot = GreySlot(pg.Rect((1200, 620, 130, 52)), self.player, os.path.join('sounds', 'test.ogg'))
        self.clickable_lst = [ChangeScene(pg.Rect(40, 35, 250, 400), 1, hover_cursor = 3), greslot]
