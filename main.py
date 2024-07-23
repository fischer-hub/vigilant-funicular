import pygame as pg
import src.animate as am
from src.player import Player
from src.overlay import Overlay
from src.scene import Scene
from scenes.scene1 import Scene1
from scenes.elevator.elevator import ElevatorScene
from lib.helper import record_collision_points
from lib.helper import set_dev
import src.scene as sc
import sys, os


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
    screen = pg.display.set_mode((320 * scale_factor, 180 *scale_factor), display=0)
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
    doctor_talk = am.StripAnimate('sprites/characters/dr_talk.png', frame_rate = 5, scale_factor = scale_factor)
    doctor_crouch = am.StripAnimate('sprites/characters/dr_crouch.png', frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0)

    mid_window = am.StripAnimate('sprites/bg1_mid_window.png', img_width = 320, frame_rate = 5, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)

    inventory = am.StripAnimate('sprites/inventory.png', img_width = 320, frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0)
    menu_buttons = am.StripAnimate('sprites/menu_buttons-sheet.png', img_width = 320, frame_rate = 3, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once = True)


    # init character (Player) objects
    doctor = Player([doctor_idle, doctor_walk, doctor_talk, doctor_crouch], step_size = 2, dev = dev, pos = (1000, 700))
    
    # set background music
    pg.mixer.music.load('sounds/music/colorful_flowers.mp3')
    pg.mixer.music.set_volume(0.1)
    pg.mixer.music.play()


    # init scene objects
    scene1 = Scene1(doctor, cursor, [mid_window, 'sprites/red_slot2.png', 'sprites/green_slot.png', 'sprites/bg1.png'], [pipe, 'sprites/fg1.png'], collision_file = 'scenes/scene1.pickle', scale_factor = scale_factor, dev = dev)
    elevator_scene = ElevatorScene(doctor, cursor, ['scenes/elevator/elevator_inside.png', elevator_door, 'scenes/elevator/elevator_bg.png'], [], collision_file = 'scenes/elevator/collision.pickle', scale_factor = scale_factor, dev = dev)
    overlay = Overlay(doctor, cursor, [inventory, menu_buttons], [])

    # init scene handler
    scene_handler = sc.SceneHandler([scene1, elevator_scene], doctor, overlay)


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

            # we have to handle events moving the player to catch cases where a clickable was clicked but we dont want to walk to mous position
            scene_handler.handle_event(event)

 
                 
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_q and dev:
                    record_collision_points(p1, p2, scale_factor, screen, str(sys.argv[2]))

                elif event.key == pg.K_e:
                    if overlay.hide:
                        overlay.hide = False
                    else:
                        overlay.hide = True

            if event.type == pg.QUIT:
                running = False
            
        
        # draw rect on screen
        #pg.draw.rect(screen, (255,255,255), (0, 128, 100, 900))
        
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