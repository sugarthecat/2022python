import random as r
import pygame
cityImg = pygame.image.load('megacity.png')
facImg = pygame.image.load('factory.png')
militiaImg = pygame.image.load('militia.png')
infImg = pygame.image.load('infantry.png')
boatImg = pygame.image.load('patrolboat.png')
bcImg = pygame.image.load('battlecopter.png')
tankImg = pygame.image.load('tank.png')
carrierImg = pygame.image.load('carrier.png')
colors = [(0,0,0), (255,255,255), (255,50,50),(100,0,0), (100,100,100), (255,255,0), (180,0,180),(0,100,0),(0,0,100)]
class Tile:
	def __init__(self,landtype,border):
		self.owner = False
		self.ontile = False
		self.costal = False
		self.type = landtype
		if self.type == False:
			self.type = "Water"
			self.color = (55, 120, 255)
		else:
			self.type = "Land"
			self.color = (100,255,50)
		self.border = border
		self.money = 0
	def display(self,screen):
		if self.ontile and self.ontile.hp <=0:
			self.ontile = False
		if self.type == "Water":
			self.color = (55,120,255)
		if self.ontile and self.type == "Land":
			self.color = self.ontile.color
		elif self.ontile:
			self.color = (self.color[0]*0.5 + self.ontile.color[0]*0.5,
				self.color[1]*0.5 + self.ontile.color[1]*0.5,
				self.color[2]*0.5 + self.ontile.color[2]*0.5,)
		pygame.draw.polygon(screen,self.color,self.border)
		self.money+=1
	def displayTile(self,screen):
		if self.ontile:
			self.ontile.display(screen,self.border[0],(self.border[2][0]-self.border[0][0],self.border[3][1]-self.border[0][1]))
	
class City:
	def __init__(self,iid):
		self.hp = 10
		self.money = 0
		self.type = "City"
		self.canSpawn = True
		self.id = iid
		self.color = colors[iid % len(colors)]
	def display(self,screen,xy,wh):
		thisVer = pygame.transform.scale(cityImg,wh)
		screen.blit(thisVer,xy)
		self.money +=1
	def spawn(self,caps):
		if self.money > 12 and r.randint(0,2) == 0 and caps["Infantry"] < 15:
			self.money-=12
			return Infantry(self.color,self.id)
		elif self.money > 15 and r.randint(0,2) == 0 and caps["Patrol Boat"] < 10:
			self.money-=15
			return patrolBoat(self.color,self.id)
		elif r.randint(0,3) == 0 and self.money > 6 and caps["Militia"] < 10:
			return Militia(self.color,self.id)
			self.money -= 6
		else:
			return False
class Factory:
	def __init__(self,iid):
		self.hp = 10
		self.money = 0
		self.type = "City"
		self.canSpawn = True
		self.id = iid
		self.color = colors[iid % len(colors)]
	def display(self,screen,xy,wh):
		thisVer = pygame.transform.scale(facImg	,wh)
		screen.blit(thisVer,xy)
		self.money +=1
	def spawn(self,caps):
		if self.money > 20 and caps["Attack Helicopter"] < 10 and r.randint(0,2) == 0:
			self.money-=20
			return AttackHelicopter(self.color,self.id)
		if self.money > 20 and caps["Tank"] < 5 and r.randint(0,2) == 0:
			self.money-=20
			return Tank(self.color,self.id)
		if self.money > 100 and caps["Carrier"] < 1 and r.randint(0,2) == 0:
			self.money-=100
			return Carrier(self.color,self.id)
		else:
			return False
class Militia:
	def __init__(self,color,cityid):
		self.color = color
		self.hp = 7
		self.dmg = 2
		self.id = cityid
		self.type = "Unit"
		self.canSpawn = False	
		self.unitType = "Militia"
		self.attacklocked = False
	def display(self,screen,xy,wh):
		thisVer = pygame.transform.scale(militiaImg,wh)
		screen.blit(thisVer,xy)
	def canMoveOn(self,tile):
		if tile == "Land":
			return True
		if tile == "Water":
			return False
class Carrier:
	def __init__(self,color,cityid):
		self.color = color
		self.hp = 10
		self.dmg = 2
		self.id = cityid
		self.type = "Unit"
		self.canSpawn = True	
		self.unitType = "Carrier"
		self.attacklocked = False
		self.helisleft = r.randint(3,5)
	def display(self,screen,xy,wh):
		thisVer = pygame.transform.scale(carrierImg,wh)
		screen.blit(thisVer,xy)
	def canMoveOn(self,tile):
		if tile == "Land":
			return False
		if tile == "Water":
			return True
	def spawn(self,caps):
		if self.helisleft > 0 and r.randint(0,50) == 0:
			self.helisleft -=1
			return AttackHelicopter(self.color,self.id)
		else:
			return False
class AttackHelicopter:
	def __init__(self,color,cityid):
		self.color = color
		self.hp = 10
		self.dmg = 10
		self.id = cityid
		self.canSpawn = False	
		self.type = "Unit"
		self.unitType = "Attack Helicopter"
		self.attacklocked = False
	def display(self,screen,xy,wh):
		thisVer = pygame.transform.scale(bcImg,wh)
		screen.blit(thisVer,xy)
	def canMoveOn(self,tile):
		if tile == "Land":
			return True
		if tile == "Water":
			return True
class Infantry:
	def __init__(self,color,cityid):
		self.color = color
		self.hp = 10
		self.canSpawn = False	
		self.dmg = 3
		self.id = cityid
		self.type = "Unit"
		self.unitType = "Infantry"
		self.attacklocked = False
	def display(self,screen,xy,wh):
		thisVer = pygame.transform.scale(infImg,wh)
		screen.blit(thisVer,xy)
	def canMoveOn(self,tile):
		if tile == "Land":
			return True
		if tile == "Water":
			return False
class Tank:
	def __init__(self,color,cityid):
		self.color = color
		self.hp = 40
		self.canSpawn = False	
		self.dmg = 4
		self.id = cityid
		self.type = "Unit"
		self.unitType = "Tank"
		self.attacklocked = False
	def display(self,screen,xy,wh):
		thisVer = pygame.transform.scale(tankImg,wh)
		screen.blit(thisVer,xy)
	def canMoveOn(self,tile):
		if tile == "Land":
			return True
		if tile == "Water":
			return False
class patrolBoat:
	def __init__(self,color,cityid):
		self.color = color
		self.hp = 20
		self.dmg = 5
		self.canSpawn = False	
		self.id = cityid
		self.type = "Unit"
		self.unitType = "Patrol Boat"
		self.attacklocked = False
	def display(self,screen,xy,wh):
		thisVer = pygame.transform.scale(boatImg,wh)
		screen.blit(thisVer,xy)
	def canMoveOn(self,tile):
		if tile == "Land":
			return False
		if tile == "Water":
			return True
