import pygame as pg
from src.animate import StripAnimate
import pickle
from lib.helper import path


class SceneHandler():
    def __init__(self, scene_lst, player, overlay):

        self.scene_lst = scene_lst
        self.scene = self.scene_lst[3]
        self.player = player
        self.player.collision_lst = self.scene.collision_lst
        self.scene_idx = 3
        self.overlay = overlay

    def change_scene(self, scene_idx):
        
        # TODO: draw transition between scene change here before chaning actually

        # real scene index, save in case we come back after moving
        if scene_idx >= 0:
            self.scene_idx = scene_idx

        # we stopped moving to destination, ready for next scnene
        #if not self.player.moving:
        if True:
            print('Changing to scene: ', self.scene_idx)
            [sound.stop() for sound in self.scene.sound_lst]
            self.scene = self.scene_lst[self.scene_idx]
            self.player.rect[0] = self.scene.player_spawn[0]
            self.player.rect[1] = self.scene.player_spawn[1]
            self.player.destination_pos = self.scene.player_spawn
            self.player.collision_lst = self.scene.collision_lst
            
            for sound in self.scene.sound_lst: 
                sound.stop()
                sound.play(-1)

        # we are still walking, send userevent to check in a few seconds again
        else:
            pg.time.set_timer(event = pg.USEREVENT + 1, millis = 50, loops = 1)


    def handle_event(self, event):
        event_response = None

        if not self.overlay.hide: 
            self.overlay.handle_event(event)
        else:
            event_response = self.scene.handle_event(event)

                   # handle MOUSEBUTTONUP
        if event.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                print('mpos is ', mpos)
                
                if not self.player.talking and self.overlay.hide and event_response != 42 and not self.scene.id == 3:
                
                    self.player.move_to(mpos)

                # maybe put this in an extra fct at some point
                #if dev:
                 #   p1.append(mpos[0])
                   # p2.append(mpos[1])


        if event_response is not None and event_response != 42:
            self.change_scene(event_response)
    
    def draw_bg(self, surface):
        self.scene.draw_bg(surface)

    def draw_fg(self, surface):
        self.scene.draw_fg(surface)

        if not self.overlay.hide:
            self.overlay.draw_bg(surface)



class Scene():
    def __init__(self, player, cursor, collision_file = None, scale_factor = 6, dev = False):

        #self.bg_lst = [layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor) for layer in background_lst]
        #self.fg_lst = [layer if type(layer) is StripAnimate else pg.transform.scale_by(pg.image.load(path(layer)).convert_alpha(), scale_factor) for layer in foreground_lst]

        self.show_collision = False
        self.clickable_lst = {}
        self.bg_lst = {}
        self.fg_lst = {}
        self.last_clickable_idx = None
        self.scale_factor = scale_factor
        self.sound_lst = []

        self.player = player
        self.player_spawn = (960, 520)


        if not dev and collision_file:
            with open(path(collision_file), "rb") as fn: 
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
        for layer in self.bg_lst.values():
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))
                    

    def draw_fg(self, surface):
        
        if self.show_collision:
            for i in range(len(self.collision_lst)):
                surface.set_at((i, self.collision_lst[i]), "red")

        for layer in self.fg_lst.values():
            if type(layer) is StripAnimate:
                layer.update()
                layer.draw(surface)
            else:
                surface.blit(layer, (0, 0))


    def handle_event(self, event):

        """Handle event specific to scene, return index of scnene to change to in scene_lst if change event is triggered."""
        
        # set cursor to default img, when no clickable is hovered, we just leave it, this ensures the cursor defaults when we stop hovering
        self.cursor.change_cursor(0)   
        
        if event.type == pg.MOUSEBUTTONUP and self.cursor.item:
            self.cursor.cursor_img = self.cursor.cursor_img_default

            # do this when consuming /using an item
            #self.player.inventory.remove(self.cursor.item)     
            self.cursor.item = ''
        
        for obj in self.clickable_lst.values():
            scaled_rect = pg.Rect(tuple(int(value * (self.scale_factor / 6)) for value in obj.rect))
            if scaled_rect.collidepoint(pg.mouse.get_pos()):
                self.cursor.change_cursor(obj.hover_cursor)

            
            if event.type == pg.MOUSEBUTTONUP and scaled_rect.collidepoint(event.pos):
                return obj.on_click()
        

        # come back from waiting on moving player to scene change
        if event.type == pg.USEREVENT + 1:
            # trigger scene change in scene handler onto last scene index
            return -1
        
        elif event.type == pg.USEREVENT + 2:
            # i forgot what this does but I think it retriggers a clickable that we walk to, maybe replace that with the new move_to() function feature
            self.clickable_lst[self.last_clickable_idx].on_click()
        
        elif event.type == pg.USEREVENT + 3:
            # trigger end of talking animation
            self.player.rect = self.player.current_animation.rect
            self.player.current_animation = self.player.animation_lst[0]
            self.player.current_animation.rect = self.player.rect
            self.player.talking = False
            print('talking ends')
        
        elif event.type == pg.USEREVENT + 4:
            # trigger start of talking animation after crouching
            if self.player.talking:
                self.player.rect = self.player.current_animation.rect
                self.player.current_animation = self.player.animation_lst[2]
                self.player.current_animation.rect = self.player.rect
                self.player.talking = True


class Clickable():
    def __init__(self, rect, animation = None, hover_cursor = 0, sound_lst = None):
        self.rect = rect
        self.animation = animation
        self.hover_cursor = hover_cursor
        self.sound_lst = sound_lst

    def on_click(self):
        print(f"Clickable does not implement own on_click() method. Clicked on object at {self.rect.topleft}")


class ChangeScene(Clickable):
    def __init__(self, rect, next_scene_idx, animation=None, hover_cursor = 0):
        super().__init__(rect, animation, hover_cursor)
        self.next_scene_idx = next_scene_idx

    def on_click(self):
        print('change scene triggered')
        return self.next_scene_idx
    

class Commentable(Clickable):
    '''A class implementing a clickable object that triggers the main player talk function, given a sound (comment) to play at the same time.'''
    def __init__(self, rect, player, animation=None, hover_cursor = 2, sound_lst=None):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.player = player
    
    def on_click(self):
        self.player.talk(self.sound_lst)
        return None
    

class Collectable(Clickable):
    def __init__(self, rect, player, sound_lst, scene, list_name, item_id_lst, animation=None, hover_cursor = 1):
        super().__init__(rect, animation, hover_cursor, sound_lst)
        self.player = player
        self.scene = scene
        self.collected = False
        self.list_name = list_name
        self.grab_sound = pg.mixer.Sound(path('sounds', 'characters', 'dr', 'grab.ogg'))
        self.item_id_lst = item_id_lst
        self.sound_lst = sound_lst
    
    def collect(self):
        self.player.crouch()
        self.collected = True
        self.scene.bg_lst.pop(self.list_name)
        self.scene.clickable_lst.pop(self.list_name)
        self.grab_sound.play(maxtime = 1000)
        [self.player.inventory.append(item) for item in self.item_id_lst]

    def on_click(self):
        if not self.collected:
            self.player.talk(self.sound_lst[0])
            self.player.move_to(pg.mouse.get_pos(), self.collect)
