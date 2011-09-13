import pygame
pygame.init()

import sys
from modules.map import Map

print sys.argv[1]

with open(sys.argv[1]) as f:
	m = Map(f.read())

print m.structure
print m.width, m.height
print m(2,1)

size = (640, 480)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

while True:
	clock.tick(30)
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			sys.exit()

	m.draw(screen)
	pygame.display.flip()
