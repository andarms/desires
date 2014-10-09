import pygame

class Bullet(pygame.Rect):
    def __init__(self, (x, y), w, h, target):
        super(Bullet, self).__init__(x, y, w, h)
        self.tx, self.ty = target

        self.x_opration = '+'
        if self.x < self.left:
            self.x_opration = '-'

        self.y_opration = '+'
        if self.x < self.top:
            self.y_opration = '-'

        self.speed = 5

    def update(self):
        if self.x_opration == '+' and self.left != self.tx:
            self.left += self.speed
        else:
            self.left += self.speed

        if self.y_opration == '+' and self.top != self.ty:
            self.top += self.speed
        else:
            self.top += self.speed

        if self.tx == self.left and self.ty == self.top:
            del(self)


    def render(self, screen):
        pygame.draw.rect(screen, (255,0,0), self)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, ctrl):
        super(Weapon, self).__init__()
        self.ctrl = ctrl
        self.relative_y = None
        self.bullets = []

    def generate_bullet(self):
        b = Bullet(self.rect.center, 1,1, (100,100))
        self.bullets.append(b)

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

        for bullet in self.bullets:
            bullet.update()

    def render(self, screen):
        screen.blit(self.image, self.rect)

        for bullet in self.bullets:
            bullet.update()


class Ak47(Weapon):
    def __init__(self, ctrl, x, y):
        super(Ak47, self).__init__(ctrl)
        self.normal = self.ctrl.frames['weapons/ak47']
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.relative_y = 24
        self.rect.left = x
        self.rect.top = self.relative_y + y


class Hkg36(Weapon):
    def __init__(self, ctrl, x, y):
        super(Hkg36, self).__init__(ctrl)
        self.normal = self.ctrl.frames['weapons/hkg36']
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.relative_y = 24
        self.rect.left = x
        self.rect.top = self.relative_y + y


class Shotgun(Weapon):
    def __init__(self, ctrl, x, y):
        super(Shotgun, self).__init__(ctrl)
        self.normal = self.ctrl.frames['weapons/shotgun']
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.relative_y = 24
        self.rect.left = x
        self.rect.top = self.relative_y + y

class Flamethrower(Weapon):
    def __init__(self, ctrl, x, y):
        super(Flamethrower, self).__init__(ctrl)
        self.normal = self.ctrl.frames['weapons/flamethrower']
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.relative_y = 16
        self.rect.left = x
        self.rect.top = self.relative_y + y


class Chainsaw(Weapon):
    def __init__(self, ctrl, x, y):
        super(Chainsaw, self).__init__(ctrl)
        self.normal = self.ctrl.frames['weapons/chainsaw-0']
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.relative_y = 24
        self.rect.left = x
        self.rect.top = self.relative_y + y

        self.curr_frame = 0


