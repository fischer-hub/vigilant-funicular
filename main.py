# Example file showing a circle moving on screen
import pygame as pg
import src.animate as am
from src.player import Player
from src.scene import Scene
from lib.helper import record_collision_points
from lib.helper import set_dev
import sys



def main():
    
    if len(sys.argv) > 1:
        set_dev(True)
        dev = True
    else:
        set_dev(False)
        dev = False

    # pg setup
    pg.init()
    scale_factor = 6
    screen = pg.display.set_mode((320 * scale_factor, 180 *scale_factor))
    clock = pg.time.Clock()
    running = True
    dt = 0

    p1 = []
    p2 = []

    # initial position for sprite top left corner
    pipe = am.StripAnimate('sprites/fg1_pipe.png', frame_rate = 5, scale_factor = scale_factor, img_width = 320)
    scene1 = Scene(['sprites/bg1.png'], [pipe, 'sprites/fg1.png'], 'scenes/scene1.pickle', scale_factor = scale_factor, dev = dev)
    doctor_idle = am.StripAnimate('sprites/dr_idle.png', scale_factor = scale_factor)
    doctor_walk = am.StripAnimate('sprites/dr_walk.png', frame_rate = 5, scale_factor = scale_factor)
    doctor = Player([doctor_idle, doctor_walk], scene1.collision_lst, step_size = 2, dev = dev, pos = (1000, 700))
    if dev: scene1.draw_bg(screen)

    while running:


        if not dev:

            # display background
            scene1.draw_bg(screen)
        
            # call draw function on doctor ass sprites
            doctor.draw(screen)

            # load and display foreground
            scene1.draw_fg(screen)

        # poll for events
        for event in pg.event.get():

            # handle MOUSEBUTTONUP
            if event.type == pg.MOUSEBUTTONUP:
                 mpos = pg.mouse.get_pos()
                 doctor.move_to(mpos)

                 # maybe put this in an extra fct at some point
                 if dev:
                    p1.append(mpos[0])
                    p2.append(mpos[1])
                 
            if dev and event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    record_collision_points(p1, p2, scale_factor, screen, str(sys.argv[1]))

            if event.type == pg.QUIT:
                running = False

        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pg.quit()

if __name__ == '__main__':
    main()