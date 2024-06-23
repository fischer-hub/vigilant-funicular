from lib.helper import sign
from lib.animate import StripAnimate
import pygame as pg

class Player():
    def __init__(self, anim_lst, step_size = 5, pos = (5, 5)):
        self.animation_lst = anim_lst
        self.moving = False
        self.destination_pos = pos
        self.step_size = step_size
        self.current_animation = anim_lst[0] if not self.moving else anim_lst[1]
        self.rect = self.current_animation.rect
        self.flip = False
    
    def update_pos(self, pos):
        if (self.current_animation.rect[0:1]) != pos:
            # the position of the mouse click is where the feet of the character should end up on the screen, approximately, shift and scale the sprite accordingly
            self.destination_pos = (pos[0] - ((self.current_animation.img_height / 2) * self.current_animation.scale_factor), pos[1] - ((self.current_animation.img_width / 1.5 ) * self.current_animation.scale_factor))
            
            # set moving bool to true and change animation to walking animation (2), change position of sprite to curretn pos of player
            self.moving = True
            self.rect = self.current_animation.rect
            self.current_animation = self.animation_lst[1]
            self.current_animation.rect = self.rect

    
    def update(self):

        """Updates the sprite to the next frame based on the frame rate and changes the rect position until it matches the destination position."""
        
        # check if we arrived at destination position
        if (self.current_animation.rect[0], self.current_animation.rect[1]) == self.destination_pos:
            self.moving = False
            self.current_animation = self.animation_lst[0]
        else:
            # check if distance to destination is pos or negative and shift by step size
            self.current_animation.rect[0] += sign(self.destination_pos[0] - self.current_animation.rect[0]) * self.step_size
            self.current_animation.rect[1] += sign(self.destination_pos[1] - self.current_animation.rect[1]) * self.step_size

            # if distance to destination is smaller than the step size set pos to destination to avoid twitching animation
            if abs(self.destination_pos[0] - self.current_animation.rect[0]) <= self.step_size:
                self.current_animation.rect[0] = self.destination_pos[0]
            if abs(self.destination_pos[1] - self.current_animation.rect[1]) <= self.step_size:
                self.current_animation.rect[1] = self.destination_pos[1]

        # check if time span for set frame rate has passed since last update call
        self.current_animation.update()

        if self.destination_pos[0] - self.current_animation.rect[0] < 0:
            self.flip = True
        else:
            self.flip = False
        print('curr pos: ', (self.current_animation.rect[0], self.current_animation.rect[1]))
        print('destination: ', self.destination_pos)

    

    def draw(self, surface):
        """Calls the draw function for the current animation."""
        self.update()
        self.current_animation.draw(surface, self.flip)
