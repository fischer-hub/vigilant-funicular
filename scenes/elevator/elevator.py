from src.scene import Scene, Clickable
import pygame as pg


class ElevatorScene(Scene):
    def __init__(self, player, background_lst, foreground_lst, collision_file = None, scale_factor=6, dev=False):
        super().__init__(player, background_lst, foreground_lst, collision_file, scale_factor, dev)
        
        self.clickable_lst = []
