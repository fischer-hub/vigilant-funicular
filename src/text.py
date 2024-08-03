import pygame as pg
from lib.helper import path


class Text():
    def __init__(self, text, rect, size, color, scale_factor):
        self.scale_factor = scale_factor
        self.rect = rect
        my_font = pg.font.Font(path('Pixeled.ttf'), scale_factor * size)
        self.text = my_font.render(text, False, color)


    def draw(self, surface):
        surface.blit(self.text, tuple(int(value * (self.scale_factor / 6)) for value in self.rect))

    def update(self):
        pass