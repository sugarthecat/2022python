import math
import pygame
from noise import snoise2, pnoise2
import random as ran

pygame.init()
from shape import *
PIXEL_DEFINITION = (140,70)
#How precisely the map is to be generated
NOISE_SCALE = 30
NOISE_THRESHOLD = 0.5
NOISE_OCTAVES = 1
CITY_RARITY = 100
CITY_COSTAL_RARITY = 10
#Start of tile setup
#Sample points to choose wether tile is land or sea
offset = (ran.randint(0,1000000),ran.randint(0,1000000),ran.randint(0,1000000),ran.randint(0,1000000),ran.randint(0,1000000),ran.randint(0,1000000))
samples = []
for x in range(PIXEL_DEFINITION[0]+1):
	samples.append([])
	for y in range(PIXEL_DEFINITION[1]+1):
		if snoise2((x+offset[0])/NOISE_SCALE,(y+offset[1])/NOISE_SCALE) > pnoise2((y+offset[2])/NOISE_SCALE,(x+offset[3])/NOISE_SCALE)/3 or pnoise2((y+offset[4])/NOISE_SCALE*4,(x+offset[5])/NOISE_SCALE*4) >  NOISE_THRESHOLD:
			samples[x].append(True)
		else:
			samples[x].append(False)

#Convert samples into shapes
worldshapes = []
moved = []
for x in range(PIXEL_DEFINITION[0]+1):
	worldshapes.append([])
	moved.append([])
	for y in range(PIXEL_DEFINITION[1]+1):
		worldshapes[x].append([])
		xmod = -1*(y % 2 * 0.5)
		worldshapes[x][y].append(((x+xmod)*1800/PIXEL_DEFINITION[0],(y-0.33)*900/PIXEL_DEFINITION[1]))
		worldshapes[x][y].append(((x+0.5+xmod)*1800/PIXEL_DEFINITION[0],(y-0.67)*900/PIXEL_DEFINITION[1]))
		worldshapes[x][y].append(((x+1+xmod)*1800/PIXEL_DEFINITION[0],(y-0.33)*900/PIXEL_DEFINITION[1]))
		worldshapes[x][y].append(((x+1+xmod)*1800/PIXEL_DEFINITION[0],(y+0.33)*900/PIXEL_DEFINITION[1]))
		worldshapes[x][y].append(((x+0.5+xmod)*1800/PIXEL_DEFINITION[0],(y+0.67)*900/PIXEL_DEFINITION[1]))
		worldshapes[x][y].append(((x+xmod)*1800/PIXEL_DEFINITION[0],(y+0.33)*900/PIXEL_DEFINITION[1]))
		worldshapes[x][y] = Tile(samples[x][y],worldshapes[x][y])
		moved[x].append(False)
		
#Mark any costal tiles as costal
for x in range(len(worldshapes)):
		for y in range(len(worldshapes[x])):
			if worldshapes[x][y].type == "Land":
				bordering = [ (x-2*(y % 2 * 0.5),y-1),(x-1,y),(x-2*(y % 2 * 0.5),y+1),(x+1-2*(y % 2 * 0.5),y+1),(x+1,y),(x+1-2*(y % 2 * 0.5),y-1) ]
				for item in bordering:
					if item[0] >= 0 and item[0] < len(worldshapes) and item[1] >= 0 and item[1] < len(worldshapes[x]) and worldshapes[int(item[0])][item[1]].type == "Water":
						worldshapes[x][y].costal = True
#generate cities
cityID = 0
landUnits =[]
for x in range(len(worldshapes)):
	for y in range(len(worldshapes[x])):
		if(worldshapes[x][y].type == "Land" and ((worldshapes[x][y].costal and ran.randint(0,CITY_COSTAL_RARITY) == 0) or ((not worldshapes[x][y].costal) and ran.randint(0,CITY_RARITY) == 0))):
			if(ran.randint(0,1) == 0):
				worldshapes[x][y].ontile = City(cityID)
			else:
				worldshapes[x][y].ontile = Factory(cityID)
			cityID+=1
			landUnits.append({})

#If any city borders anothetr, remove its existence as a city
for x in range(len(worldshapes)):
		for y in range(len(worldshapes[x])):
			if worldshapes[x][y].ontile and worldshapes[x][y].ontile.type == "City":
				bordering = [ (x-2*(y % 2 * 0.5),y-1),(x-1,y),(x-2*(y % 2 * 0.5),y+1),(x+1-2*(y % 2 * 0.5),y+1),(x+1,y),(x+1-2*(y % 2 * 0.5),y-1) ]
				for item in bordering:
					if item[0] >= 0 and item[0] < len(worldshapes) and item[1] >= 0 and item[1] < len(worldshapes[x]) and worldshapes[int(item[0])][item[1]].ontile:
						worldshapes[int(item[0])][item[1]].ontile = False


#End of tile setup

