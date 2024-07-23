from src.scene import Scene, Clickable, ChangeScene
import pygame as pg
import os


class Commentable(Clickable):
    def __init__(self, rect, player, animation=None, hover_cursor = 2, sound=None):
        super().__init__(rect, animation, hover_cursor, sound)
        self.player = player
    
    def on_click(self):
        self.player.talk(self.sound)
        return None

class MidWindow(Clickable):
    def __init__(self, rect, animation=None, hover_cursor = 1, sound=None):
        super().__init__(rect, animation, hover_cursor, sound)
    
    def on_click(self):
        if self.animation.pause:
            self.animation.pause = False
            sound = pg.mixer.Sound(self.sound)
            sound.set_volume(0.2)
            sound.play()

        return 42
    
class GreySlot(Clickable):
    def __init__(self, rect, player, sound, animation=None, hover_cursor = 2):
        super().__init__(rect, animation, hover_cursor, sound)
        self.player = player

    def on_click(self):

        self.player.talk(self.sound)
        print('grey slot click')


class GreenSlot(Clickable):
    def __init__(self, rect, player, sound, scene, animation=None, hover_cursor = 1):
        super().__init__(rect, animation, hover_cursor, sound)
        self.player = player
        self.scene = scene
        self.red = False
    
    def turn_red(self):
        self.player.crouch()
        self.red = True
        green_slot_img = self.scene.bg_lst[2]
        self.scene.bg_lst[2] = self.scene.bg_lst[1]
        self.scene.bg_lst[1] = green_slot_img

    def on_click(self):
        if not self.red:
            self.player.talk(self.sound[0])
            self.player.move_to(pg.mouse.get_pos(), self.turn_red)
        else:
            self.player.talk(self.sound[1])
            

class Scene1(Scene):
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, background_lst, foreground_lst, collision_file, scale_factor, dev)
        self.id = 0
        
        redslot = GreySlot(pg.Rect((1500, 625, 130, 52)), self.player, os.path.join('sounds', 'characters', 'dr', 'das_sieht_nicht_richtig.ogg'))
        greenslot = GreenSlot(pg.Rect((908, 615, 110, 42)), self.player, [os.path.join('sounds', 'characters', 'dr', 'das_koennte_spaeter.ogg'), os.path.join('sounds', 'characters', 'dr', 'das_sieht_nicht_richtig.ogg')], self)
        greyslot = GreySlot(pg.Rect((1200, 620, 130, 52)), self.player, os.path.join('sounds', 'characters', 'dr', 'sieht_aus_als.ogg'))
        greenbutton1 = Commentable(pg.Rect((1709, 455, 40, 40)), self.player, sound = os.path.join('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        greenbutton2 = Commentable(pg.Rect((1337, 400, 40, 40)), self.player, sound = os.path.join('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        greenbutton3 = Commentable(pg.Rect((852, 400, 40, 40)), self.player, sound = os.path.join('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        redbutton1 = Commentable(pg.Rect((901, 406, 40, 40)), self.player, sound = os.path.join('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        redbutton2 = Commentable(pg.Rect((1291, 428, 40, 40)), self.player, sound = os.path.join('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        redbutton3 = Commentable(pg.Rect((1652, 482, 40, 40)), self.player, sound = os.path.join('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        greybutton = Commentable(pg.Rect((1375, 362, 40, 40)), self.player, sound = os.path.join('sounds', 'characters', 'dr', 'hier_fehlt_wohl_etwas.ogg'))
        midwindow = MidWindow(pg.Rect((1180, 155, 215, 160)), animation = self.bg_lst[0], sound = os.path.join('sounds', 'water.ogg'))

        self.clickable_lst = [ChangeScene(pg.Rect(40, 35, 250, 400), 1, hover_cursor = 3), greyslot, greenslot, redslot, midwindow,
                               greenbutton1, greenbutton2, greenbutton3, redbutton1, redbutton2, redbutton3, greybutton]
