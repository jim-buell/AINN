import random
from guizero import App, Text, Window
import time

mainStr = ""
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
	
	#add words to the main string. There's an extra space in the from of the string to make the timing better. 
	global mainStr
	mainStr = ""
	wordSeq = allSentences[random.randrange(0, len(allSentences))]
	for item in wordSeq:
		mainStr = " " + mainStr + getword("{}".format(item)) + " "
	mainStr = mainStr.upper()
	#print(mainStr)
	return mainStr
		
#initiates the GUI
app = App(title="Infinite Scroll 2.0", bg="#000000")

def pause():
	nothing = 0
	nothing += 1
	print(nothing)

#main text display 
#blankLeft = Text(app, text = "", size = 72, align = "left", font = "akkurat mono", bg = "#000000")
displayText = Text(app, text = "", size = 72, font = "akkurat mono", bg = "#000000", color = "#ffffff", align="left")

#calls the sentence creator and updates the display text
def updateText():
	global counter
	global dispStr
	global mainStr
	dispStr = dispStr + mainStr[counter]
	displayText.value = dispStr
	counter += 1
	print(counter)
	if counter >= len(mainStr):
		app.after(1000, pause)
		mainStr = ""
		typeSen()
		counter = 0
		dispStr = " "
		time.sleep(1.5)
		displayText.value = ""

#calls updateText repeatedly in the app loop — gets new letters to pass to the GUI
app.repeat(150, updateText)

#sets the initial sentence 
typeSen()

#sets full screen
app.set_full_screen()

#this is the main GUI loop
app.display()





