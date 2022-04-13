import pygame
from worldgeneration import generateWorld

TILESIZE = 3

def renderWorld():
	for x in range(len(world)):
		for y in range(len(world[x])):
			if mapMode == "geography":
				pygame.draw.rect(screen,world[x][y].color,(x*TILESIZE,y*TILESIZE,TILESIZE,TILESIZE))
			if mapMode == "political" and world[x][y].teamcolor:
				pygame.draw.rect(screen,world[x][y].color,(x*TILESIZE,y*TILESIZE,TILESIZE,TILESIZE))
world = generateWorld(int(1800/TILESIZE),int(800/TILESIZE),250/TILESIZE,750/TILESIZE)
pygame.init()
screen = pygame.display.set_mode([1800, 900])
pygame.font.init()
font = pygame.font.SysFont('Consolas', 50)
mapMode = "geography"
screen.fill((255,255,255))
running = True
print(len(world))
renderWorld()
while running:
	mousex, mousey = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONUP:
			if mousex > 0 and mousex < 1000 and mousey > 800 and mousey < 900:
				mapMode = "geography"
				renderWorld()
			if mousex > 350 and mousex < 700 and mousey > 800 and mousey < 900:
				mapMode = "political"
				renderWorld()
	pygame.draw.rect(screen,(255,255,255),(0,800,1800,100))
	if mousex > 0 and mousex < 350 and mousey > 800 and mousey < 900:
		pygame.draw.rect(screen,(80,80,80),(0,800,350,100))
	if mousex > 350 and mousex < 700 and mousey > 800 and mousey < 900:
		pygame.draw.rect(screen,(80,80,80),(350,800,350,100))
	label = font.render("Geography", 1, (0,0,0))
	screen.blit(label,(50,820))
	label = font.render("Political", 1, (0,0,0))
	screen.blit(label,(400,820))
	pygame.display.flip()
pygame.quit()