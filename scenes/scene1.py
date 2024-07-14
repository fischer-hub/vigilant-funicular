from src.scene import Scene, Clickable, ChangeScene
import pygame as pg

class GreySlot(Clickable):
    def __init__(self, rect, scene, animation=None, hover_cursor = 2):
        super().__init__(rect, animation, hover_cursor)
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

class Scene1(Scene):
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor = 6, dev = False):
        super().__init__(player, cursor, background_lst, foreground_lst, collision_file, scale_factor, dev)
        
        greslot = GreySlot(pg.Rect((1200, 620, 130, 52)), 1)
        self.clickable_lst = [ChangeScene(pg.Rect(40, 35, 250, 400), 1, hover_cursor = 3), greslot]
