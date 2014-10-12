import math
import time
import pygame

from weapons import *

# taken from https://github.com/Mekire/meks-pygame-samples/blob/master/eight_dir_movement_adjusted.py
DIRECT_DICT = {pygame.K_LEFT  : (-1, 0),
               pygame.K_RIGHT : ( 1, 0),
               pygame.K_UP    : ( 0,-1),
               pygame.K_DOWN  : ( 0, 1)}

#X and Y Component magnitude when moving at 45 degree angles
ANGLE_UNIT_SPEED = math.sqrt(2)/2

class Player(pygame.sprite.Sprite):


    def __init__(self, ctrl):
        super(Player, self).__init__()
        self.ctrl = ctrl
        self.image = self.ctrl.frames['hero/normal']
        self.walk_frames = [
            self.ctrl.frames['hero/walk-0'],
            self.ctrl.frames['hero/walk-1'],
            self.ctrl.frames['hero/walk-2'],
            self.ctrl.frames['hero/walk-3'],
        ]
        self.rect = self.image.get_rect()

        self.runing = False
        self.orientation = 'ltr'
        

        self.rect.height = 8
        self.rect.top += 56
        self.rect.center = (200, 120)

         # movement base on Mekire's samples
        self.move = list(self.rect.center)
        self.old_move = self.move
        self.speed = 150
        self.vector = [0, 0]

        self.curr_frame = 0

        self.animate_timer = 0.0
        self.animate_fps = 15.0

        self.weapon = Ak47(self.ctrl,  self.rect.left, self.rect.top)

    def get_frame(self, frames):
        if self.curr_frame  < len(frames) - 1:
            self.curr_frame += 1
        else:
            self.curr_frame = 0

        return self.curr_frame


    def collide(self, level, delta, index):
        rect = level.tile_rect
        for y in xrange(level.view_y1, level.view_y2):
            for x in xrange(level.view_x1, level.view_x2):
                rect.x = x*level.tw
                rect.y =  y*level.th
                tile = level.get_tile_image(x, y, level.collition_layer)
                if tile != 0:
                    if self.rect.colliderect(rect):
                        self.move[index] -= delta
                        self.rect.center = self.move


                        


    def handle_events(self, keys):
        self.runing = False
        self.y_direction = None

        if keys[pygame.K_RIGHT]:
            self.runing = True
            self.orientation = 'ltr'

        if keys[pygame.K_LEFT]:
            self.runing = True
            self.orientation = 'rtl'

        if keys[pygame.K_UP]:
            self.runing = True

        if keys[pygame.K_DOWN]:
            self.runing = True


        if keys[pygame.K_d]:
            self.weapon.generate_bullet()

    def update(self, keys, level):
        # movement base on Mekire's samples
        self.vector = [0, 0]
        for key in DIRECT_DICT:
            if keys[key]:
                self.vector[0] += DIRECT_DICT[key][0]
                self.vector[1] += DIRECT_DICT[key][1]
        factor = (ANGLE_UNIT_SPEED if all(self.vector) else 1)
        frame_speed = self.speed*factor*self.ctrl.td
        self.move[0] += self.vector[0]*frame_speed
        self.move[1] += self.vector[1]*frame_speed
        self.rect.center = self.move
        self.old_move = self.move
        self.collide(level, self.vector[0]*frame_speed, 0)
        self.collide(level, self.vector[1]*frame_speed, 1)

        now = pygame.time.get_ticks()
        if now-self.animate_timer > 1000/self.animate_fps:
            if self.runing:
                frame = self.get_frame(self.walk_frames)
                if self.orientation == 'ltr':
                    self.image = self.walk_frames[frame]
                else:
                    self.image = pygame.transform.flip(self.walk_frames[frame],1,0)

            else:
                frame = self.ctrl.frames['hero/normal']
                if self.orientation == 'ltr':
                    self.image = frame
                else:
                    self.image = pygame.transform.flip(frame,1,0)

            self.animate_timer = now
        
        self.weapon.update(self.rect, self.orientation)



    def render(self, screen, camera):        
        screen.blit(self.image, (self.rect.left - camera.left,
                                 self.rect.top - 56 - camera.top))
        self.weapon.render(screen, camera)