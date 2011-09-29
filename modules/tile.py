"""This Module provides the basic Tile classes.
For convenience, moving blocks are tiles, too"""
        
from pygame import draw, Rect, image
from recolor import compileSVASheet
from spriteSheet import CachedResizeSheet

dir2uldr = {
(0, -1) : 0,
(-1, 0) : 1,
(0, 1)  : 2,
(1, 0)  : 3,
(0, 0)  : 4
}
        
class Tile(object):
    __slots__ = ["x", "y"]
    def __init__(self, x, y):
        object.__init__(self)
        self.x, self.y = x, y
    def _getTuple(self):
        return (self.x, self.y)
    pos = property(_getTuple)
    def pxPos(self, pxCellSize):
        return self.x*pxCellSize, self.y*pxCellSize
    def pxRect(self, pxCellSize):
        return Rect(self.pxPos(pxCellSize),(pxCellSize, pxCellSize))
        
class TriggerTile(Tile):
    __slots__ = []
    """Abstract base class for all tile which modify blocks."""
    def trigger(self, block):
        pass
        
class DirectedTile(TriggerTile):
    """Directed tiles without a trigger seem kinda pointless, thus they inherit from TriggerTile"""
    __slots__ = ["direction"]
    def __init__(self, x, y, direction):
        TriggerTile.__init__(self, x, y)
        self.direction = direction

# Very Basic Tiles
        
class Empty(Tile):
    __slots__ = []
    def draw(self, target, pxCellSize):
        draw.rect(target, (200, 200, 200), self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)

class Null(Tile):
    __slots__ = []
    def draw(self, target, pxCellSize):
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize) )

class Static(Tile):
    __slots__ = []
    def draw(self, target, pxCellSize):
        draw.rect(target, (100, 100, 100), self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)

# Input Slot

class Slot(DirectedTile):
    __slots__ = []
    def draw(self, target, pxCellSize):
        draw.rect(target, (100, 100, 200), self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)
    def trigger(self, block):
        if block.direction[0] == -self.direction[0]:
            if block.direction[1] == -self.direction[1]:
                block.kill()
                return
        block.direction = self.direction
        
# Redirection Tiles

imgPusher = CachedResizeSheet(compileSVASheet(image.load("data/images/pusher.png"), (0, 150, 0)), 4)

print imgPusher.sprites.data

class Pusher(DirectedTile):
    __slots__ = ["color"]
    def __init__(self, x, y, direction):
        DirectedTile.__init__(self, x, y, direction)
    def draw(self, target, pxCellSize):
        rect = self.pxRect(pxCellSize)
        draw.rect(target, (200, 200, 200), rect )
        draw.rect(target, (0, 0, 0), rect, 1)
        target.blit(imgPusher(dir2uldr[self.direction], 0, rect.w, rect.h), (rect.x, rect.y))
    def trigger(self, block):
        block.direction = self.direction
    
def PushUp(x, y):
    return Pusher(x, y, (0, -1))

def PushLeft(x, y):
    return Pusher(x, y, (-1, 0))

def PushDown(x, y):
    return Pusher(x, y, (0, 1))

def PushRight(x, y):
    return Pusher(x, y, (1, 0))

# Freeze Tile

imgFreeze = CachedResizeSheet(compileSVASheet(image.load("data/images/frost.png"), (100, 100, 255)), 1)

class Freeze(TriggerTile):
    __slots__ = []
    def __init__(self, x, y):
        TriggerTile.__init__(self, x, y)
    def draw(self, target, pxCellSize):
        rect = self.pxRect(pxCellSize)
        draw.rect(target, (200, 200, 200), rect )
        target.blit(imgFreeze(0, 0, rect.w, rect.h), (rect.x, rect.y))
        draw.rect(target, (0, 0, 0), rect, 1)
    def trigger(self, block):
        block.direction = (0, 0)

# Mirror Tile

class Mirror(TriggerTile):
    __slots__ = []
    def __init__(self, x, y):
        TriggerTile.__init__(self, x, y)
    def draw(self, target, pxCellSize):
        draw.rect(target, (255, 180, 180), self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)
    def trigger(self, block):
        block.direction = (-block.direction[0], -block.direction[1])
        
# Delete Tile

imgDelete = CachedResizeSheet(compileSVASheet(image.load("data/images/delete.png"), (255, 0, 0)), 1)

class Delete(TriggerTile):
    __slots__ = []
    def __init__(self, x, y):
        TriggerTile.__init__(self, x, y)
    def draw(self, target, pxCellSize):
        rect = self.pxRect(pxCellSize)
        draw.rect(target, (200, 200, 200), rect )
        target.blit(imgDelete(0, 0, rect.w, rect.h), (rect.x, rect.y))
        draw.rect(target, (0, 0, 0), rect, 1)
    def trigger(self, block):
        block.kill()
        
# Delay Tile

imgDelay = CachedResizeSheet(compileSVASheet(image.load("data/images/delay.png"), (200, 0, 200)), 1)
imgDelayContent = image.load("data/images/arrow.png")

class Delay(TriggerTile):
    __slots__ = ["last", "lastDirection", "iArrow"]
    def __init__(self, x, y):
        TriggerTile.__init__(self, x, y)
        self.last = None
        self.lastDirection = None
        self.iArrow = None
    def draw(self, target, pxCellSize):
        rect = self.pxRect(pxCellSize)
        draw.rect(target, (200, 200, 200), rect )
        target.blit(imgDelay(0, 0, rect.w, rect.h), (rect.x, rect.y))
        if self.iArrow is not None:
            target.blit(self.iArrow(dir2uldr[self.last.direction], 0, rect.w, rect.h), (rect.x, rect.y))
        draw.rect(target, (0, 0, 0), rect, 1)
    def trigger(self, block):
        block.kill()
        if self.last is not None:
            block.world.registerBlock(self.last)
            self.last.direction = self.lastDirection
            
        self.lastDirection = block.direction
        self.last = block
        self.iArrow = CachedResizeSheet(compileSVASheet(imgDelayContent, block.player.color), 5)