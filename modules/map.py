"""This Modul implements a Map class that stores all information about the map's state"""

from pygame import draw, image, Rect

class Map(object):
	def __init__(self, data):
		self.structure = []
		self.width = None
		self.height = 0
		for line in data.split():
			self.structure.append([settings[c]() for c in line])
			self.height += 1
			if self.width is not None:
				if self.width != len(line):
					raise Exception("Die Karte ist nicht rechteckig!")
			else:
				self.width = len(line)
	def __call__(self, x, y):
		return self.structure[y][x]

	def getCSI(self, target):
		return min(target.get_width() / (self.width+2), target.get_height() / (self.height+2))

	def draw(self, target):
		CSI = self.getCSI(target)
		for x in range(self.height):
			Slot().draw(target, (x+1)*CSI, 0, CSI)
			Slot().draw(target, (x+1)*CSI, (self.width+1)*CSI, CSI)
		for y in range(self.width):
			Slot().draw(target, 0, (y+1)*CSI, CSI)
			Slot().draw(target, (self.height+1)*CSI, (y+1)*CSI, CSI)
			for x in range(self.height):
				self(x,y).draw(target, (x+1)*CSI, (y+1)*CSI, CSI)

	def px2cord(self, target, x, y):
		CSI = self.getCSI(target)
		return x / CSI, y / CSI

	def mapType(self, x, y):
		a, b = (0 < x <= self.width), (0 < y <= self.height)
		if a and b:
			return self(x-1,y-1)
		if not (a or b):
			return None
		if a:
			return Slot((0, (1 if y == 0 else -1)))
		if b:
			return Slot(((1 if x == 0 else -1), 0))
class Empty(object):
	def draw(self, target, x, y, CSI):
		draw.rect(target, (200, 200, 200), Rect((x, y),(CSI, CSI)) )
		draw.rect(target, (0, 0, 0), Rect((x, y),(CSI, CSI)), 1)

class Null(object):
	def draw(self, target, x, y, CSI):
		draw.rect(target, (0, 0, 0), Rect((x, y),(CSI, CSI)) )

class Static(object):
	def draw(self, target, x, y, CSI):
		draw.rect(target, (100, 100, 100), Rect((x, y),(CSI, CSI)) )
		draw.rect(target, (0, 0, 0), Rect((x, y),(CSI, CSI)), 1)

class Slot(object):
	def __init__(self, direction=None):
		self.direction = direction
	def draw(self, target, x, y, CSI):
		draw.rect(target, (100, 100, 200), Rect((x, y),(CSI, CSI)) )
		draw.rect(target, (0, 0, 0), Rect((x, y),(CSI, CSI)), 1)

settings = {
'.' : Empty,
'x' : Static
}
