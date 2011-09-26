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

while True:
	clock.tick(30)
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
					block.move()

	m.draw(screen)
	for block in m:
		block.draw(screen)
	pygame.display.flip()
