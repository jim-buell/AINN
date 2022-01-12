import random

#gets a random word from a list of specified word types. Pass a str indicating the 
#part of speech to get that type of word. 
def getword(wordType):
	File = open(r"words/{}.txt".format(wordType), "r")
	wordList = []
	Lines = File.readlines()
	for item in Lines:
		wordList.append(item.strip())
	nextWord = wordList[random.randrange(0, len(wordList))]
	#print("The selected word is ", verbList[random.randrange(0, len(verbList))])
	return nextWord
	
def typeSen():
	#sentence structures 
	struct1 = ["NN", "VBZ", "JJ", "NNS"]
	struct2 = ["NNP", "VBN", "NN"]
	struct3 = ["NNP", "verbTrans", "JJ", "NN"]
	
	allSentences = [struct3]
	
	x = 0
	while x <= 20:
		mainStr = ""
		wordSeq = allSentences[random.randrange(0, len(allSentences))]
		for item in wordSeq:
			mainStr = mainStr + getword("{}".format(item)) + " "
		mainStr = mainStr.upper()
		print(mainStr)
		x = x + 1
		
#testTypeSen()
		
typeSen()





