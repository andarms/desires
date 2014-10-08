import sys
import pygame

import data
from .scene import TestScene, SplashScene
from loader import Loader

# global FRAMES = {}

class Control():
    def __init__(self):
        self.screen_size = (640,480)
        self.flags = pygame.DOUBLEBUF|pygame.HWSURFACE
        self._screen = pygame.display.set_mode(self.screen_size, self.flags)
        self.screen = self._screen.convert().subsurface(0,0,320,240)
        
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.scene = None

        self.frames = {}
        self.sounds = {}

        self.loader = Loader()
        self.loader.image2load = 'sprite_sheet.png'
        self.loader.json_file = data.filepath('sprites.json')
        self.loader.sounds2load = [
            'DST-Defunkt.ogg',
            'menu.wav',
        ]


        self.loader.start()
        self.music = pygame.mixer.Channel(3)
        self.sfx = pygame.mixer.Channel(4)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()

            self.scene.handle_events()
            self.scene.update()
            self.scene.render(self.screen)

            caption = "{} - FPS: {:.2f}".format('Desires', self.clock.get_fps())
            pygame.display.set_caption(caption)

            tmp = pygame.transform.scale(self.screen, self.screen_size)
            self._screen.blit(tmp, (0,0))

            pygame.display.update()
            self.clock.tick(self.fps)

            

    def change_scene(self, scene):
        self.scene = scene


    def quit(self):
        pygame.quit()
        sys.exit()



def main():
    ctrl = Control()
    scene = SplashScene(ctrl)
    ctrl.change_scene(scene)
    ctrl.loop()
