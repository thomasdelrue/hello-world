import math
import random
import pygame
import pygame.gfxdraw
from pygame.locals import *
from sys import *

from vector2 import Vector2


FPS = 4

'''img = pygame.Surface((30, 30))
pygame.draw.rect(img, (124, 0, 0), (6, 6, 16, 16), 1)
pygame.draw.line(img, (255, 0, 0), (10, 10), (10, 0))'''


rotation = 0.0

#setrecursionlimit(1500)

def bezier1(p0, p1):
    # calculate 20 points...
    bez_points = []
    
    for i in range(0, 51):
        t = i / 50
        x = (1 - t) * p0.x + t * p1.x
        y = (1 - t) * p0.y + t * p1.y
        bez_points.append(Vector2(int(x), int(y)))
    
    return bez_points


def bezier2(p0, p1, p2):
    # calculate 20 points...
    bez_points = []
    
    for i in range(0, 51):
        t = i / 50
        x = (1 - t) ** 2 * p0.x + 2 * (1 - t) * t * p1.x + t ** 2 * p2.x
        y = (1 - t) ** 2 * p0.y + 2 * (1 - t) * t * p1.y + t ** 2 * p2.y
        bez_points.append(Vector2(int(x), int(y)))
    
    return bez_points


def bezier3(p0, p1, p2, p3):
    # calculate 20 points...
    bez_points = []
    
    for i in range(0, 21):
        t = i / 20
        x = (1 - t) ** 3 * p0.x + 3 * (1 - t) ** 2 * t * p1.x + 3 * (1 - t) * t ** 2 * p2.x + t ** 3 * p3.x
        y = (1 - t) ** 3 * p0.y + 3 * (1 - t) ** 2 * t * p1.y + 3 * (1 - t) * t ** 2 * p2.y + t ** 3 * p3.y
        bez_points.append(Vector2(int(x), int(y)))
    
    return bez_points

	
def bezier3(p0, p1, p2, p3, t):
	x = (1 - t) ** 3 * p0.x + 3 * (1 - t) ** 2 * t * p1.x + 3 * (1 - t) * t ** 2 * p2.x + t ** 3 * p3.x
	y = (1 - t) ** 3 * p0.y + 3 * (1 - t) ** 2 * t * p1.y + 3 * (1 - t) * t ** 2 * p2.y + t ** 3 * p3.y
	return Vector2(int(x), int(y))
	
def dot(v1, v2):
	return v1.x * v2.x + v1.y * v2.y
	
	
def findDrawingPoints(t0, t1, insertionIndex, pointList):
	tMid = (t0 + t1) / 2
	lp0 = bezier3(p0, p1, p2, p3, 0)
	lp1 = bezier3(p0, p1, p2, p3, 1)
	
	if (lp0 - lp1).get_magnitude() < 100:
		return 0
	
	pMid = bezier3(p0, p1, p2, p3, tMid)
	leftDirection = (lp0 - pMid) 
	leftDirection.normalize()
	rightDirection = (lp1 - pMid) 
	rightDirection.normalize()
	
	print('3v', lp0, lp1, pMid)
	print('l', leftDirection)
	print('r', rightDirection)
	
	print(dot(leftDirection, rightDirection))
	dotP = dot(leftDirection, rightDirection)
	if dotP > -0.99 and dotP != 0.0:
		pointsAdded = 0
		
		pointsAdded += findDrawingPoints(t0, tMid, insertionIndex, pointList)
		
		pointList.insert(insertionIndex + pointsAdded, pMid)
		pointsAdded += findDrawingPoints(tMid, t1, insertionIndex + pointsAdded, pointList)
		
		return pointsAdded
		
	return 0
	
	
def findPoints():
	pointList = []
	lp0 = bezier3(p0, p1, p2, p3, 0)
	lp1 = bezier3(p0, p1, p2, p3, 1)
	pointList.append(lp0)
	pointList.append(lp1)
	
	pointsAdded = findDrawingPoints(0, 1, 1, pointList)
	
	assert(pointsAdded + 2 == len(pointList))
	return pointList
	
	
pygame.init()
screen = pygame.display.set_mode((500, 600), 0, 32)

'''sprite_map = pygame.image.load('Reference_material\\galaga sprite map.png').convert_alpha()
img = sprite_map.subsurface((20, 100, 20, 20))'''


clock = pygame.time.Clock()

p0 = Vector2(100, 100)
p1 = Vector2(200, 100)

p2 = Vector2(100, 200)
p3 = Vector2(100, 200)

RED = (255, 0, 0)

screen.fill((0, 0, 0))

points = []

'''points = bezier1(p0, p1)
print(points)

points.extend(bezier2(p0, p2, p1))'''

'''points.append(bezier3(p0, p2, p1, p3, 0))
points.append(bezier3(p0, p2, p1, p3, 1))
points.append(bezier3(p0, p2, p1, p3, .5))'''

points = findPoints()
print(points)

'''vo = Vector2(0, -10)
v0 = None'''

params = [p0, p1, p2, p3]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
    if len(points) > 0:
        #screen.fill((0, 0, 0))        
        v1 = points.pop(0)
        pygame.gfxdraw.aacircle(screen, v1.x, v1.y, 2, RED) 
        
        '''if v0:
            rotation = Vector2.getAngle(vo, v1 - v0) 
            print(rotation)
            newImg = pygame.transform.rotate(img, -rotation).convert_alpha()
            imgPos = v1.x - newImg.get_width() // 2, v1.y - newImg.get_height() // 2
            
            screen.blit(newImg, imgPos)
        
        v0 = v1 '''
    '''else:
        random.shuffle(params)
        print(params)
        points = bezier3(*tuple(params))'''
        #v0 = None

    
    
    clock.tick(FPS)
    pygame.display.update()
    
    
    
    
        