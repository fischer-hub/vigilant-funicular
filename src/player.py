from lib.helper import sign, path, save_config
from src.animate import StripAnimate
import pygame as pg
import os

class Player():
    def __init__(self, anim_lst, collision_lst = [], step_size = 5, pos = (5, 5), dev = False, config = {}):

        self.dev = dev
        self.collision_lst = collision_lst
        self.animation_lst = anim_lst
        self.moving = False
        self.talking = False
        self.destination_pos = pos
        self.step_size = step_size
        self.current_animation = anim_lst[0] if not self.moving else anim_lst[1]
        self.current_animation.rect[0] = pos[0]
        self.current_animation.rect[1] = pos[1]
        self.rect = self.current_animation.rect
        self.flip = False
        self.steps_sound = pg.mixer.Sound(path('sounds/characters/dr/steps.ogg'))
        self.talk_sound = None
        self.function_to_exec = None
        self.inventory = []
        self.config = config

    

    def correct_y_pos_on_collision(self, pos):

        """Given a pos tuple, return the list with y value shifted such that y <= y of collision border"""
        
        x_offset = int((self.current_animation.img_height / 2 ) * self.current_animation.scale_factor)
        y_offset = int((self.current_animation.img_width / 1.5 ) * self.current_animation.scale_factor)
        
        # catch funky x coords going out of bounds, not a good fix but oh well this isnt a good game so its sufficient
        #if pos[0] < 0: 
        #    pos = (0, pos[1])
        # if we reach the collision bound, set y to y value at collision border, dont ask me whats going on with the x offset i dont understand why its working but im not touching it anymore
        if not self.dev and (pos[1] <= (self.collision_lst[pos[0] + x_offset] - y_offset)):
            
            return [pos[0], int(self.collision_lst[pos[0] + x_offset] - y_offset)]
        else:
            return pos


    def move_to(self, pos, function = None):

        if (self.current_animation.rect[0:1]) != pos:

            # stop step sound if we already were walking
            self.steps_sound.stop()
            self.steps_sound.play(loops = -1)

            # the position of the mouse click is where the feet of the character should end up on the screen, approximately, shift and scale the sprite accordingly
            x_offset = (self.current_animation.img_height / 2 ) * self.current_animation.scale_factor
            y_offset = (self.current_animation.img_width / 1.5 ) * self.current_animation.scale_factor

            self.destination_pos = (int(pos[0] - x_offset), int(pos[1] - y_offset))
            
            self.destination_pos = self.correct_y_pos_on_collision(self.destination_pos)

            # set moving bool to true and change animation to walking animation (2), change position of sprite to curretn pos of player
            self.moving = True
            self.rect = self.current_animation.rect
            self.current_animation = self.animation_lst[1]
            self.current_animation.rect = self.rect
        
        if function: self.function_to_exec = function


    def update(self):

        """Updates the sprite to the next frame based on the frame rate and changes the rect position until it matches the destination position."""

        # check if we arrived at destination position
        if self.current_animation.rect[0] == self.destination_pos[0] and self.current_animation.rect[1] == self.destination_pos[1] and self.moving: # and self.talking
            self.moving = False
            

            if not self.talking:
                self.current_animation = self.animation_lst[0]

            self.steps_sound.stop()

            if self.function_to_exec: 
                self.function_to_exec()
                self.function_to_exec = None

            #if self.talking:
            #    self.current_animation = self.animation_lst[2]
            #    self.current_animation.pause = False

        else:


            # check if distance to destination is pos or negative and shift by step size
            self.current_animation.rect[0] += sign(self.destination_pos[0] - self.current_animation.rect[0]) * self.step_size
            self.current_animation.rect[1] += sign(self.destination_pos[1] - self.current_animation.rect[1]) * self.step_size
            
            x_corr, y_corr = self.correct_y_pos_on_collision((self.current_animation.rect[0], self.current_animation.rect[1]))
            self.current_animation.rect[0] = x_corr
            self.current_animation.rect[1] = y_corr

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
    

    def draw(self, surface):
        """Calls the draw function for the current animation."""
        self.update()
        self.current_animation.draw(surface, self.flip)

    def talk(self, audiofile):
        # stop talking if we are already talking to prevent talking over ourself
        if self.talk_sound: self.talk_sound.stop()
        self.talk_sound = pg.mixer.Sound(path(audiofile))
        self.talking = True
        self.moving = False
        self.rect = self.current_animation.rect
        self.current_animation = self.animation_lst[2]
        self.current_animation.rect = self.rect
        self.destination_pos = (self.rect[0], self.rect[1])
        self.steps_sound.stop()
        pg.mixer.Sound.play(self.talk_sound)
        print('talk triggered')
        pg.time.set_timer(pg.USEREVENT + 3, int(self.talk_sound.get_length() * 1000), 1)

    def crouch(self):
        self.rect = self.current_animation.rect
        self.current_animation = self.animation_lst[3]
        self.current_animation.pause = False
        self.current_animation.rect = self.rect
        self.destination_pos = (self.rect[0], self.rect[1])
        # check if we are talking in a few secs when crouch animation is done
        pg.time.set_timer(pg.USEREVENT + 4, 1000)

    def save(self):
        save_config(self.config)