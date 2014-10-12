import random

import pygame
import util as u
import solver

class EnemyCtrl(object):
    def __init__(self, ctrl, game):
        self.ctrl = ctrl

        self.curr_enemies = 0
        self.max_enemies = 10
        self.player_kills = 0
        self.game = game

        self.done = False
        self.ticks = 0

    def update(self):
        if self.curr_enemies <= self.max_enemies:
            z = Zombie(self.ctrl, self.game)
            self.game.entities.append(z)
            self.curr_enemies += 1


        target = self.game.player.rect.center
        if self.ticks > 50:
            for e in self.game.entities:
                e.target = target
            self.ticks = 0

        self.ticks +=  1




class Enemy(pygame.sprite.Sprite):
    def __init__(self, ctrl):
        super(Enemy, self).__init__()
        self.ctrl = ctrl
        self.moving = False
        self.move = [0,0]

        self.orientation = 'ltr'
        self.animate_timer = 0.0
        self.animate_fps = 5.0

        self.health = 100

        

    def get_frame(self, frames):
        if self.curr_frame  < len(frames) - 1:
            self.curr_frame += 1
        else:
            self.curr_frame = 0

        return self.curr_frame

    def update(self):
            
        now = pygame.time.get_ticks()
        if now-self.animate_timer > 1000/self.animate_fps:
            if self.moving:
                if self.target[0] > self.rect.centerx:
                    self.move[0] += self.speed
                    self.orientation = 'ltr'
                    if self.move[0] > self.target[0]:
                        self.move[0] = self.target[0]

                elif self.target[0] < self.rect.centerx:
                    self.move[0] -= self.speed
                    self.orientation = 'rtl'
                    if self.move[0] < self.target[0]:
                        self.move[0] = self.target[0] 

                if self.target[1] > self.rect.centery:
                    self.move[1] += self.speed
                    if self.move[1] > self.target[1]:
                        self.move[1] = self.target[1] 
                elif self.target[1] < self.rect.centery:
                    self.move[1] -= self.speed
                    if self.move[1] < self.target[1]:
                        self.move[1] = self.target[1]

                self.rect.center = self.move


                frame = self.get_frame(self.walk_frames)
                if self.orientation == 'ltr':
                    self.image = self.walk_frames[frame]
                else:
                    self.image = pygame.transform.flip(self.walk_frames[frame],1,0)
            else:
                frame = self.normal
                if self.orientation == 'ltr':
                    self.image = frame
                else:
                    self.image = pygame.transform.flip(frame,1,0)

                
                self.target = self.game.player.rect.center
                self.moving = True

            self.animate_timer = now

                



        if self.rect.center == self.target:
                self.moving = False


    def render(self, screen, camera):
        screen.blit(self.image, (self.rect.left - camera.left,
                                 self.rect.top - camera.top))

    


class Zombie(Enemy):
    def __init__(self, ctrl, game):
        super(Zombie, self).__init__(ctrl)

        self.normal = self.ctrl.frames['zombie/normal']
        self.image = self.normal

        self.walk_frames = [
            self.ctrl.frames['zombie/walk-0'],
            self.ctrl.frames['zombie/walk-1']
        ]

        self.curr_frame = 0

        self.game = game

        self.rect = self.image.get_rect()
        x, y = u.get_pixel_coords(random.randint(0, 100), random.randint(0, 100))
        self.rect.center = (x, y)
        self.move = list(self.rect.center)
        self.target = self.game.player.rect.center

        self.moving = True

        self.speed = 5


    