#leftright (direction (left-right) that people go through)
leftright = False
pygame.font.init()
font = pygame.font.SysFont('Consolas', 10)
screen = pygame.display.set_mode([1800, 900])
running = True
while running:

	screen.fill((255,255,255))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			print(event.key)          
	
	for x in range(len(worldshapes)):
		for y in range(len(worldshapes[x])):
			worldshapes[x][y].display(screen)
			moved[x][y]= False
	for x in range(len(worldshapes)):
		for y in range(len(worldshapes[x])):
			worldshapes[x][y].displayTile(screen)
	for i in range(len(landUnits)):
		landUnits[i]["Militia"] = 0
		landUnits[i]["Infantry"] = 0
		landUnits[i]["Attack Helicopter"] = 0
		landUnits[i]["Patrol Boat"] = 0 
		landUnits[i]["Tank"] = 0
		landUnits[i]["Carrier"] = 0

	for x in range(len(worldshapes)):
		for y in range(len(worldshapes[x])):
			if worldshapes[x][y].ontile and worldshapes[x][y].ontile.type == "Unit":
				landUnits[worldshapes[x][y].ontile.id][worldshapes[x][y].ontile.unitType] += 1

	#Do spawning
	for x in range(len(worldshapes)):
		for y in range(len(worldshapes[x])):
			if worldshapes[x][y].ontile and worldshapes[x][y].ontile.canSpawn:
				bordering = [ (x-2*(y % 2 * 0.5),y-1),(x-1,y),(x-2*(y % 2 * 0.5),y+1),(x+1-2*(y % 2 * 0.5),y+1),(x+1,y),(x+1-2*(y % 2 * 0.5),y-1) ]
				tryspawn = worldshapes[x][y].ontile.spawn(landUnits[worldshapes[x][y].ontile.id])
				for item in bordering[:]:
					if item[0] < 0 or item[0] >= len(worldshapes) or item[1] < 0 or item[1] >= len(worldshapes[x]):
						bordering.remove(item)
					elif ( tryspawn and not tryspawn.canMoveOn(worldshapes[int(item[0])][item[1]].type)) or worldshapes[int(item[0])][item[1]].ontile:
						bordering.remove(item)
				if len(bordering) > 0:
					place = ran.choice(bordering)
					worldshapes[int(place[0])][place[1]].ontile = tryspawn
					moved[int(place[0])][place[1]] = True
					
					
	# Do movement
	lrThing = range(len(worldshapes))
	lrThing2 = range(len(worldshapes[0]))
	if ran.randint(0,1) == 0:
		lrThing= range(len(worldshapes)-1,0,-1)
	if ran.randint(0,1) == 0:
		lrThing2= range(len(worldshapes[0])-1,0,-1)

	for x in lrThing:
		for y in lrThing2:
			if worldshapes[x][y].ontile and worldshapes[x][y].ontile.type == "Unit" and (not moved[x][y]) and (not worldshapes[x][y].ontile.attacklocked) :
				bordering = [ (x-2*(y % 2 * 0.5),y-1),(x-1,y),(x-2*(y % 2 * 0.5),y+1),(x+1-2*(y % 2 * 0.5),y+1),(x+1,y),(x+1-2*(y % 2 * 0.5),y-1) ]
				for item in bordering[:]:
					if item[0] < 0 or int(item[0]) >= len(worldshapes) or item[1] < 0 or item[1] >= len(worldshapes[x]):
						bordering.remove(item)
					elif ( not worldshapes[x][y].ontile.canMoveOn(worldshapes[int(item[0])][item[1]].type)) or worldshapes[int(item[0])][item[1]].ontile or moved[x][y] or moved[int(item[0])][item[1]]:
						bordering.remove(item)
				if len(bordering) > 0:
					moveto = ran.choice(bordering)
					worldshapes[int(moveto[0])][moveto[1]].ontile = worldshapes[x][y].ontile
					worldshapes[x][y].ontile = False
					moved[int(moveto[0])][moveto[1]] = True
					moved[x][y] = True
	#do attacks 
	for x in range(len(worldshapes)):
		for y in range(len(worldshapes[x])):
			if worldshapes[x][y].ontile and worldshapes[x][y].ontile.type == "Unit":
				bordering = [ (x-2*(y % 2 * 0.5),y-1),(x-1,y),(x-2*(y % 2 * 0.5),y+1),(x+1-2*(y % 2 * 0.5),y+1),(x+1,y),(x+1-2*(y % 2 * 0.5),y-1) ]
				for item in bordering[:]:
					if item[0] < 0 or int(item[0]) >= len(worldshapes) or item[1] < 0 or item[1] >= len(worldshapes[x]):
						bordering.remove(item)
					elif (not worldshapes[int(item[0])][item[1]].ontile) or worldshapes[int(item[0])][item[1]].ontile.color == worldshapes[x][y].ontile.color:
						bordering.remove(item)
				worldshapes[x][y].ontile.attacklocked = False

				if len(bordering) > 0:
					worldshapes[x][y].ontile.attacklocked = True
					target = ran.choice(bordering)
					if worldshapes[int(target[0])][target[1]].ontile.type == "City":
						 worldshapes[int(target[0])][target[1]].ontile.color = worldshapes[x][y].ontile.color
					else:
						worldshapes[int(target[0])][target[1]].ontile.hp -= worldshapes[x][y].ontile.dmg
						
	pygame.display.flip()

pygame.quit()