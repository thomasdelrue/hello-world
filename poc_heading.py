import math
import pygame
from pygame.locals import *
from sys import exit

from vector2 import Vector2

vs = []

def draw():
	pygame.init()
	screen = pygame.display.set_mode((600, 600), 0, 32)

	screen.fill((0, 0, 0))

	for v in vs:
		pygame.draw.circle(screen, (255, 0, 0), tuple(v), 10, 1)

	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			
if __name__ == '__main__':
	v = Vector2(300, 300)
	
	vs.append(v)
	
	for a in range(0, 360, 45):
		h = Vector2(math.cos(math.radians(a)), math.sin(math.radians(a)))
		print(h, h.getHeading())
		v2 = v + h * 50
		v2 = Vector2(int(v2.x), int(v2.y))
	
		vs.append(v2)

	draw()