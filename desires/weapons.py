import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, ctrl):
        super(Weapon, self).__init__()
        self.ctrl = ctrl
        self.relative_y = None

    def update(self, p_rect, orientation):
        y = p_rect.top
        y += self.relative_y
        self.rect.top = y
        self.rect.left = p_rect.left

        if orientation == 'ltr':
            self.image = self.normal
        else:
            self.image = pygame.transform.flip(self.normal, 1, 0)
            self.rect.left -= 8 # magic numbers

    def render(self, screen):
        screen.blit(self.image, self.rect)


class Ak47(Weapon):
    def __init__(self, ctrl, x, y):
        super(Ak47, self).__init__(ctrl)
        self.normal = self.ctrl.frames['weapons/ak47']
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.relative_y = 24
        self.rect.left = x
        self.rect.top = self.relative_y + y

