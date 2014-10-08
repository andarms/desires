import time
import pygame

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

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

        self.speed = 5
        self.vx = 0
        self.vy = 0

        self.runing = False
        self.orientation = 'ltr'
        self.direction = LEFT

        self.rect.center = (200,220)

        self.curr_frame = 0

        self.animate_timer = 0.0
        self.animate_fps = 7.0

    def get_frame(self, frames):
        if self.curr_frame  < len(frames) - 1:
            self.curr_frame += 1
        else:
            self.curr_frame = 0

        return self.curr_frame

    def handle_events(self, key):
        self.runing = False
        # self.x_direction = None
        self.y_direction = None

        if key[pygame.K_RIGHT]:
            self.runing = True
            self.orientation = 'ltr'
            self.direction = RIGHT

        if key[pygame.K_LEFT]:
            self.runing = True
            self.orientation = 'rtl'
            self.direction = LEFT

        if key[pygame.K_UP]:
            self.runing = True
            self.direction = UP

        if key[pygame.K_DOWN]:
            self.runing = True
            self.direction = DOWN


    def update(self):
        now = pygame.time.get_ticks()
        if now-self.animate_timer > 1000/self.animate_fps:            

            if self.runing:
                
                if self.direction == RIGHT:
                    self.vx += self.speed
                elif self.direction == LEFT:
                    self.vx -= self.speed                
                elif self.direction == UP:
                    self.vy -= self.speed
                elif self.direction == DOWN:            
                    self.vy += self.speed

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


            self.rect.left += self.vx
            self.rect.top += self.vy

            self.vx = 0
            self.vy = 0

            self.animate_timer = now


    def render(self, screen):        
        screen.blit(self.image, self.rect)