import pygame
colors = [(255,255,255), (228,228,228),(136,136,136), (34,34,34), (255,167,209),(229, 0, 0),(229, 149, 0),(160, 106, 66),(229, 217, 0),(148, 224, 68),(2, 190, 1),(0, 229, 240),(0, 0, 234),(0, 0, 234),(224, 74, 255),(130, 0, 128)]
file = open('tiles_filtered.csv','r')
index = 0;

placed = []
for i in range(1001):
	placed.append([])
	for j in range(1001):
		placed[i].append(False)

pygame.init()
screen = pygame.display.set_mode([1000, 1000])
screen.fill((255,255,255))
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	maintime = "Start"
	going = True
	while going:
		line = file.readline()
		if line == "":
			going = False
		else:
			color = colors[int(line.split(',')[3])]
			args = (int(line.split(',')[1]),int(line.split(',')[2]),1,1)
			if not placed[int(line.split(',')[1])][int(line.split(',')[2])]:
				pygame.draw.rect(screen,color,args)
				#placed[int(line.split(',')[1])][int(line.split(',')[2])] = True
			time = float(line.split(',')[0])
			if maintime == "Start":
				maintime = time
			if maintime + 12 < time:
				going = False

	pygame.display.flip()

pygame.quit()