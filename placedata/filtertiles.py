lines = []
with open('place_tiles.csv','r') as f:
    lines = f.readlines()
print(len(lines))
l = 0
while l< len(lines):
	line = lines[l]
	
	time = line.split(',')[0][6:len(line.split(',')[0])-4] 
	time = time.replace(":","")
	time = time.replace("-","")
	time = time.replace(" ","")
	if len(line.split(',')) == 5:
		end = time + "," + line.split(',')[2] + "," + line.split(',')[3] + ","+ line.split(',')[4]

	if len(line.split(',')) == 5 and len(time) > 0 and line.split(',')[2] != "":
		lines[l] = end
	else:
		print("Removed " + lines[l])
		lines.remove(lines[l])
		l -=1
	l+=1
print("Placement done. Now sorting...")

lines.sort(key=lambda x: float(x.split(',')[0]), reverse=False)
print("Sorted!")

file2 = open("tiles_filtered.csv","w")
for line in lines:
	file2.write(line)
file2.close()
print(Added to file!)