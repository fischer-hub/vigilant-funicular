import pygame as pg
from src.animate import StripAnimate
import pickle

class Scene():
    def __init__(self, background_lst, foreground_lst, collision_file, scale_factor = 6, dev = False):
        self.bg_lst = [layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(layer).convert_alpha(), scale_factor) for layer in background_lst]
        self.fg_lst = [layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(layer).convert_alpha(), scale_factor) for layer in foreground_lst]

        self.show_collision = False

        if not dev:
            with open((collision_file), "rb") as fn: 
                self.collision_lst = pickle.load(fn)
        else:
            self.collision_lst = [0] * 8000
            

    def draw_bg(self, surface):
        for layer in self.bg_lst:
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))
                    

    def draw_fg(self, surface):
        
        if self.show_collision:
            for i in range(len(self.collision_lst)):
                surface.set_at((i, self.collision_lst[i]), "red")

        for layer in self.fg_lst:
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))