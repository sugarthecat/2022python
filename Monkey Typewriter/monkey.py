import random as r
file = open('allWords.txt')
words = file.readlines()
file.close()
letters = "abcdefghijklmnopqrstuvwxyz "
typedwords = []
feed = ""
tried = 0
successes = 0
while True:
	letterchoice = r.choice(letters	)
	
	if letterchoice	== " ":
		tried+=1
		if feed in words:
			print(feed)
			successes+=1

		if(tried % 1000 == 0):
			print(str(successes) + "/" + str(tried))
		feed = ""
	else:
		feed += letterchoice	
