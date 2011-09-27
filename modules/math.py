"""Collection of mathematical helper functions."""

class XYMap():
    __slots__ = ["width", "height", "data"]
    def __init__(self, function, width, height):
        self.width  = width
        self.height = height
        
        self.data = [[function(x, y) for y in xrange(self.height)] for x in xrange(self.width)]
        
    def __call__(self, x, y):
        try:
            return self.data[x][y]
        except IndexError:
            return None
        
    def set(self, x, y, value):
        self.data[x][y] = value
        
class CentralCurry(object):
    def __init__(self, function, head=(), tail=()):
        self.function = function
        self.head = head
        self.tail = tail
    def __call__(self, *arg):
        args = list(self.head)
        args.extend(list(arg))
        args.extend(list(self.tail))
        
        return self.function(*tuple(args))