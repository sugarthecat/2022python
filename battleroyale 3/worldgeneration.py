import random as r
from noise import pnoise2

class Ocean:
	def __init__(self):
		self.color = (0,0,220)
		self.teamcolor = False

class CloseOcean:
	def __init__(self):
		self.color = (20,20,230)
		self.teamcolor = False

class Desert:
	def __init__(self):
		self.color = (210,190,0)
		self.teamcolor = False

class Plains:
	def __init__(self):
		self.color = (40,190,50)
		self.teamcolor = False

class Forest:
	def __init__(self):
		self.color = (25,125,0)
		self.teamcolor = False

class Tundra:
	def __init__(self):
		self.color = (215,210,210)
		self.teamcolor = False

class DesertMountain:
	def __init__(self):
		self.color = (95,80,50)
		self.teamcolor = False

class Mountain:
	def __init__(self):
		self.color = (85,85,85)
		self.teamcolor = False

class TundraMountain:
	def __init__(self):
		self.color = (170,170,170)
		self.teamcolor = False


xoffset = r.randint(-10000,10000)
yoffset = r.randint(-10000,10000)
def generateWorld(x,y,scale, enviroscale):
	world = []
	xoffset = r.randint(-100000,100000)
	yoffset = r.randint(-100000,100000)
	xoffset2 = r.randint(-100000,100000)
	yoffset2 = r.randint(-100000,100000)

	for px in range(x):
		world.append([])
		for py in range(y):
			if(pnoise2(px/scale+xoffset2,py/scale+yoffset2, octaves=10) < -0.1):
				world[px].append(Ocean())
			elif(pnoise2(px/scale+xoffset2,py/scale+yoffset2, octaves=10) < 0):
				world[px].append(CloseOcean())
			elif(pnoise2(px/scale+xoffset2,py/scale+yoffset2, octaves=10) < 0.35):
				if(pnoise2(px/enviroscale+xoffset,py/enviroscale+yoffset, octaves=10) < -0.10):
					world[px].append(Desert())
					#Desert
				elif(pnoise2(px/enviroscale+xoffset,py/enviroscale+yoffset, octaves=10) < 0):
					world[px].append(Plains())
					#Plains
				elif(pnoise2(px/enviroscale+xoffset,py/enviroscale+yoffset, octaves=10) < 0.10):
					world[px].append(Forest())
					#Forest
				else:
					world[px].append(Tundra())
					#Snow/Tundra
			else:

				if(pnoise2(px/enviroscale+xoffset,py/enviroscale+yoffset, octaves=10) < -0.1):
					world[px].append(DesertMountain())
					#Desert Mountain
				elif(pnoise2(px/enviroscale+xoffset,py/enviroscale+yoffset, octaves=10) < 0.08):
					world[px].append(Mountain())
					#Mountain
				else:
					world[px].append(TundraMountain())
					#Tundra Mountain
	return world