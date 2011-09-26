import pygame
pygame.init()

import sys
from modules.map import World, Slot
from modules.block import Block
print sys.argv[1]

with open(sys.argv[1]) as f:
	m = World(f.read())

size = (640, 480)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
worldTime = 0

autoMove = False
animationDuration = 10
animTick = 0

while True:
	clock.tick(30)
	worldTime += 1
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			sys.exit()
		if e.type == pygame.MOUSEBUTTONDOWN:
			if e.button == 1:
				pos = m.px2cord(screen, *e.pos)
				if isinstance(m(*pos), Slot):
					Block(m, *pos)
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE:
				for block in m:
					block.move(animationDuration)
			elif e.key == pygame.K_a:
				autoMove = not autoMove
			
	m.draw(screen)
	for block in m:
		block.draw(screen, worldTime)
	
	if autoMove:
		animTick += 1
		if animTick == animationDuration:
			animTick = 0
			for block in m:
				block.move(animationDuration)
	pygame.display.flip()
