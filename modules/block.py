"""This Module implements a Block class that supports movements, collisions and stopping"""

from pygame import draw, Rect, sprite
from tile import DirectedTile, Static, TriggerTile
from animation import StaticAnimator, FlowAnimator
from math import CentralCurry as CC

class Block(DirectedTile, sprite.Sprite):
	def __init__(self, world, player, x, y):
		DirectedTile.__init__(self, x, y, (0, 0))
		sprite.Sprite.__init__(self)
		self.world = world
		self.world.registerBlock(self)
		self.player = player
		
		self.anim = CC(StaticAnimator)
	def draw(self, target, time):
		CSI = self.world.getCSI(target)
		rect = Rect((self.x * CSI+5, self.y * CSI+5), (CSI-10, CSI-10))
		
		if callable(self.anim):
			# If the animator isn't constructed yet, create one
			self.anim = self.anim(time, rect)
			
		draw.rect(target, self.player.color, self.anim.evaluate(time))
		if self.isStatic:
			draw.rect(target, (150, 0, 150), self.anim.evaluate(time), 2)
	def trigger(self):
		# current Tile
		tile = self.world(self.x, self.y)
		
		# trigger the current Tile
		if isinstance(tile, TriggerTile):
			tile.trigger(self)
		
	def	makeRequest(self, requestMap):
		self.target = self.x+self.direction[0], self.y+self.direction[1]
		requestMap.set(*self.target, value=self)
	
	def move(self, animationDuration):
		
		"""self.x += self.direction[0]
		self.y += self.direction[1]"""
		self.x, self.y = self.target
		
		a = self.anim
		
		def curry(time, rect):
			if not callable(a):
				return FlowAnimator(time, animationDuration, a, StaticAnimator(time, rect))
			else:
				return FlowAnimator(time, animationDuration, a(time, rect), StaticAnimator(time, rect))
				
		self.anim = curry
		
	def kill(self):
		self.world.removeBlock(self.x, self.y)
		sprite.Sprite.kill(self)
	def _getIsStatic(self):
		return self.direction[0] == 0 == self.direction[1]
	isStatic = property(_getIsStatic)
	
	def __str__(self):
		return "<Block(%d, %d) -> (%d, %d)>" % (self.x, self.y, self.direction[0], self.direction[1])
