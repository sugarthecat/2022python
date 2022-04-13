import math
import pygame
from noise import pnoise2,snoise2
from colors import colorlist
from names import Culture
import random as ran
#Screen size
PWIDTH = 200
PHEIGHT = 100

#Provinces left-right (PWIDTH), provinces up-down(PHEIGHT)
CITY_CHANCE = 300
#1 in CITY_CHANCE of each province being a city
ATTACK_MAX = 1500
#Max number of total attacks occurring in one frame
BOOST_PER_CITY = 15
#random 1 to BOOST_PER_CITY additional attacks per city for its owning color
WORLD_NOISE_SCALE = 500
WORLD_NOISE_OCTAVES = 10
WORLD_NOISE_THRESHOLD = 0.002
#

xoffset = ran.random()*1000000
yoffset = ran.random()*1000000
totalValue = 0
class Province():
	def __init__(self,borders,inid):
		global totalValue
		self.x = int((borders[0][0] + borders[1][0] + borders[2][0] + borders[3][0])/4)
		self.border = borders
		self.y =  int((borders[0][1] + borders[1][1] + borders[2][1] + borders[3][1])/4)
		self.id = ran.randint(0,len(colorlist)-1)
		self.color = colorlist[self.id]
		if snoise2( (self.x+xoffset)/WORLD_NOISE_SCALE,(self.y+yoffset) / WORLD_NOISE_SCALE, WORLD_NOISE_OCTAVES) <= WORLD_NOISE_THRESHOLD:
			self.isLand = True
			if ran.randint(0,CITY_CHANCE) == 0 and self.x > 30 and self.y > 30 and self.x < 1770 and self.y < 870:
				self.isCity = True
				self.cityname = cultures[self.id].cityName()
				cultures[self.id].citynames[str(self.x)+"/"+str(self.y)] = self.cityname
				self.value = ran.randint(1,BOOST_PER_CITY)
				totalValue += self.value
				print("Total City Value: " + str(totalValue))
			else:
				self.isCity = False
		else:
			self.isLand = False
			self.isCity = False
			
	def display(self):
		if(self.isLand):
			pygame.draw.polygon(screen,self.color,self.border)
		elif self.color:
			pygame.draw.polygon(screen,(self.color[0]*0.2,125*0.8 + self.color[1]*0.2,255 * 0.8 + self.color[2]*0.2),self.border)
		else:
			pygame.draw.polygon(screen,(0,125,255),self.border)
	def doText(self):
		if self.isCity:
			if self.color[0] +self.color[1] +self.color[2] < 255:
				clr1 = (255,255,255)
				clr2 = (0,0,0)
				label = cityfont.render(self.cityname, 1, (255,255,255))
			else:
				clr1 = (0,0,0)
				clr2 = (255,255,255)
				label = cityfont.render(self.cityname, 1, (0,0,0))
			pygame.draw.circle(screen,clr1,(self.x,self.y),5)
			if self.value > BOOST_PER_CITY/2:
				pygame.draw.circle(screen,clr2,(self.x,self.y),3.5)
			if self.value >= BOOST_PER_CITY*0.9:
				pygame.draw.circle(screen,clr1,(self.x,self.y),2)
			
			screen.blit(label,(self.x-len(self.cityname),self.y+5))
def revoltIn(selected):
	for i in range(len(provinces)):
		if provinces[i].id == selected and (ran.randint(0,5) != 0) and provinces[i].isLand:
			provinces[i].id = ran.randint(0,len(colorlist)-1)
			provinces[i].color = colorlist[provinces[i].id]
			if not(inCZ[i]):
				inCZ[i] = True
				combatZones.append(i)     

borders = []
cultures = []
for i in range(len(colorlist)):
	cultures.append(Culture())
for x in range(PWIDTH+1):
	for y in range(PHEIGHT+1):
		placex = x*(1800/PWIDTH)-(900/PWIDTH)+ran.random()*0.8*(1800/PWIDTH)+(900/PWIDTH)*0.1
		placey = y*(900/PHEIGHT)-(450/PHEIGHT)+ran.random()*0.8*(900/PHEIGHT)+(900/PHEIGHT)*0.1
		if x == 0:
			placex = 0
		if x == PWIDTH:
			placex = 1800
		if y == 0:
			placey = 0
		if y == PHEIGHT: 
			placey = 900
		borders.append((placex,placey))

provinces = []
for i in range(len(borders)):
	if i > PHEIGHT and i % (PHEIGHT+1) != 0:
		provinces.append(Province([borders[i], borders[i-1], borders[i-PHEIGHT-2], borders[i-PHEIGHT-1]] ,i ))
pygame.init()
pygame.font.init()
combatZones = []
inCZ = []
cityfont = pygame.font.SysFont('Consolas', 10)
for i in range(len(provinces)):
	combatZones.append(i)
	inCZ.append(True)
