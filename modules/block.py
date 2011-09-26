"""This Module implements a Block class that supports movements, collisions and stopping"""

from pygame import draw, image, Rect

class Block(object):
	def __init__(self, x, y, direction):
		self.x, self.y = x, y
		self.direction = direction
	def draw(self, target, map):
		CSI = map.getCSI(target)
		rect = Rect((self.x * CSI+5, self.y * CSI+5), (CSI-10, CSI-10))
		draw.rect(target, (200, 0, 0), rect)
	def move(self):
		self.x += self.direction[0]
		self.y += self.direction[1]
