"""This Module implements a Map class that stores all information about the map's state"""

from tile import Empty, Null, Slot, Static, PushUp, PushLeft, PushDown, PushRight, Mirror, Delete, Delay, Freeze
from math import XYMap
from pygame import sprite

settings = {
'.' : Empty,
'x' : Static,
'u' : PushUp,
'l' : PushLeft,
'd' : PushDown,
'r' : PushRight,
'm' : Mirror,
'b' : Delete,
'w' : Delay,
'f' : Freeze
}

class TargetSet(object):
    __slots__ = ["x", "y", "requests"]
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.requests = []
    def flush(self):
        self.requests = []

class World(sprite.Group):
    def __init__(self, data):
        sprite.Group.__init__(self)
        structure = []
        width = None
        height = 0
        for line in data.split():
            structure.append([settings[c] for c in line])
            height += 1
            if width is not None:
                if width != len(line):
                    raise Exception("Die Karte ist nicht rechteckig!")
            else:
                width = len(line)
            
        def extract(x, y):
            if 1 <= x <= width:
                if 1 <= y <= height:
                    return structure[y-1][x-1](x, y)
                
            if 1 <= x <= width:
                return Slot(x, y, (0, (1 if y == 0 else -1)))
            
            if 1 <= y <= height:
                return Slot(x, y, ((1 if x == 0 else -1), 0))
            
            return Null(x, y)
            
        self.map = XYMap(extract, width+2, height+2)
        
        def null(x, y):
            return None
        self.blocks = XYMap(null, width+2, height+2)
        self.newBlockQuee = []
        
        self.requests = XYMap(TargetSet, width+2, height+2)
    def draw(self, target, time):
        CSI = self.getCSI(target)
        for x in xrange(self.map.width):
            for y in range(self.map.height):
                self.map(x, y).draw(target, CSI)
                
        for block in self:
            block.draw(target, time)
        
    def registerBlock(self, block):
        # FIXME: What if s.th. already is at that position?
        if isinstance(self.map(*block.pos), Slot):
            self.blocks.set(*block.pos, value=block)
            self.add(block)
        else:
            self.newBlockQuee.append(block)
        
    def removeBlock(self, x, y):
        self.blocks.set(x, y, None)
        
    # Small Helpers    
    
    def __call__(self, x, y):
        return self.map(x, y)

    def getCSI(self, target):
        return min(target.get_width() / (self.map.width), target.get_height() / (self.map.height))

    def px2cord(self, target, x, y):
        CSI = self.getCSI(target)
        return x / CSI, y / CSI

    # Game Physics Logic
    
    def move(self, animationDuration):
        for block in self.newBlockQuee:
            self.blocks.set(*block.pos, value=block)
            self.add(block)
        self.newBlockQuee = []
        
        for block in self:
            block.trigger()
            
        for block in self.newBlockQuee:
            self.blocks.set(*block.pos, value=block)
            self.add(block)
        self.newBlockQuee = []
        
        self.makeStatic()
            
        for block in self:
            block.makeRequest(self.requests)
            
        for block in self:
            self.blocks.set(*block.pos, value=None)
            
        for block in self:
            block.move(animationDuration)
            self.blocks.set(*block.pos, value=block)
            
    def makeStatic(self):
        done = False
        while not done:
            done = True
            for block in self:
                block.makeRequest(self.requests)
                
            # stop all blocks that hit s.th. static
            for block in self:
                if block.isStatic:
                    continue
                if isinstance(self(*block.target), Static):
                    block.direction = (0, 0)
                    done = False
                    continue
                if self.blocks(*block.target) is not None:
                    if self.blocks(*block.target).isStatic:
                        block.direction = (0, 0)
                        done = False
                        continue