screen = pygame.display.set_mode([1800, 900])
running = True
while running:
	screen.fill((255, 255, 255))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			#print(event.key)   
			if event.key == 32:   
				mousex, mousey = pygame.mouse.get_pos()
				selected = provinces[math.floor(math.floor(mousex*PWIDTH/1800)*PHEIGHT + math.floor(mousey*PHEIGHT/900))]
				if selected.isLand:
					revoltIn(selected.id)         
						
	identifiers = []
	for province in provinces:
		province.display()
		if not(province.id in identifiers):
			identifiers.append(province.id)
	for province in provinces:
		province.doText()
	#print(str(len(identifiers)) + "/" +str(len(provinces)) + "("+str(math.floor(len(identifiers)/len(provinces)*1000)/10)+"%)")
	'''
	for i in range(len(borders)):
		if i % PHEIGHT != 0:
			pygame.draw.line(screen, (0,0,0), borders[i], borders[i-1],1)
		if i > PHEIGHT-1:
			pygame.draw.line(screen, (0,0,0), borders[i], borders[i-PHEIGHT],1)
	'''
	attack = 0
	scorecolors = []
	colorscores = []
	extraAttacks = []
	for i in range(len(colorlist)):
		extraAttacks.append(0)
	for province in provinces:
		if province.isCity:
			extraAttacks[province.id] += ran.randint(0,province.value ** 2)
		if province.id in scorecolors:
			colorscores[scorecolors.index(province.id)] +=1
		else:
			scorecolors.append(province.id)
			colorscores.append(1)
	if len(scorecolors) > 1:
		most = 0
		total = 0
		for score in colorscores:
			total += score
			if score > most:
				most = score
		attack = total-most
		if attack > ATTACK_MAX:
			attack = ATTACK_MAX
	for i in range(len(extraAttacks)):
		if extraAttacks[i] > 1:
			extraAttacks[i] = math.floor(math.sqrt(extraAttacks[i]))
			
	while attack > 0:
		attackingUnit = combatZones[ran.randint(0,len(combatZones)-1)]
		attackIndexes = []
		if attackingUnit > PHEIGHT:
			attackIndexes.append(attackingUnit-PHEIGHT)
		if attackingUnit + PHEIGHT < len(provinces):
			attackIndexes.append(attackingUnit + PHEIGHT)
		if attackingUnit % PHEIGHT != 0:
			attackIndexes.append(attackingUnit - 1)
		if attackingUnit % PHEIGHT != PHEIGHT-1:
			attackIndexes.append(attackingUnit + 1)
		for i in attackIndexes[:]:
			if provinces[i].id == provinces[attackingUnit].id:
				attackIndexes.remove(i)
			elif not(inCZ[i]):
				combatZones.append(i)
				inCZ[i] = True
		if len(attackIndexes) != 0: 
			attackAt = ran.choice(attackIndexes)
			if (extraAttacks.count(0) == len(extraAttacks) or extraAttacks[provinces[attackingUnit].id] > 0):
				if extraAttacks[provinces[attackingUnit].id] > 0:
					extraAttacks[provinces[attackingUnit].id]-=1
				attack -= 1;
				if provinces[attackingUnit].isLand or (not provinces[attackingUnit].isLand and not provinces[attackAt].isLand) or (ran.randint(0,4) == 1):
					provinces[attackAt].color = provinces[attackingUnit].color
					provinces[attackAt].id = provinces[attackingUnit].id
					if provinces[attackAt].isCity:
						if str(provinces[attackAt].x) + "/" + str(provinces[attackAt].y) in cultures[provinces[attackAt].id].citynames:
							provinces[attackAt].cityname = cultures[provinces[attackAt].id].citynames[(str(provinces[attackAt].x) + "/" +str(provinces[attackAt].y))]
						else:
							provinces[attackAt].cityname = cultures[provinces[attackAt].id].cityName()
							cultures[provinces[attackAt].id].citynames[str(provinces[attackAt].x)+"/"+str(provinces[attackAt].y)] = provinces[attackAt].cityname
					
					if attackAt > PHEIGHT and not inCZ[attackAt-PHEIGHT] and provinces[attackAt-PHEIGHT].id != provinces[attackAt].id:
						combatZones.append(attackAt-PHEIGHT)
						inCZ[attackAt-PHEIGHT] = True
					if attackAt + PHEIGHT < len(provinces) and not inCZ[attackAt+PHEIGHT] and provinces[attackAt+PHEIGHT].id != provinces[attackAt].id:
						combatZones.append(attackAt + PHEIGHT)
						inCZ[attackAt+PHEIGHT] = True
					if attackAt % PHEIGHT != 0 and not inCZ[attackAt-1] and provinces[attackAt-1].id != provinces[attackAt].id:
						combatZones.append(attackAt - 1)
						inCZ[attackAt-1] = True
					if attackAt % PHEIGHT != PHEIGHT-1 and not inCZ[attackAt+1] and provinces[attackAt+1].id != provinces[attackAt].id:
						combatZones.append(attackAt + 1)
						inCZ[attackAt+1] = True
		else:
			combatZones.remove(attackingUnit)
			inCZ[attackingUnit] = False
	pygame.display.flip()

pygame.quit()