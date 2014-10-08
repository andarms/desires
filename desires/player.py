import time
import pygame


class Player(pygame.sprite.Sprite):


    def __init__(self, ctrl):
        super(Player, self).__init__()
        self.ctrl = ctrl
        self.image = self.ctrl.frames['hero/normal']
        self.walk_frames = [
            self.ctrl.frames['hero/walk-0'],
            self.ctrl.frames['hero/walk-1']
        ]
        self.rect = self.image.get_rect()

        self.speed = .50
        self.vx = 0
        self.vy = 0

        self.runing = False
        self.x_direction = 'ltr'
        self.y_direction = None

        self.rect.center = (200,220)

        self.curr_frame = 0

        self.anim_vel = 100
        self.start_time = 0

    def get_frame(self, frames):
        if self.curr_frame  < len(frames) - 1:
            self.curr_frame += 1
        else:
            self.curr_frame = 0

        return self.curr_frame

    def handle_events(self, key):
        self.runing = False
        self.y_direction = None

        if key[pygame.K_RIGHT]:
            self.runing = True
            self.x_direction = 'ltr'

        if key[pygame.K_LEFT]:
            self.runing = True
            self.x_direction = 'rtl'

        if key[pygame.K_UP]:
            self.runing = True
            self.y_direction = 'utd'

        if key[pygame.K_DOWN]:
            self.runing = True
            self.y_direction = 'dtu'


    def update(self):
        time = pygame.time.get_ticks()
        if time - self.start_time > self.anim_vel:
            self.start_time = time

            if self.runing:
                frame = self.get_frame(self.walk_frames)
                if self.x_direction == 'ltr':
                    self.vx += self.speed
                    self.image = self.walk_frames[frame]
                else:
                    self.vx -= self.speed
                    self.image = pygame.transform.flip(self.walk_frames[frame],1,0)

                if self.y_direction is not None:
                    if self.y_direction == 'utd':
                        self.vy -= self.speed
                    else:            
                        self.vy += self.speed
            else:
                self.vx = 0
                self.vy = 0

            self.rect.left += self.vx
            self.rect.top += self.vy


    def render(self, screen):        
        screen.blit(self.image, self.rect)