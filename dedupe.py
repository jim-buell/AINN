#remove duplicates

wordList = []
File = open(r"words/verbsNew.txt", "r")
Lines = File.readlines()
for item in Lines:
	wordList.append(item.strip())
	
wordList = list(dict.fromkeys(wordList))

f = open(r"words/verbsNew.txt", "w")
for item in wordList:
	f.write(item + "\n")