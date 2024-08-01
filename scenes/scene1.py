from src.scene import Scene, Clickable, ChangeScene, Commentable
import pygame as pg
import os


class Bird(Clickable):
    def __init__(self, rect, animation=None, hover_cursor = 1, sound_lst=None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
    
    def on_click(self):
        if self.animation.pause:
            self.animation.pause = False
            sound = pg.mixer.Sound(self.sound_lst)
            sound.set_volume(0.8)
            sound.play()

        return 42


class MidWindow(Clickable):
    def __init__(self, rect, animation=None, hover_cursor = 1, sound_lst=None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
    
    def on_click(self):
        if self.animation.pause:
            self.animation.pause = False
            sound = pg.mixer.Sound(self.sound_lst)
            sound.set_volume(0.2)
            sound.play()

        return 42
    
class GreySlot(Clickable):
    def __init__(self, rect, player, sound_lst, animation=None, hover_cursor = 2):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.player = player

    def on_click(self):

        self.player.talk(self.sound_lst)
        print('grey slot click')


class GreenSlot(Clickable):
    def __init__(self, rect, player, sound_lst, scene, animation=None, hover_cursor = 1):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.player = player
        self.scene = scene
        self.red = False
    
    def turn_red(self):
        self.player.crouch()
        self.red = True
        green_slot_img = self.scene.bg_lst[2]
        self.scene.bg_lst[2] = self.scene.bg_lst[1]
        self.scene.bg_lst[1] = green_slot_img
        grab_sound = pg.mixer.Sound(self.sound_lst[2])
        grab_sound.play(maxtime = 1000)
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')

    def on_click(self):
        if not self.red:
            self.player.talk(self.sound_lst[0])
            self.player.move_to(pg.mouse.get_pos(), self.turn_red)
        else:
            self.player.talk(self.sound_lst[1])
            

class Scene1(Scene):
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, background_lst, foreground_lst, collision_file, scale_factor, dev)
        self.id = 0
        
        redslot = GreySlot(pg.Rect((1500, 625, 130, 52)), self.player, os.path.join('sounds', 'characters', 'dr', 'das_sieht_nicht_richtig.ogg'))
        greenslot = GreenSlot(pg.Rect((908, 615, 110, 42)), self.player, [os.path.join('sounds', 'characters', 'dr', 'das_koennte_spaeter.ogg'), os.path.join('sounds', 'characters', 'dr', 'das_sieht_nicht_richtig.ogg'), os.path.join('sounds', 'characters', 'dr', 'grab.ogg')], self)
        greyslot = GreySlot(pg.Rect((1200, 620, 130, 52)), self.player, os.path.join('sounds', 'characters', 'dr', 'sieht_aus_als.ogg'))
        greenbutton1 = Commentable(pg.Rect((1709, 455, 40, 40)), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        greenbutton2 = Commentable(pg.Rect((1337, 400, 40, 40)), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        greenbutton3 = Commentable(pg.Rect((852, 400, 40, 40)), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        redbutton1 = Commentable(pg.Rect((901, 406, 40, 40)), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        redbutton2 = Commentable(pg.Rect((1291, 428, 40, 40)), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        redbutton3 = Commentable(pg.Rect((1652, 482, 40, 40)), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        greybutton = Commentable(pg.Rect((1375, 362, 40, 40)), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'hier_fehlt_wohl_etwas.ogg'))
        midwindow = MidWindow(pg.Rect((1180, 155, 215, 160)), animation = self.bg_lst[0], sound_lst = os.path.join('sounds', 'water.ogg'))
        bird = Bird(pg.Rect((1650, 0, 250, 100)), self.fg_lst[-1], sound_lst = os.path.join('sounds', 'bird_flap.ogg'))



        self.clickable_lst = [ChangeScene(pg.Rect(40, 35, 250, 400), 1, hover_cursor = 3), greyslot, greenslot, redslot, midwindow,
                               greenbutton1, greenbutton2, greenbutton3, redbutton1, redbutton2, redbutton3, greybutton, bird]
