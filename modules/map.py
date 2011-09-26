"""This Module implements a Map class that stores all information about the map's state"""

from tile import Empty, Null, Slot, Static, PushUp, PushLeft, PushDown, PushRight
from math import XYMap
from pygame import sprite

settings = {
'.' : Empty,
'x' : Static,
'u' : PushUp,
'l' : PushLeft,
'd' : PushDown,
'r' : PushRight
}

class World(sprite.Group):
	def __init__(self, data):
		object.__init__(self)
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
	def __call__(self, x, y):
		return self.map(x, y)

	def getCSI(self, target):
		return min(target.get_width() / (self.map.width), target.get_height() / (self.map.height))

	def draw(self, target):
		CSI = self.getCSI(target)
		for x in xrange(self.map.width):
			for y in range(self.map.height):
				self.map(x, y).draw(target, CSI)

	def px2cord(self, target, x, y):
		CSI = self.getCSI(target)
		return x / CSI, y / CSI
