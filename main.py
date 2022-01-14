import random
from guizero import App, TextBox, Text, Picture, Box
import time

mainStr = ""
counter = 0
dispStr = ""
blinkTime = 0

#gets a random word from a list of specified word types. Pass a str indicating the 
#part of speech to get that type of word. 
def getword(wordType):
	File = open(r"words/{}.txt".format(wordType), "r")
	wordList = []
	Lines = File.readlines()
	for item in Lines:
		wordList.append(item.strip())
	nextWord = wordList[random.randrange(0, len(wordList))]
	return nextWord
	
#function that picks a sentence structure and then grabs random words to form a sentence
def typeSen():
	#sentence structures 
	struct1 = ["NN", "verbTrans", "JJ", "NN"]
	struct2 = ["NN", "verbTrans", "NN"]
	struct3 = ["NNP", "verbTrans", "JJ", "NN"]
	struct4 = ["NNP", "verbTrans", "NN"]
	struct5 = ["NNP", "verbTrans", "NNP"]
	
	allSentences = [struct1, struct2, struct3, struct4, struct5]
	
	#add words to the main string.
	global mainStr
	mainStr = ""
	wordSeq = allSentences[random.randrange(0, len(allSentences))]
	for item in wordSeq:
		mainStr = mainStr + getword("{}".format(item)) + " "
	mainStr = mainStr.upper()
	#print(mainStr)
	return mainStr

#function that calls the sentence creator, updates the display, and scrolls the text
def updateText():
	global counter
	global dispStr
	global mainStr
	global blinkTime
	if counter >= len(mainStr):
		#this blinks the cursor at the end of typing
		if blinkTime <= 6:
			if (blinkTime % 2) == 0:
				dispStr = dispStr.replace("█", "")
				displayText.value = dispStr
				blinkTime += 1
			else:
				dispStr = dispStr + "█"
				displayText.value = dispStr
				blinkTime += 1
		else:			
			mainStr = ""
			typeSen()
			counter = 0
			dispStr = ""
			displayText.value = ""
			blinkTime = 0
	else:
		dispStr = dispStr.replace("█", "")
		dispStr = dispStr + mainStr[counter] + "█"
		displayText.value = dispStr
		counter += 1
		#print(dispStr)
		
#initiates the GUI
app = App(title="Infinite Scroll 2.0", bg = "#000000", layout = "grid", width = 640, height = 480)

#sets the logo
logo = Picture(app, image="logo.png", grid = [0, 1])
logo.tk.config(bd = 0, cursor = "none")

#main text display 
displayText = TextBox(app, text = "", multiline = True, grid = [0, 3])

#textBox properties 
displayText.font = "akkurat mono"
displayText.text_color = "#00ff00"
displayText.text_size = 50
displayText.align = "left"
displayText.tk.config(cursor = "none", bd = 50, highlightbackground = "#000000")
displayText.borderwidth = 0
displayText.height = 8
displayText.width = 16

#padding for logo
top_pad = Box(app, align = "left", height = 50, width = 5, grid = [0, 0])
bottom_pad = Box(app, align = "left", height = 1, width = 5, grid = [0, 2])

#calls updateText repeatedly in the app loop — gets new letters to pass to the GUI
app.repeat(200, updateText)

#sets the initial sentence 
typeSen()

#sets full screen
#app.set_full_screen()

#this is the main GUI loop
app.display()