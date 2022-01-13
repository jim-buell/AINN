import random
from guizero import App, Text

mainStr = "Hello World"
counter = 0
dispStr = ""

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
	struct1 = ["NN", "verbTrans", "JJ", "NN"]
	struct2 = ["NN", "verbTrans", "NN"]
	struct3 = ["NNP", "verbTrans", "JJ", "NN"]
	struct4 = ["NNP", "verbTrans", "NN"]
	struct5 = ["NNP", "verbTrans", "NNP"]
	
	allSentences = [struct1, struct2, struct3, struct4, struct5]
	
	global mainStr
	mainStr = ""
	wordSeq = allSentences[random.randrange(0, len(allSentences))]
	for item in wordSeq:
		mainStr = mainStr + getword("{}".format(item)) + " "
	mainStr = mainStr.upper()
	#print(mainStr)
	return mainStr
		
#initiates the GUI
app = App(title="Infinite Scroll 2.0", width=1800, height=80,)

#main text display 
displayText = Text(app, text="start", size=72, font="akkurat mono")

#calls the sentence creator and updates the display text
def updateText():
	global counter
	global dispStr
	global mainStr
	dispStr = dispStr + mainStr[counter]
	displayText.value = dispStr
	counter = counter + 1
	print(counter)
	if counter >= len(mainStr):
		mainStr = ""
		typeSen()
		counter = 0
		dispStr = ""

#calls updateText repeatedly in the app loop — gets new sentences to pass to the GUI
#app.repeat(1000, typeSen)
app.repeat(150, updateText)

#this is the main GUI loop
typeSen()
app.display()





