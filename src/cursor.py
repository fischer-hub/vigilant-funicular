import pygame as pg


class Cursor:
    def __init__(self, animation_obj):
        self.cursor_img = animation_obj
        self.cursor_img_default = animation_obj
        self.item = ''

    # set cursor img position to mouse position and draw cursor img to screen
    def draw(self, surface):
        self.cursor_img.rect.center = pg.mouse.get_pos()
        self.cursor_img.draw(surface)

    # change the cursor img to index on cursor img sprite
    def change_cursor(self, cursor_sprite_index):
        self.cursor_img.index = cursor_sprite_index
        self.cursor_img.update()