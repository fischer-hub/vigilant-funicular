# Example file showing a circle moving on screen
import pygame as pg
import src.animate as am
from src.player import Player
from src.scene import Scene
from scenes.scene1 import Scene1
from scenes.elevator.elevator import ElevatorScene
from lib.helper import record_collision_points
from lib.helper import set_dev
import src.scene as sc
import sys


class Cursor:
    def __init__(self, animation_obj):
        self.cursor_img = animation_obj

    # set cursor img position to mouse position and draw cursor img to screen
    def draw(self, surface):
        self.cursor_img.rect.center = pg.mouse.get_pos()
        self.cursor_img.draw(surface)

    # change the cursor img to index on cursor img sprite
    def change_cursor(self, cursor_sprite_index):
        self.cursor_img.index = cursor_sprite_index
        self.cursor_img.update()
        


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

    # set mouse invisable and init cursor
    pg.mouse.set_visible(False)
    cursor = Cursor(am.StripAnimate('sprites/cursor.png', 16, scale_factor/2, pause = True))

    # init StripAnimate objects (maybe move this to the respective scene class for cleaner code)
    pipe = am.StripAnimate('sprites/fg1_pipe.png', frame_rate = 5, scale_factor = scale_factor, img_width = 320)
    elevator_door = am.StripAnimate('scenes/elevator/elevator_doors.png', img_width = 320, frame_rate = 5, scale_factor = scale_factor, cycles = 1, pause = True)
    doctor_idle = am.StripAnimate('sprites/dr_idle.png', scale_factor = scale_factor)
    doctor_walk = am.StripAnimate('sprites/dr_walk.png', frame_rate = 5, scale_factor = scale_factor)

    # init character (Player) objects
    doctor = Player([doctor_idle, doctor_walk], step_size = 2, dev = dev, pos = (1000, 700))

    # init scene objects
    scene1 = Scene1(doctor, cursor, ['sprites/bg1.png'], [pipe, 'sprites/fg1.png'], collision_file = 'scenes/scene1.pickle', scale_factor = scale_factor, dev = dev)
    elevator_scene = ElevatorScene(doctor, cursor, ['scenes/elevator/elevator_inside.png', elevator_door, 'scenes/elevator/elevator_bg.png'], [], collision_file = 'scenes/elevator/collision.pickle', scale_factor = scale_factor, dev = dev)

    # init scene handler
    scene_handler = sc.SceneHandler([scene1, elevator_scene], doctor)


    # whatever that is
    if dev: elevator_scene.draw_bg(screen)


    while running:

        
        if not dev:

            # display background
            scene_handler.draw_bg(screen)
        
            # call draw function on doctor ass sprites
            doctor.draw(screen)

            # load and display foreground
            scene_handler.draw_fg(screen)

        # poll for events
        for event in pg.event.get():

            # handle MOUSEBUTTONUP
            if event.type == pg.MOUSEBUTTONUP:
                 mpos = pg.mouse.get_pos()
                 doctor.move_to(mpos)
                 print(mpos)

                 # maybe put this in an extra fct at some point
                 if dev:
                    p1.append(mpos[0])
                    p2.append(mpos[1])
                 
            if dev and event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    record_collision_points(p1, p2, scale_factor, screen, str(sys.argv[2]))

            if event.type == pg.QUIT:
                running = False
            
            scene_handler.handle_event(event)

        # draw rect on screen
        pg.draw.rect(screen, (255,255,255), (1200, 620, 130, 52))

        cursor.draw(screen)

        #screen.blit(clickable_surf, change_scene_clickable)
        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000


    pg.quit()

if __name__ == '__main__':
    main()