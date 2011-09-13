"""This Modul implements a Map class that stores all information about the map's state"""

from pygame import draw, image, Rect

CSI = 30

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
	def _cells(self):
		for x in range(self.width):
			for y in range(self.height):
				yield x,y
	cells = property(_cells)
	def draw(self, target):
		for x,y in self.cells:
			self(x,y).draw(target, x*CSI, y*CSI)

class Empty(object):
	def draw(self, target, x, y):
		draw.rect(target, (200, 200, 200), Rect((x, y),(CSI, CSI)) )
		draw.rect(target, (0, 0, 0), Rect((x, y),(CSI, CSI)), 1)

class Static(object):
	def draw(self, target, x, y):
		draw.rect(target, (100, 100, 100), Rect((x, y),(CSI, CSI)) )
		draw.rect(target, (0, 0, 0), Rect((x, y),(CSI, CSI)), 1)

settings = {
'.' : Empty,
'x' : Static
}
