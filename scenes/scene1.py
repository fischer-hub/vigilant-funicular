from src.scene import Scene, Clickable, ChangeScene
import pygame as pg
import os

class GreySlot(Clickable):
    def __init__(self, rect, player, sound, animation=None, hover_cursor = 2):
        super().__init__(rect, animation, hover_cursor, sound)
        self.player = player

    def on_click(self):

        self.player.talk(self.sound)


class GreenSlot(Clickable):
    def __init__(self, rect, player, sound, scene, animation=None, hover_cursor = 1):
        super().__init__(rect, animation, hover_cursor, sound)
        self.player = player
        self.scene = scene
        self.red = False
    
    def turn_red(self):
        self.player.crouch()
        self.red = True
        green_slot_img = self.scene.bg_lst[1]
        self.scene.bg_lst[1] = self.scene.bg_lst[0]
        self.scene.bg_lst[0] = green_slot_img

    def on_click(self):
        if not self.red:
            self.player.talk(self.sound)
            self.player.move_to(pg.mouse.get_pos(), self.turn_red)
        else:
            print('das sieht nicht richtig aus')

class Scene1(Scene):
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, background_lst, foreground_lst, collision_file, scale_factor, dev)
        
        redslot = GreySlot(pg.Rect((1500, 625, 130, 52)), self.player, os.path.join('sounds', 'characters', 'dr', 'das_sieht_nicht_richtig.ogg'))
        greenslot = GreenSlot(pg.Rect((908, 615, 110, 42)), self.player, os.path.join('sounds', 'characters', 'dr', 'das_koennte_spaeter.ogg'), self)
        greyslot = GreySlot(pg.Rect((1200, 620, 130, 52)), self.player, os.path.join('sounds', 'characters', 'dr', 'sieht_aus_als.ogg'))
        self.clickable_lst = [ChangeScene(pg.Rect(40, 35, 250, 400), 1, hover_cursor = 3), greyslot, greenslot, redslot]
