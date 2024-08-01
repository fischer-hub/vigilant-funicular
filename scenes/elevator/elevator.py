from src.scene import Scene, Clickable, ChangeScene, Commentable
from src.animate import StripAnimate
import pygame as pg
from src.scene import Clickable
import os

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
        self.scene.bg_lst.pop(5)
        self.scene.clickable_lst.pop(3)
        grab_sound = pg.mixer.Sound(self.sound_lst[0])
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
    def __init__(self, rect, scene, sound_lst, animation=None):
        super().__init__(rect, animation, sound_lst = sound_lst)
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
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor=6, dev=False):
        super().__init__(player, cursor, background_lst, foreground_lst, collision_file, scale_factor, dev)
        self.id = 1
        self.elevator_fixed = False
        
        
        # sprites
        elevator_door = StripAnimate('scenes/elevator/elevator_doors.png', img_width = 320, frame_rate = 5, scale_factor = scale_factor, cycles = 1, pause = True)
        yoyo = StripAnimate(os.path.join('sprites', 'characters', 'yoyo', 'yoyo_sleep.png'), img_width = 320, frame_rate = 1, scale_factor = scale_factor)
        bottles = StripAnimate(os.path.join('scenes', 'elevator', 'bottles.png'), img_width = 32, frame_rate = 1, scale_factor = scale_factor, pos = (981, 687))
        
        #clickables
        elevator_door_clickable = ElevatorDoor(pg.Rect(((1180, 420, 50, 55))), self, sound_lst = [os.path.join('sounds', 'characters', 'dr', 'fahrstuhl_ausser_betrieb.ogg')])
        bottles_clickable = Bottles(pg.Rect(((981, 687, 32 * self.scale_factor, 32 * self.scale_factor))), self.player, scene = self, sound_lst = [os.path.join('sounds', 'characters', 'dr', 'grab.ogg'), os.path.join('sounds', 'characters', 'dr', 'eine_leere_bierflasche.ogg')], animation = bottles)
        yoyo_sleeping_clickable = YoyoSleeping(pg.Rect(1292, 540, 150, 250), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'der_handwerker_schlaeft_gerade.ogg'))
        newton_picture = Commentable(pg.Rect(190, 150, 280, 180), self.player, sound_lst = os.path.join('sounds', 'characters', 'dr', 'ein_bild_von_isaac_newton.ogg'))

        # sounds
        yoyo_snoring = pg.mixer.Sound(os.path.join('sounds', 'characters', 'yoyo', 'snoring.ogg'))
        yoyo_snoring.set_volume(0.3)

        self.player_spawn = (1737 - (int((self.player.current_animation.img_height / 2 ) * self.player.current_animation.scale_factor)), 870 - (int((self.player.current_animation.img_width / 1.5 ) * self.player.current_animation.scale_factor)))


        self.bg_lst += ['scenes/elevator/elevator_inside.png', elevator_door, os.path.join('scenes', 'elevator', 'band.png'), 'scenes/elevator/elevator_bg.png', yoyo,
                        bottles]
        self.bg_lst = [layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(layer).convert_alpha(), scale_factor) for layer in self.bg_lst]

        
        self.clickable_lst = [ChangeScene(pg.Rect(1849, 128, 100, 900), 0, hover_cursor = 4), ChangeScene(pg.Rect(0, 128, 100, 900), 1, hover_cursor = 3), 
                              elevator_door_clickable, bottles_clickable, yoyo_sleeping_clickable, newton_picture]

        self.sound_lst += [yoyo_snoring]