import pygame
pygame.init()

size = (640, 480)
screen = pygame.display.set_mode(size)

import sys
from modules.map import World, Slot
from modules.block import Block
from modules.player import Player
from modules.recolor import compileSVASheet
print sys.argv[1]

with open(sys.argv[1]) as f:
	m = World(f.read())


clock = pygame.time.Clock()
worldTime = 0

autoMove = False
animationDuration = 10
animTick = 0

red = Player((255, 0, 0))
yellow = Player((255, 255, 0))
current = red

while True:
	clock.tick(30)
	worldTime += 1
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if e.type == pygame.MOUSEBUTTONDOWN:
			if e.button == 1:
				pos = m.px2cord(screen, *e.pos)
				if m.blocks(*pos) is not None:
					print m.blocks(*pos)
					continue
				if isinstance(m(*pos), Slot):
					Block(m, current, *pos)
					current = (yellow if current==red else red)
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE:
				m.move(animationDuration)
			elif e.key == pygame.K_a:
				autoMove = not autoMove
			
	m.draw(screen, worldTime)
	
	if autoMove:
		animTick += 1
		if animTick == animationDuration:
			animTick = 0
			m.move(animationDuration)
			
	pygame.display.flip()
