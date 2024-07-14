import pygame as pg


class StripAnimate(pg.sprite.Sprite):
    """
    A class to animate a strip of sprites for a Pygame application.

    This class handles loading a sprite sheet (strip of sprites) and animating
    it frame by frame. It supports scaling the sprite frames by a sclaing factor
    and controlling the frame rate of the animation.

    Attributes:
        sprite_sheet (pg.Surface): The loaded sprite sheet image.
        index (int): The index to keep track of the current frame being displayed.
        sprite_offset (int): The pixel offset from the start of the sprite sheet to the current frame.
        scale_factor (int): The factor by which to scale the sprite frames.
        sprite_width (int): The width of the sprite sheet.
        img_height (int): The height of each sprite frame.
        img_width (int): The width of each sprite frame.
        image (pg.Surface): The current sprite frame image.
        rect (pg.Rect): The rectangle defining the position and dimensions of the sprite.
        frame_timestamp (int): The timestamp of the last frame update.
        frame_rate (int): The frame rate of the animation (frames per second).
        x (int): The int value of the X-coordinate of the left side of the rectangle.
        y (int): The int value of the Y-coordinate of the left side of the rectangle.


    Methods:
        update(): Updates the sprite to the next frame based on the frame rate.
    """
    def __init__(self, sprite_path: str, img_width = 0, scale_factor = 6, frame_rate = 1, pos = (0, 0), cycles = 0, default_frame = 0, pause = False):
        super(StripAnimate, self).__init__()
        
        # load sprite sheet image file
        self.sprite_sheet = pg.image.load(sprite_path).convert_alpha()

        # index to keep track of which frame of the animation is currently displayed
        self.index = 0

        # pixel offset from sprite start to current frame
        self.sprite_offset = 0

        # scale sprite to right resolution, e.g.: for background 320x180 -> 1920x1080 scale factor = 6
        self.scale_factor = scale_factor

        # get width of the whole sprite sheet (strip), image height is equal to sprite sheet height for strips
        self.sprite_width = self.sprite_sheet.get_width()
        self.img_height = self.sprite_sheet.get_height()

        # if image height is not set, assume the sprite is a square and sprite sheet height equals image width
        self.img_width = self.img_height if not img_width else img_width

        # initialize animation with first frame of sprite strip and scale to right resolution
        self.image = pg.transform.scale_by(self.sprite_sheet.subsurface([0, 0, self.img_width, self.img_height]), self.scale_factor)

        # set rect (what does this do??)
        self.rect = pg.Rect(pos[0], pos[1], self.img_width, self.img_height)

        # initialize time of first frame displayed
        self.frame_timestamp = pg.time.get_ticks()

        # set frame rate of animations in FPS (i hope)
        self.frame_rate = frame_rate

        # number of animation cycles that should be played
        self.cycles = cycles

        # current number of animation cycles already played
        self.cycle_count = 1

        # frame to show when no animation is played
        self.default_frame = default_frame

        self.pause = pause


    def update(self):

        """Updates the sprite to the next frame based on the frame rate."""
        
        # check if time span for set frame rate has passed since last update call
        if pg.time.get_ticks() - self.frame_timestamp > 1000 / self.frame_rate:

            if self.pause:
                return

            self.frame_timestamp = pg.time.get_ticks()
            self.index += 1
            self.sprite_offset = self.index * self.img_width

            # end of sprite reached, wrap around to first frame
            if self.sprite_offset >= self.sprite_width:
                
                # if cycle not 0 and cycle limit reached, return from update (end on last frame of spritesheet)
                if self.cycles and (self.cycles <= self.cycle_count):
                    print(self.cycle_count, self.cycles)
                    #self.index = self.default_frame
                    return
                
                self.cycle_count += 1
                self.index = 0
                self.sprite_offset = 0

            self.image = pg.transform.scale_by(self.sprite_sheet.subsurface([self.index * self.img_width, 0, self.img_width, self.img_height]), self.scale_factor)


    def draw(self, surface, flip = False):

        """Draw current image of sprite sheet, flipped if flip is true. Flip is true if the player moves in the opposite direction that the animation is implying."""
        
        if flip:
            surface.blit(pg.transform.flip(self.image, True, False), self.rect)
        else:
            surface.blit(self.image, self.rect)

