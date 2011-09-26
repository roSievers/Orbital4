"""This Module provides the basic Tile classes.
For convenience, moving blocks are tiles, too"""
        
from pygame import draw, Rect
        
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
    def draw(self, target, pxCellSize):
        draw.rect(target, (200, 200, 200), self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)

class Null(Tile):
    def draw(self, target, pxCellSize):
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize) )

class Static(Tile):
    def draw(self, target, pxCellSize):
        draw.rect(target, (100, 100, 100), self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)

# Input Slot

class Slot(DirectedTile):
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

class Pusher(DirectedTile):
    def __init__(self, x, y, direction, color):
        DirectedTile.__init__(self, x, y, direction)
        self.color = color
    def draw(self, target, pxCellSize):
        draw.rect(target, self.color, self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)
    def trigger(self, block):
        block.direction = self.direction
    
def PushUp(x, y):
    return Pusher(x, y, (0, -1), (0, 150, 0))

def PushLeft(x, y):
    return Pusher(x, y, (-1, 0), (0, 150, 0))

def PushDown(x, y):
    return Pusher(x, y, (0, 1), (0, 150, 0))

def PushRight(x, y):
    return Pusher(x, y, (1, 0), (0, 150, 0))

# Mirror Tile

class Mirror(TriggerTile):
    def __init__(self, x, y):
        TriggerTile.__init__(self, x, y)
    def draw(self, target, pxCellSize):
        draw.rect(target, (255, 200, 200), self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)
    def trigger(self, block):
        block.direction = (-block.direction[0], -block.direction[1])
        
# Delete Tile

class Delete(TriggerTile):
    def __init__(self, x, y):
        TriggerTile.__init__(self, x, y)
    def draw(self, target, pxCellSize):
        draw.rect(target, (0, 40, 0), self.pxRect(pxCellSize) )
        draw.rect(target, (0, 0, 0), self.pxRect(pxCellSize), 1)
    def trigger(self, block):
        block.kill()