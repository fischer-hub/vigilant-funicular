from src.scene import Scene, Clickable, ChangeScene
import src.animate as am
import pygame as pg
from src.scene import Clickable


class ElevatorDoor(Clickable):
    def __init__(self, rect, scene, animation=None):
        super().__init__(rect, animation)
        self.scene = scene

    def on_click(self):

        self.scene.last_clickable_idx = 0

        if not self.scene.player.moving:
            self.scene.bg_lst[1].default_frame = 6
            self.scene.bg_lst[1].pause = False
            return None
        # we are still walking, send userevent to check in a few seconds again
        else:
            pg.time.set_timer(pg.USEREVENT + 2, 50)
        

class ElevatorScene(Scene):
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor=6, dev=False):
        super().__init__(player, cursor, background_lst, foreground_lst, collision_file, scale_factor, dev)
        
        #elevator_door_clickable = Clickable(pg.Rect(((1180, 420, 50, 55))), elevator_door_animation)
        elevator_door_clickable = ElevatorDoor(pg.Rect(((1180, 420, 50, 55))), self)
        #elevator_door_clickable = pg.Rect((1203, 447, 20, 20)

        
        self.clickable_lst = [ChangeScene(pg.Rect(1849, 128, 100, 900), 0, hover_cursor = 4), ChangeScene(pg.Rect(0, 128, 100, 900), 1, hover_cursor = 3), elevator_door_clickable]
        self.player_spawn = (1737 - (int((self.player.current_animation.img_height / 2 ) * self.player.current_animation.scale_factor)), 870 - (int((self.player.current_animation.img_width / 1.5 ) * self.player.current_animation.scale_factor)))
