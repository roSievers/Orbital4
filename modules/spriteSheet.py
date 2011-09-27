

from pygame import transform, Rect
from math import XYMap

class CachedResizeSheet(object):
    def __init__(self, spritesheet, size):
        
        if isinstance(size, int):
            size = (size, 1)
        
        self.source = spritesheet
        self.tWidth = self.source.get_width() / size[0]
        self.tHeight = self.source.get_height() / size[1]
        
        
        def subsurface(x, y):
            rect =  Rect((x * self.tWidth, y * self.tHeight), (self.tWidth, self.tHeight))
            return self.source.subsurface(rect)
        self.sprites = XYMap(subsurface, *size)
        
        self.cache = {}
        
    def __call__(self, x, y, w, h):
        if not x in self.cache:
            self.cache[x] = {}
        if not y in self.cache[x]:
            self.cache[x][y] = {}
        if not w in self.cache[x][y]:
            self.cache[x][y][w] = {}
        if not h in self.cache[x][y][w]:
            self.cache[x][y][w][h] = transform.smoothscale(self.sprites(x, y), (w, h))
            
        return self.cache[x][y][w][h]