# Example file showing a circle moving on screen
import pygame as pg
import src.animate as am




def main():
        

    # pg setup
    pg.init()
    screen = pg.display.set_mode((1920, 1080))
    clock = pg.time.Clock()
    running = True
    dt = 0

    player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    doctor = am.StripAnimate('sprites/dr_idle.png')
    #my_group = pg.sprite.Group(my_sprite)

    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

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
        #my_group.update()
        doctor.update()
        doctor.draw(screen)

        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pg.quit()

if __name__ == '__main__':
    main()