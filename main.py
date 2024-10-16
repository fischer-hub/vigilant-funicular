import pygame as pg
import src.animate as am
from src.player import Player
from src.overlay import Overlay
from src.cursor import Cursor
from src.load_game import LoadGame
from scenes.start_screen.start import StartScreen
from scenes.scene1 import Scene1
from scenes.elevator.elevator import ElevatorScene
from scenes.bathroom.bathroom import Bathroom
import lib.helper as util 
import src.scene as sc
import sys




def main():

    print(sys.argv)
    
    # load config file
    config = util.load_config()
    config['version'] = 'v0.0.2-alpha'

    # I think this doesnt even work..    
    if 'dev' in sys.argv:
        config['dev'] = dev = True 
        print('Running in dev mode')
    else:
        config['dev'] = dev = False


    # pg setup
    pg.init()
    pg.font.init()

    scale_factor = 3 if not 'scale_factor' in config else config['scale_factor']
    if dev: scale_factor = 6
    screen = pg.display.set_mode((320 * scale_factor, 180 * scale_factor), display=0)
    clock = pg.time.Clock()
    running = True
    dt = 0

    p1 = []
    p2 = []

    # set mouse invisable and init cursor
    pg.mouse.set_visible(False)
    cursor = Cursor(am.StripAnimate('sprites/cursor.png', 16, scale_factor/2, pause = True))

    # init StripAnimate objects (maybe move this to the respective scene class for cleaner code)
    doctor_idle = am.StripAnimate('sprites/dr_idle.png', scale_factor = scale_factor)
    doctor_walk = am.StripAnimate('sprites/dr_walk.png', frame_rate = 5, scale_factor = scale_factor)
    doctor_talk = am.StripAnimate('sprites/characters/dr_talk.png', frame_rate = 5, scale_factor = scale_factor)
    doctor_crouch = am.StripAnimate('sprites/characters/dr_crouch.png', frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once =  True)
    doctor_stretch = am.StripAnimate('sprites/characters/dr_stretch.png', frame_rate = 1, scale_factor = scale_factor, cycles = 1, default_frame = 0, pause = True, once =  True)

    # init character (Player) objects
    doctor = Player([doctor_idle, doctor_walk, doctor_talk, doctor_crouch, doctor_stretch], step_size = 2, dev = dev, pos = (-100, -100), config = config)
    
    # this makes sure the inventory is loaded correctly from the savegame before the scenes are initialized, since some items only get rendered in the scene when they are not in the players inventory yet
    if any("slay" in arg for arg in sys.argv): doctor.load()
    
    # set background music
    pg.mixer.music.load(util.path('sounds/music/colorful_flowers.mp3'))
    pg.mixer.music.set_volume(0.1)
    pg.mixer.music.play()


    # init scene objects
    start_screen = StartScreen(doctor, cursor, collision_file = 'scenes/scene1.pickle', scale_factor = scale_factor, dev = dev, config = config)
    load_game = LoadGame(doctor, cursor, scale_factor = scale_factor, dev = dev)
    scene1 = Scene1(doctor, cursor, collision_file = 'scenes/scene1.pickle', scale_factor = scale_factor, dev = dev)
    elevator_scene = ElevatorScene(doctor, cursor, collision_file = 'scenes/elevator/collision.pickle', scale_factor = scale_factor, dev = dev)
    bathroom = Bathroom(doctor, cursor, scale_factor = scale_factor, collision_file = 'scenes/bathroom/collision.pickle', dev = dev, config = config)
    overlay = Overlay(doctor, cursor, scale_factor = scale_factor, dev = dev)

    # init scene handler
    scene_handler = sc.SceneHandler([scene1, elevator_scene, bathroom, 
                                     start_screen, load_game],
                                     doctor, overlay)


    # whatever that is
    if dev: 
        bathroom.draw_bg(screen)
        scene_handler.scene = bathroom

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

            if dev and event.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                print('recording poitn: ', mpos)
                p1.append(mpos[0])
                p2.append(mpos[1])

            if event.type == pg.KEYDOWN:


                if event.key == pg.K_q and dev:
                    print("recording collisions to: ", str(sys.argv[2]))
                    util.record_collision_points(p1, p2, scale_factor, screen, str(sys.argv[2]))

                elif event.key == pg.K_e:
                    if overlay.hide:
                        overlay.hide = False
                    else:
                        overlay.hide = True

            if event.type == pg.QUIT:
                running = False
            
        
        # draw rect on screen
        #pg.draw.rect(screen, (255,255,255), (((10, 700, 400, 180))))
        
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