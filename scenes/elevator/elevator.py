from src.scene import Scene, Clickable, ChangeScene, Commentable, Collectable
from src.animate import StripAnimate
import pygame as pg
from lib.helper import path

class Plant(Clickable):
    def __init__(self, rect, player, animation=None, hover_cursor = 2, sound_lst=None, scene = None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.player = player
        self.sound_lst = sound_lst
        self.scene = scene
    
    def on_click(self):
        if 'PUBottleFull' in self.player.inventory:
            self.scene.bg_lst['plant'].pause = False
            self.player.inventory.pop('PUBottleFull')
        else:
            self.player.talk(self.sound_lst)

        return None

class YoyoSleeping(Clickable):
    def __init__(self, rect, player, animation=None, hover_cursor = 2, sound_lst=None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.player = player
    
    def on_click(self):
        self.player.talk(self.sound_lst)
        return None

class Bottles(Clickable):
    def __init__(self, rect, player, sound_lst, scene, animation=None, hover_cursor = 1):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.player = player
        self.scene = scene
        self.collected = False
    
    def collect(self):
        self.player.crouch()
        self.collected = True
        self.scene.bg_lst.pop('bottles')
        self.scene.clickable_lst.pop('bottles')
        grab_sound = pg.mixer.Sound(path(self.sound_lst[0]))
        grab_sound.play(maxtime = 1000)
        self.player.inventory.append('PUBottleEmpty')
        self.player.inventory.append('MateBottleEmpty')

    def on_click(self):
        if not self.collected:
            self.player.talk(self.sound_lst[1])
            self.player.move_to(pg.mouse.get_pos(), self.collect)
        else:
            self.player.talk(self.sound_lst[1])

class ElevatorDoor(Clickable):
    def __init__(self, rect, scene, sound_lst, animation=None, hover_cursor = 2):
        super().__init__(rect, animation, sound_lst = sound_lst, hover_cursor = hover_cursor)
        self.scene = scene

    def on_click(self):

        if self.scene.elevator_fixed:

            self.scene.last_clickable_idx = 0

            if not self.scene.player.moving:
                self.scene.bg_lst[1].default_frame = 6
                self.scene.bg_lst[1].pause = False
                return None
            # we are still walking, send userevent to check in a few seconds again
            else:
                pg.time.set_timer(pg.USEREVENT + 2, 50)
        else:
            self.scene.player.talk(self.sound_lst[0])

        

class ElevatorScene(Scene):
    def __init__(self, player, cursor, collision_file = None, scale_factor=6, dev=False):
        super().__init__(player, cursor, collision_file, scale_factor, dev)
        self.id = 1
        self.elevator_fixed = False
        self.dev = dev
        
        
        # sprites
        elevator_door = StripAnimate('scenes/elevator/elevator_doors.png', img_width = 320, frame_rate = 5, scale_factor = scale_factor, cycles = 1, pause = True)
        yoyo = StripAnimate('sprites/characters/yoyo/yoyo_sleep.png', img_width = 320, frame_rate = 1, scale_factor = scale_factor)
        bottles = StripAnimate('scenes/elevator/bottles.png', img_width = 32, frame_rate = 1, scale_factor = scale_factor, pos = (981* ((self.scale_factor) / 6), 687 * ((self.scale_factor) / 6)))
        rohrzange = StripAnimate('scenes/elevator/rohrzange.png', img_width = 32, frame_rate = 1, scale_factor = scale_factor, pos = (1081 * ((self.scale_factor) / 6), 687 * ((self.scale_factor) / 6)))
        pflanze = StripAnimate('scenes/elevator/elevator_tree.png', img_width = 320, frame_rate = 5, scale_factor = scale_factor, cycles = 1, pause = True)

        # clickables
        elevator_door_clickable = ElevatorDoor(pg.Rect(((1180, 420, 50, 55))), self, sound_lst = [path('sounds', 'characters', 'dr', 'fahrstuhl_ausser_betrieb.ogg')])
        bottles_clickable = Bottles(pg.Rect(((981, 687, 20 * self.scale_factor, 20 * self.scale_factor))), self.player, scene = self, sound_lst = [path('sounds', 'characters', 'dr', 'grab.ogg'), path('sounds', 'characters', 'dr', 'eine_leere_bierflasche.ogg')], animation = bottles)
        yoyo_sleeping_clickable = YoyoSleeping(pg.Rect(1292, 540, 150, 250), self.player, sound_lst = path('sounds', 'characters', 'dr', 'der_handwerker_schlaeft_gerade.ogg'))
        newton_picture = Commentable(pg.Rect(190, 150, 280, 180), self.player, sound_lst = path('sounds', 'characters', 'dr', 'ein_bild_von_isaac_newton.ogg'))
        rohrzange_clickable = Collectable(pg.Rect(1131, 717, 20* self.scale_factor, 20*self.scale_factor), self.player, sound_lst = ['sounds/characters/dr/eine_rohrzange.ogg'], scene = self, list_name = 'rohrzange', item_id_lst = ['Rohrzange'])
        pflanze_clb_top = Plant(pg.Rect(1450, 115, 300, 105), self.player, sound_lst = path('sounds', 'characters', 'dr', 'gegossen_werden.ogg'), scene = self)
        pflanze_clb_bottom = Plant(pg.Rect(1600, 206, 220, 555), self.player, sound_lst = path('sounds', 'characters', 'dr', 'gegossen_werden.ogg'), scene = self)
        

        # sounds
        yoyo_snoring = pg.mixer.Sound(path('sounds', 'characters', 'yoyo', 'snoring.ogg'))
        yoyo_snoring.set_volume(0.3)


        self.bg_lst = {'elevator_inside': 'scenes/elevator/elevator_inside.png', 'elevator_door': elevator_door, 'elevator_band': 'scenes/elevator/band.png', 
                        'elevator_bg': 'scenes/elevator/elevator_bg.png', 'yoyo': yoyo, 'bottles': bottles, 
                        'rohrzange': rohrzange, 'plant': pflanze}
        self.fg_lst = {}
        
        self.bg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.bg_lst.items()}
        self.fg_lst = {key: (layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor)) for key, layer in self.fg_lst.items()}

        
        self.clickable_lst = {'right_change_scene': ChangeScene(pg.Rect(1849, 128, 100, 900), 0, hover_cursor = 4), 'elevator_door': elevator_door_clickable,
                               'bottles': bottles_clickable, 'yoyo': yoyo_sleeping_clickable, 'newton': newton_picture,
                               'rohrzange': rohrzange_clickable, 'left_change_scene': ChangeScene(pg.Rect(0, 128, 100, 900), 2, hover_cursor = 3, pos = (1880 * ((self.scale_factor - 1) / 6), 842 * ((self.scale_factor - 1) / 6))),
                               'plant_top': pflanze_clb_top, 'plant_bottom': pflanze_clb_bottom }

        self.sound_lst += [yoyo_snoring]