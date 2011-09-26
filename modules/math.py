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