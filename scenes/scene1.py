from src.scene import Scene, Clickable, ChangeScene, Commentable
import pygame as pg
from lib.helper import path
from src.animate import StripAnimate


class Bird(Clickable):
    def __init__(self, rect, animation=None, hover_cursor = 1, sound_lst=None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
    
    def on_click(self):
        if self.animation.pause:
            self.animation.pause = False
            sound = pg.mixer.Sound(path(self.sound_lst))
            sound.set_volume(0.8)
            sound.play()

        return 42


class MidWindow(Clickable):
    def __init__(self, rect, animation=None, hover_cursor = 1, sound_lst=None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
    
    def on_click(self):
        if self.animation.pause:
            self.animation.pause = False
            sound = pg.mixer.Sound(path(self.sound_lst))
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
        self.player.config['savegame']['scene1'] = {'red': False}
    
    def turn_red(self):
        self.player.crouch()
        self.player.config['savegame']['scene1'].update({'red': True})
        self.scene.bg_lst.pop('green_slot')
        grab_sound = pg.mixer.Sound(path(self.sound_lst[2]))
        grab_sound.play(maxtime = 1000)
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')
        self.player.inventory.append('ATPContainerFilled')

    def on_click(self):
        if not self.player.config['savegame']['scene1']['red']:
            self.player.talk(self.sound_lst[0])
            self.player.move_to(pg.mouse.get_pos(), self.turn_red)
        else:
            self.player.talk(self.sound_lst[1])
            

class Scene1(Scene):
    def __init__(self, player, cursor, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, collision_file, scale_factor, dev)
        self.id = 0
        self.player.scene = self
        self.dev = dev

        mid_window = StripAnimate('sprites/bg1_mid_window.png', img_width = 320, frame_rate = 5, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        bird = StripAnimate('sprites/bird.png', img_width = 320, frame_rate = 14, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)
        pipe = StripAnimate('sprites/fg1_pipe.png', frame_rate = 5, scale_factor = scale_factor, img_width = 320)

        self.bg_lst = {'mid_window': mid_window, 'red_slot': 'sprites/red_slot2.png',  'bg1': 'sprites/bg1.png'}

        # this is so bad pls change this omg (i probably won't), fix the savegame loading to get a default one like the config
        try:
            if not self.player.config['savegame']['scene1']['red']: self.bg_lst.update({'green_slot': 'sprites/green_slot.png'})
        except KeyError:
            pass
        
        self.fg_lst = {'pipe': pipe, 'fg1': 'sprites/fg1.png', 'bird': bird}

        redslot = GreySlot(pg.Rect((1500, 625, 130, 52)), self.player, path('sounds', 'characters', 'dr', 'das_sieht_nicht_richtig.ogg'))
        greenslot = GreenSlot(pg.Rect((908, 615, 110, 42)), self.player, [path('sounds', 'characters', 'dr', 'das_koennte_spaeter.ogg'), path('sounds', 'characters', 'dr', 'das_sieht_nicht_richtig.ogg'), path('sounds', 'characters', 'dr', 'grab.ogg')], self)
        greyslot = GreySlot(pg.Rect((1200, 620, 130, 52)), self.player, path('sounds', 'characters', 'dr', 'sieht_aus_als.ogg'))
        greenbutton1 = Commentable(pg.Rect((1709, 455, 40, 40)), self.player, sound_lst = path('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        greenbutton2 = Commentable(pg.Rect((1337, 400, 40, 40)), self.player, sound_lst = path('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        greenbutton3 = Commentable(pg.Rect((852, 400, 40, 40)), self.player, sound_lst = path('sounds', 'characters', 'dr', 'ein_gruener_knopf.ogg'))
        redbutton1 = Commentable(pg.Rect((901, 406, 40, 40)), self.player, sound_lst = path('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        redbutton2 = Commentable(pg.Rect((1291, 428, 40, 40)), self.player, sound_lst = path('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        redbutton3 = Commentable(pg.Rect((1652, 482, 40, 40)), self.player, sound_lst = path('sounds', 'characters', 'dr', 'ein_roter_knopf.ogg'))
        greybutton = Commentable(pg.Rect((1375, 362, 40, 40)), self.player, sound_lst = path('sounds', 'characters', 'dr', 'hier_fehlt_wohl_etwas.ogg'))
        midwindow = MidWindow(pg.Rect((1180, 155, 215, 160)), animation = self.bg_lst['mid_window'], sound_lst = path('sounds', 'water.ogg'))
        bird = Bird(pg.Rect((1650, 0, 250, 100)), self.fg_lst['bird'], sound_lst = path('sounds', 'bird_flap.ogg'))

        self.bg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.bg_lst.items()}
        self.fg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.fg_lst.items()}


        self.clickable_lst = {'change_scene_left': ChangeScene(pg.Rect(40, 35, 250, 400), 1, hover_cursor = 3, pos = (1737 * ((self.scale_factor - 1) / 6), 870 * ((self.scale_factor - 1) / 6))), 'grey_slot': greyslot, 'green_slot': greenslot,
                              'red_slot': redslot, 'mid_window': midwindow, 'green_button1': greenbutton1,
                              'green_button2': greenbutton2, 'green_button3': greenbutton3, 'red_button1': redbutton1,
                              'red_button2': redbutton2, 'red_button3': redbutton3, 'grey_button': greybutton,
                              'bird': bird}
