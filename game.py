import pygame
pygame.init()

import sys
from modules.map import Map, Slot
from modules.block import Block
print sys.argv[1]

with open(sys.argv[1]) as f:
	m = Map(f.read())

print m.width, m.height
print m(2,1)

blocks = []

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
				if isinstance(m.mapType(*pos), Slot):
					blocks.append(Block(*pos, direction=m.mapType(*pos).direction))
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE:
				for block in blocks:
					block.move()

	m.draw(screen)
	for block in blocks:
		block.draw(screen, m)
	pygame.display.flip()
