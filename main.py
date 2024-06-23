# Example file showing a circle moving on screen
import pygame as pg
import lib.animate as am




def main():
        

    # pg setup
    pg.init()
    screen = pg.display.set_mode((320 * 6, 180 *6))
    clock = pg.time.Clock()
    running = True
    dt = 0

    player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    # initial position for sprite top left corner
    pos = (500, 500)
    doctor_idle = am.Player('sprites/dr_idle.png', pos = pos)
    doctor_walk = am.StripAnimate('sprites/dr_walk.png', frame_rate = 5)
    my_group = pg.sprite.Group(doctor_idle, doctor_walk)

    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close your window
        for event in pg.event.get():

            # handle MOUSEBUTTONUP
            if event.type == pg.MOUSEBUTTONUP:
                 mpos = pg.mouse.get_pos()
                 doctor_idle.update_pos(mpos)
                 print(mpos)
            if event.type == pg.QUIT:
                running = False

        # display background
        screen.blit(pg.transform.scale_by(pg.image.load('sprites/bg1.png').convert_alpha(), 6), (0,0))

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player_pos.y -= 300 * dt
        if keys[pg.K_s]:
            player_pos.y += 300 * dt
        if keys[pg.K_a]:
            player_pos.x -= 300 * dt
        if keys[pg.K_d]:
            player_pos.x += 300 * dt


        # Calling the 'my_group.update' function calls the 'update' function of all 
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        my_group.update()
        my_group.draw(screen)

        # load and display foreground
        screen.blit(pg.transform.scale_by(pg.image.load('sprites/fg1.png').convert_alpha(), 6), (0,0))


        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pg.quit()

if __name__ == '__main__':
    main()