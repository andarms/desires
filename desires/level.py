import pygame
from pytmx import tmxloader

class Level:
    def __init__(self, filename):
        self.tiledmap = tmxloader.load_pygame(filename, pixelalpha=True)

        self.tw = self.tiledmap.tilewidth
        self.th = self.tiledmap.tileheight
        self.width = self.tiledmap.width
        self.height = self.tiledmap.height
        self.get_tile_image = self.tiledmap.getTileImage
        l = self.tiledmap.getTileLayerByName('collition')
        self.collition_layer = self.tiledmap.tilelayers.index(l)

        self.upper_layer = []
        for layer_name in ('trees', 'shrubs','assets'):
            l = self.tiledmap.getTileLayerByName(layer_name)
            layer = self.tiledmap.tilelayers.index(l)
            self.upper_layer.append(layer)


        self.left_edge = 0
        self.top_edge = 64 # height of player
        self.right_edge = self.tiledmap.width * self.tw
        self.bottom_edge = self.tiledmap.height * self.th

        self.objects =  self.tiledmap.getObjects()


        """
        tiledmap.width and tiledmap.height are int numbers like 70, 80, etc.
        so in the render function i need to know which tiles collides with camera rect,
        i can looking for all the tiles "for x in range(self.width):", 
        but that have a low perfomance. For that reason i calculate a view rect
        which tell me where are the tiles, that i need.
        level.view_x1 = camera.left / level.tw
        level.view_x2 = camera.right / level.tw
        level.view_y1 = camera.top / level.tw
        level.view_y2 = camera.bottom / level.tw
        """
        self.view_x1 = 0
        self.view_x2 = 20
        self.view_y1 = 0
        self.view_y2 = 15


    def render(self, screen,  camera):
        r = pygame.Rect(0,0, self.tw, self.th)
        for layer in self.upper_layer:
            for y in xrange(self.view_y1, self.view_y2):
                for x in xrange(self.view_x1, self.view_x2):
                    r.x = x*self.tw
                    r.y =  y*self.th
                    if camera.colliderect(r):
                        t = self.get_tile_image(x, y, layer)
                        if t != 0:
                            screen.blit(t, 
                                        ((x*self.tw)- camera.left,
                                         (y*self.th)- camera.top))