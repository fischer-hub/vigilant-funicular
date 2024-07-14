import pygame as pg
from src.animate import StripAnimate
import pickle


class SceneHandler():
    def __init__(self, scene_lst, player):

        self.scene_lst = scene_lst
        self.scene = self.scene_lst[0]
        self.player = player
        self.player.collision_lst = self.scene.collision_lst
        self.scene_idx = 0

    def change_scene(self, scene_idx):
        
        # TODO: draw transition between scene change here before chaning actually

        # real scene index, save in case we come back after moving
        if scene_idx >= 0:
            self.scene_idx = scene_idx

        # we stopped moving to destination, ready for next scnene
        if not self.player.moving:
            print('Changing to scene: ', self.scene_idx)
            self.scene = self.scene_lst[scene_idx]
            self.player.rect[0] = self.player.destination_pos[0] = self.scene.player_spawn[0]
            self.player.rect[1] = self.player.destination_pos[1] = self.scene.player_spawn[1]
            self.player.collision_lst = self.scene.collision_lst

        # we are still walking, send userevent to check in a few seconds again
        else:
            pg.time.set_timer(event = pg.USEREVENT + 1, millis = 50, loops = 1)


    def handle_event(self, event):
        event_response = self.scene.handle_event(event)

        if event_response is not None:
            self.change_scene(event_response)
    
    def draw_bg(self, surface):
        self.scene.draw_bg(surface)

    def draw_fg(self, surface):
        self.scene.draw_fg(surface)


class Scene():
    def __init__(self, player, cursor, background_lst, foreground_lst, collision_file = None, scale_factor = 6, dev = False):

        self.bg_lst = [layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(layer).convert_alpha(), scale_factor) for layer in background_lst]
        self.fg_lst = [layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(layer).convert_alpha(), scale_factor) for layer in foreground_lst]

        self.show_collision = False
        self.clickable_lst = []
        self.last_clickable_idx = None

        self.player = player
        self.player_spawn = (960, 520)

        if not dev and collision_file:
            with open((collision_file), "rb") as fn: 
                self.collision_lst = pickle.load(fn)

                # scale collision values to resolution
                self.collision_lst = self.collision_lst[::(7 - scale_factor)]
        elif not collision_file:
            print('No collision file defined for this scene, initializing collision values to upper screen bound 0.')
            self.collision_lst = [0] * 8000
        else:
            print('Running in dev mode, set collision values to 0.')
            self.collision_lst = [0] * 8000

        self.player.collision_lst = self.collision_lst
        self.cursor = cursor
            

    def draw_bg(self, surface):
        for layer in self.bg_lst:
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))
                    

    def draw_fg(self, surface):
        
        if self.show_collision:
            for i in range(len(self.collision_lst)):
                surface.set_at((i, self.collision_lst[i]), "red")

        for layer in self.fg_lst:
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))

    def handle_event(self, event):

        """Handle event specific to scnene, return index of scnene to change to in scene_lst if change event is triggered."""
        
        for obj in self.clickable_lst:
            if obj.rect.collidepoint(pg.mouse.get_pos()):
                self.cursor.change_cursor(obj.hover_cursor)
            else:
                self.cursor.change_cursor(0)

            
            if event.type == pg.MOUSEBUTTONUP and obj.rect.collidepoint(event.pos):
                return obj.on_click()
                
        # come back from waiting on moving player to scene change
        if event.type == pg.USEREVENT + 1:
            # trigger scene change in scene handler onto last scene index
            return -1
        
        elif event.type == pg.USEREVENT + 2:
            # trigger scene change in scene handler onto last scene index
            self.clickable_lst[self.last_clickable_idx].on_click()
        


class Clickable():
    def __init__(self, rect, animation = None, hover_cursor = 0):
        self.rect = rect
        self.animation = animation
        self.hover_cursor = hover_cursor

    def on_click(self):
        print(f"Clickable does not implement own on_click() method. Clicked on object at {self.rect.topleft}")


class ChangeScene(Clickable):
    def __init__(self, rect, next_scene_idx, animation=None, hover_cursor = 0):
        super().__init__(rect, animation, hover_cursor)
        self.next_scene_idx = next_scene_idx

    def on_click(self):
        print('change scene triggered')
        return self.next_scene_idx
    