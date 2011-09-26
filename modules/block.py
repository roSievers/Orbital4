"""This Module implements a Block class that supports movements, collisions and stopping"""

from pygame import draw, Rect, sprite
from tile import DirectedTile, Static, Slot

class Block(DirectedTile, sprite.Sprite):
	def __init__(self, world, x, y):
		DirectedTile.__init__(self, x, y, (0, 0))
		sprite.Sprite.__init__(self, world)
		self.world = world
	def draw(self, target):
		CSI = self.world.getCSI(target)
		rect = Rect((self.x * CSI+5, self.y * CSI+5), (CSI-10, CSI-10))
		draw.rect(target, (200, 0, 0), rect)
	def move(self):
		tile = self.world(self.x, self.y)
		# Read redirecting Information from the map
		if isinstance(tile, DirectedTile):
			if isinstance(tile, Slot):
				# Check, whether the Block left the World
				if self.direction[0] == -tile.direction[0]:
					if self.direction[1] == -tile.direction[1]:
						self.kill()
			self.direction = tile.direction
			
		target = self.world(self.x+self.direction[0], self.y+self.direction[1])
		
		if isinstance(target, Static):
			self.direction = (0, 0)
		
		self.x += self.direction[0]
		self.y += self.direction[1]
