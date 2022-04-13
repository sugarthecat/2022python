import math
import pygame
from noise import snoise2, pnoise2
import random as ran
import time as t
class Nation:
	def __init__(self):
		self.color = (ran.randint(0,255),ran.randint(0,255),ran.randint(0,75))
class Point:
	def __init__(self):
		self.x = ran.randint(0,1800)
		self.y = ran.randint(0,900)	
		self.connections = []
		self.border = []
		self.nation = ran.randint(0,len(nations)-1)
		self.color = nations[self.nation].color
		self.defense = 1
		self.atk = 10
	def setUpBorder(self):
		self.border = []
		for c in self.connections:
			if points[c].nation == self.nation:
				self.border.append( (points[c].x * 0.5 + self.x*0.5 ,points[c].y * 0.5 + self.y * 0.5) )
			else:
				factor = points[c].defense+self.defense
				self.border.append( (self.x * (points[c].defense/factor) + points[c].x* (self.defense/factor) ,self.y * (points[c].defense/factor) + points[c].y* (self.defense/factor)) )
			for dc in points[c].connections:
				if dc in self.connections:
					factor = points[dc].defense + points[c].defense + self.defense

					self.border.append( (  self.x * (1-self.defense/factor)/2 + points[c].x * (1-points[c].defense/factor)/2 + points[dc].x * (1-points[dc].defense/factor)/2, self.y * (1-self.defense/factor)/2 + points[c].y * (1-points[c].defense/factor)/2 + points[dc].y * (1-points[dc].defense/factor)/2 ) )
		self.border.sort(key=lambda x: AngleBtw2Points(x,(self.x,self.y)), reverse=True)
	def display(self):
		self.setUpBorder()
		self.color = nations[self.nation].color
		if(len(self.border) > 2):
			pygame.draw.polygon(screen, self.color,self.border)
			if self.color[0] + self.color[1] + self.color[2] > 255:
				pygame.draw.circle(screen, (0,0,0),(self.x,self.y),5)
			else:
				pygame.draw.circle(screen, (255,255,255),(self.x,self.y),5)
		else:
			self.border.append((self.x,self.y))
	def attack(self):
		self.defense = self.defense + 1.5
		self.defense = self.defense * 0.999
		self.atk = self.atk + 2 + ran.random()
		possibleAttacks = self.connections.copy()
		for a in possibleAttacks[:]:
			if points[a].nation == self.nation:
				possibleAttacks.remove(a)
		if len(possibleAttacks) > 0:
			chosenAttack = ran.choice(possibleAttacks)
			points[chosenAttack].defense -= self.atk / 4 * ran.random()
			self.atk = self.atk * 3/4
			if points[chosenAttack].defense <= 0:
				points[chosenAttack].nation = self.nation
				points[chosenAttack].defense = self.atk / 2
				points[chosenAttack].atk = self.atk / 2
				self.atk = self.atk / 2
		else:
			sendDestination = ran.choice(self.connections.copy())
			points[sendDestination].atk += self.atk / 10.1
			self.atk = self.atk * 0.9

#snippet: https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
# assumes line segments are stored in the format [(x0,y0),(x1,y1)]
def intersects(s0,s1):
    dx0 = s0[1][0]-s0[0][0]
    dx1 = s1[1][0]-s1[0][0]
    dy0 = s0[1][1]-s0[0][1]
    dy1 = s1[1][1]-s1[0][1]
    p0 = dy1*(s1[1][0]-s0[0][0]) - dx1*(s1[1][1]-s0[0][1])
    p1 = dy1*(s1[1][0]-s0[1][0]) - dx1*(s1[1][1]-s0[1][1])
    p2 = dy0*(s0[1][0]-s1[0][0]) - dx0*(s0[1][1]-s1[0][1])
    p3 = dy0*(s0[1][0]-s1[1][0]) - dx0*(s0[1][1]-s1[1][1])
    return (p0*p1<=0) & (p2*p3<=0)

#end snippet
#snippet:
def AngleBtw2Points(pointA, pointB):
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return math.atan2(changeInY,changeInX)
#end snippet


print("Setting up...")

time = t.time()
#How precisely the map is to be generated
POINT_COUNT = 500
MIN_DIST_BETWEEN = 20
MAX_LINE_DIST = 500
#set up everything
points = []
nations = []
for i in range(math.floor(POINT_COUNT/2)):
	nations.append(Nation())
for i in range(POINT_COUNT):
	posspoint = Point()
	valid = True
	for point in points:
		if math.dist([point.x,point.y],[posspoint.x,posspoint.y]) < MIN_DIST_BETWEEN:
			valid = False
	if valid:
		points.append(posspoint)
		points[len(points)-1].connections = []
		for i in range(len(points)-1):
			if math.dist([points[i].x,points[i].y],[posspoint.x,posspoint.y]) < MAX_LINE_DIST:
				points[len(points)-1].connections.append(i)

print("Time taken: " + str(t.time()-int(time)))
print("Setting up point connections...")
time = t.time()
for p1 in points[:]:
	for c1 in p1.connections[:]:
		if math.dist([p1.x,p1.y],[points[c1].x,points[c1].y]) > MAX_LINE_DIST:
			p1.connections.remove(c1)
		else:
			for p2 in points[:]:
				for c2 in p2.connections[:]:
					possibs = [(p1.x,p1.y),
						(p2.x,p2.y),
						(points[c1].x,points[c1].y),
						(points[c2].x,points[c2].y)]
					valid = True
					tpts = []
					for poss in possibs:
						if poss in tpts:
							valid = False
						tpts.append(poss)

					if valid and c1 in p1.connections and c2 in p2.connections and intersects( [(p1.x,p1.y),(points[c1].x,points[c1].y)], [(p2.x,p2.y),(points[c2].x,points[c2].y)]):
						if math.dist([p1.x,p1.y],[points[c1].x,points[c1].y]) > math.dist([p2.x,p2.y],[points[c2].x,points[c2].y]):
							p1.connections.remove(c1)
						elif math.dist([p1.x,p1.y],[points[c1].x,points[c1].y]) < math.dist([p2.x,p2.y],[points[c2].x,points[c2].y]):
							p2.connections.remove(c2)
						else:
							print("whoah dude, thats crazy")

for p in range(len(points)):
	for c in points[p].connections:
		if not (p in points[c].connections):
			points[c].connections.append(p)
print("Time taken: " + str(t.time()-int(time)))
print("Setting up Borders...")
for p in range(len(points)):
	for c in points[p].connections:
		if not (p in points[c].connections):
			points[c].connections.append(p)

for p in points:
	p.setUpBorder()
#leftright (direction (left-right) that people go through)
leftright = False
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([1800, 900])
running = True
while running:
	for nation in nations:
		nation.strength = 0
	screen.fill((50,100,255))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	for point in points:
		point.display()	
		nations[point.nation].strength += 1
	for point in points:
		for i in point.connections:
			pygame.draw.line(screen,(0,0,0),(point.x,point.y),(points[i].x,points[i].y))
			pass
		point.attack()
	pygame.display.flip()

pygame.quit()
