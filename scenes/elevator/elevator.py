from src.scene import Scene, Clickable
import src.animate as am
import pygame as pg
from src.scene import Clickable


class ElevatorDoor(Clickable):
    def __init__(self, rect, scene, animation=None):
        super().__init__(rect, animation)
        self.scene = scene

    def on_click(self):
        self.scene.bg_lst = [self.animation] + self.scene.bg_lst
        return None

class ElevatorScene(Scene):
    def __init__(self, player, background_lst, foreground_lst, collision_file = None, scale_factor=6, dev=False):
        super().__init__(player, background_lst, foreground_lst, collision_file, scale_factor, dev)
        
        elevator_door_animation = am.StripAnimate('scenes/elevator/elevator_doors.png', img_width = 320, frame_rate = 5, scale_factor = scale_factor, cycles = 1) 
        #elevator_door_clickable = Clickable(pg.Rect(((1180, 420, 50, 55))), elevator_door_animation)
        elevator_door_clickable = ElevatorDoor(pg.Rect(((1180, 420, 50, 55))), self, elevator_door_animation)
        #elevator_door_clickable = pg.Rect((1203, 447, 20, 20)

        
        self.clickable_lst = [elevator_door_clickable]
