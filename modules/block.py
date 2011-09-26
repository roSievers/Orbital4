"""This Module implements a Block class that supports movements, collisions and stopping"""

from pygame import draw, Rect, sprite
from tile import DirectedTile, Static, TriggerTile
from animation import StaticAnimator, FlowAnimator
from math import CentralCurry as CC

class Block(DirectedTile, sprite.Sprite):
	def __init__(self, world, x, y):
		DirectedTile.__init__(self, x, y, (0, 0))
		sprite.Sprite.__init__(self, world)
		self.world = world
		
		self.anim = CC(StaticAnimator)
	def draw(self, target, time):
		CSI = self.world.getCSI(target)
		rect = Rect((self.x * CSI+5, self.y * CSI+5), (CSI-10, CSI-10))
		
		if callable(self.anim):
			# If the animator isn't constructed yet, create one
			self.anim = self.anim(time, rect)
			
		draw.rect(target, (200, 0, 0), self.anim.evaluate(time))
	def move(self, animationDuration):
		# current Tile
		tile = self.world(self.x, self.y)
		
		# trigger the current Tile
		if isinstance(tile, TriggerTile):
			tile.trigger(self)
						
		target = self.world(self.x+self.direction[0], self.y+self.direction[1])
		
		if isinstance(target, Static):
			self.direction = (0, 0)
		
		self.x += self.direction[0]
		self.y += self.direction[1]
		
		a = self.anim
		
		def curry(time, rect):
			if not callable(a):
				return FlowAnimator(time, animationDuration, a, StaticAnimator(time, rect))
			else:
				return FlowAnimator(time, animationDuration, a(time, rect), StaticAnimator(time, rect))
				
		
		self.anim = curry
	def _getIsStatic(self):
		return self.x == 0 == self.y
	isStatic = property(_getIsStatic)
