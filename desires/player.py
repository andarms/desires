import pygame

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

class Player(pygame.sprite.Sprite):


    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()

        self.speed = 5
        self.vx = 0
        self.vy = 0

        self.runing = False
        self.direction = LEFT

        self.rect.center = (200,220)

        self.image.fill((255, 0, 0))

    def handle_events(self, key):

        if key[pygame.K_RIGHT]:
            self.runing = True
            self.direction = RIGHT

        if key[pygame.K_UP]:
            self.runing = True
            self.direction = UP

        if key[pygame.K_DOWN]:
            self.runing = True
            self.direction = DOWN

        if key[pygame.K_LEFT]:
            self.runing = True
            self.direction = LEFT

    def update(self):
        if self.runing:
            if self.direction == RIGHT:
                self.vx += self.speed
            elif self.direction == LEFT:
                self.vx -= self.speed
            elif self.direction == UP:
                self.vy -= self.speed
            elif self.direction == DOWN:
                self.vy += self.speed
        else:
            self.vx = 0
            self.vy = 0

        self.rect.left += self.vx
        self.rect.top += self.vy

        self.runing = False

    def render(self, screen):        
        screen.blit(self.image, self.rect)