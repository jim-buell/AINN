#Infinite Scroll 2.0

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from itertools import groupby
import random
from guizero import App, TextBox, Picture, Box, Window
import time
import re
import feedparser
import os
import tkinter
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import mixer

# Global variables that persist to facilitate GUI display refresh
# ——————————————————————————————————————————————————————

mainStr = ""
counter = 0
dispStr = ""
blinkTime = 0
wordWrap = 0
loadingCounter = 0
wordDict = {"NN": [""], "JJ": [""], "NNP": [""], "verbTrans": [""], "ideo": [""], "verbING": [""], "while": [""], "is": [""], "?": [""], "verbState": [""], "demo": [""]}
videoImage = ""
videoCount = 0
videoFetchOn = False

# Options for video, audio, and names
# ——————————————————————————————————————————————————————

	# The video option plays the video on startup if True.
videoBool = True

	# Puts IDEO names into word list 
ideoOn = False

	# Puts Demo names into the word list
demoOn = False

	# Turns sound on at start if true. videoBool must also be on. 
	# Will play sound every 20 minutes either way.
soundOn = True

	# How many headlines play before the video starts
headlinesInRow = 10

# Functions 
# ——————————————————————————————————————————————————————

def grabNewHeadlines():
	
	headlineList = []
	# Grab headlines from RSS feeds					
	rssNames = ["http://rss.cnn.com/rss/edition.rss", " https://www.japantimes.co.jp/feed", "http://feeds.washingtonpost.com/rss/national", "http://feeds.washingtonpost.com/rss/world"] #, "https://www.nytimes.com/svc/collections/v1/publish/http://www.nytimes.com/topic/destination/japan/rss.xml"]
	for item in rssNames:
		headlineLimit = 0
		rssSources='{}'.format(item)
		rssHeadlines = feedparser.parse(rssSources)

		Headlines = rssHeadlines['entries']
		for entries in Headlines:
			if headlineLimit < 20:
				if "news" in (entries['title']).lower():
					headlineList.append(f"{entries['title']}.")
					headlineLimit += 1
				else:
					headlineList.append(f"{entries['title']}.")
					headlineLimit += 1
	print(headlineList)
	
	#record time of headline fetch in milliseconds from epoch
	currentTime = round(time.time() * 1000)
	f = open("elapsedTime.txt", "w")
	timeStr = str(currentTime)
	f.write(timeStr)
	f.close()
	
	#append headlines to master file
#	f = open("masterHeadlines.txt", "a")
#	for element in headlineList:
#		f.write(element + "\n")
#	else:
#		f.close()
	
	#overwrite new headlines to new headline file
	headlineStrs = " "
	f = open("newHeadlines.txt", "w")
	for element in headlineList:
		f.write(element + "\n")
		headlineStrs += element
		headlineStrs += " "
	else:
		f.close()
	return headlineStrs

#categorizes words in headlines into parts of speech and saves them to individual files
def sortAndStore(part):
	
	typeList = []
	#add names of any static files here. Also add them to the global wordDict dictionary 
	staticFiles = ["verbTrans", "ideo", "verbING", "while", "is", "?", "verbState", "demo"]
	#open the file with the Headlines and put them in a str
	File = open(r"newHeadlines.txt", "r")
	headlineStrs = ""
	Lines = File.readlines()
	for item in Lines:
		headlineStrs = headlineStrs + " " + item.strip()
	#print(headlineStrs)
	stop_words = set(stopwords.words('english'))
	tokenized = sent_tokenize(headlineStrs)
	for i in tokenized:
		      
		#Word tokenizers is used to find the words 
		#and punctuation in a string
		wordsList = nltk.word_tokenize(i)
  
		#removing stop words from wordList
		wordsList = [w for w in wordsList if not w in stop_words] 
  
		# Using a Tagger. Which is part-of-speech 
		tagged = nltk.pos_tag(wordsList)
		
		groups = groupby(tagged, key=lambda x: x[1])
		typeNames = [[w for w,_ in words] for tag,words in groups if tag=="{}".format(part)]
		typeNames = [" ".join(name) for name in typeNames if len(name)>=0] 
		typeList += typeNames
	File.close()
	
	#overwrites new parts to file
	if not any(x in part for x in staticFiles):
		overWrite = "w"
		f = open("words/{}.txt".format(part), "{}".format(overWrite))
		for element in typeList:
			f.write(element + " \n")
		else:
			f.close()
	
	#add words to global wordDict
	#loads static words stored in files
	if any(x in part for x in staticFiles):
		wordDict["{}".format(part)] = []
		edgeFile = open("words/{}.txt".format(part), "r")
		listTemp = edgeFile.readlines()
		edgeList = []
		for item in listTemp:
			edgeList.append(item.strip())
		wordDict.update({"{}".format(part): edgeList})
		edgeFile.close()
	if part == "NN":
		for index, item in enumerate(typeList):
			#replaces any multi-word noun with []. Then removes all [] from list.
			if " " in item:
				typeList[index] = []
				newList = list(filter(lambda x: x, typeList))
		wordDict["{}".format(part)] = []
		wordDict.update({"{}".format(part): newList})
	else:
		for element in typeList:
			wordDict["{}".format(part)] = []
			wordDict.update({"{}".format(part): typeList})
	
#this function passes every part of speech to the main sortAndStore function	
def getAllTypes():
	typeList = ["JJ", "NN", "NNP", "verbTrans", "ideo", "verbING", "while", "is", "?", "verbState", "demo"]
	#old: "JJR", "JJS", "NNS","NNPS", "PDT", "RB", "RBR", "RBS", "RP", "VB", "VBG", "VBD", "VBN", "VBP", "VBZ"]	
	for item in typeList:
		sortAndStore("{}".format(item))

#gets a random word from a list of specified word types. Pass a str indicating the 
#part of speech to get that type of word. Returns a single word as str.
def getword(wordType):
	nextWord = wordDict["{}".format(wordType)][random.randrange(0, len(wordDict["{}".format(wordType)]))]
	return nextWord
	
#function that picks a sentence structure and then grabs random words to form a sentence
def typeSen():
	#sentence parts !MUST ALSO ADD TO getAllTypes() and global wordDict!
	if ideoOn == True:
		senParts = ["NN", "NNP", "NNP", "NNP", "NNP", "ideo"]
		proper = ["NNP", "NNP", "NNP", "NNP", "ideo"]
	if demoOn == True:
		senParts = ["NN", "NNP", "NNP", "NNP", "NNP", "demo"]
		proper = ["NNP", "NNP", "NNP", "NNP", "demo"]
	else:
		senParts = ["NN", "NNP", "NNP", "NNP", "NNP"]
		proper = ["NNP", "NNP", "NNP", "NNP"]
	
	#sentence structures 
	struct1 = [(proper[random.randrange(0, len(proper))]), "verbTrans", (senParts[random.randrange(0, len(senParts))])] 
	struct2 = [(proper[random.randrange(0, len(proper))]), "verbTrans", "JJ", "NN"] 
	struct3 = [(proper[random.randrange(0, len(proper))]), "verbTrans", (senParts[random.randrange(0, len(senParts))]), "while", "verbING", (senParts[random.randrange(0, len(senParts))])]
	struct4 = ["is", (proper[random.randrange(0, len(proper))]), "verbING", (proper[random.randrange(0, len(proper))]), "?"]
	struct5 = [(proper[random.randrange(0, len(proper))]), "verbTrans", (proper[random.randrange(0, len(proper))])]
	struct6 = [(proper[random.randrange(0, len(proper))]), "verbState", "while", "verbING", (senParts[random.randrange(0, len(senParts))])]
	
	allSentences = [struct1, struct2, struct3, struct4, struct5, struct6]
	
	#add words to the main string.
	global mainStr
	mainStr = ""
	wordSeq = allSentences[random.randrange(0, len(allSentences))]
	for item in wordSeq:
		if "?" in item:
			mainStr = mainStr[:-1] + getword("{}".format(item)) + " "
		else:
			addMe = getword("{}".format(item))
			mainStr = mainStr + addMe  + " "
	#mainStr = titlecase(mainStr)
	mainStr = mainStr.upper()
	if len(mainStr) >= 65:
		print("String was", len(mainStr), "characters long, so skipping.")
		print("The long string was: ", mainStr)
		typeSen()
	else:
#		mainStr = "123456789012345 1234567890123456 12345678901234567"
#		mainStr = "WEST DOOMS FORMER MISS USA CHESLIE KRYST "
		return mainStr

#function that updates the display, scrolls the text and calls the sentence creator when finished
def updateText():
	global counter
	global dispStr
	global mainStr
	global blinkTime
	global wordWrap
	global loadingCounter
	global videoCount
	global videoBool 
	global headlinesInRow
	if videoBool == True:
		playVideo()
	else:
		if counter == 0:
			displayText.value = ""
			displayText.tk.config(insertofftime = 0)
			displayText.tk.focus_force()
		if counter >= len(mainStr):	
			# Checks if cursor is at the end of a line and pushes it to next line if so
			# Ensures there isn't this weird tiny cursor stuck after the headline ends
			# If it's the last character of the last line, it leave the little cursor there				
			if "18" in displayText.tk.index(tkinter.INSERT):
				if not displayText.tk.index(tkinter.INSERT) == "5.18":
					dispStr = dispStr + "\n"
					displayText.value = dispStr			
			#this blinks the cursor at the end of typing
			if blinkTime <= 6:
				displayText.tk.config(insertofftime = 400)
				blinkTime += 1
			#resets everything for next headline
			else:			
				window.tk.focus_force()
				mainStr = ""
				displayText.value = ""
				typeSen()
				counter = 0
				dispStr = ""
				blinkTime = 0
				wordWrap = 0
				#plays the loading screen after x number of headlines
				loadingCounter += 1
				if loadingCounter >= headlinesInRow:
					videoBool = True
					loadingCounter = 0
		else:
			if wordWrap > 8 and (counter + 7) < len(mainStr):			
				#if it's been a lot of letters and there's a space, hit return
				if " " in mainStr[counter]:
					dispStr = dispStr + "\n"
					displayText.value = dispStr
					counter += 1
					wordWrap = 0
				#if there's been a lot of letters but no space yet, keep typing
				else:
					dispStr = dispStr + mainStr[counter]
					displayText.value = dispStr
					counter += 1
					wordWrap += 1
			else:
				dispStr = dispStr + mainStr[counter]
				displayText.value = dispStr
				counter += 1
				wordWrap += 1

#checks to see if headlines are more than 1 hours old and gets new if so	
def checkAge():
	global videoFetchOn
	f = open(r"elapsedTime.txt", "r")
	lastTime = int(f.read().rstrip())
	currentTime = round(time.time() * 1000)
	elapsedTime = (currentTime - lastTime)
	print("Elapsed time is", round((elapsedTime / 60000)), "minutes.")
	if elapsedTime >= 3600000:
		print("Headlines are more than an hour old. Need to get a new set.")
		videoFetchOn = True
	else:
		print("Keeping existing headlines.")

#turns headline to title case		
def titlecase(s):
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda word: word.group(0).capitalize(), s)
        
#plays the loading screen video
def playVideo():
	global videoCount 
	global videoBool
	global soundOn
	global videoFetchOn
	window.show()
	if videoFetchOn == True:
		print("Getting headlines during video")
		fetchNew()
		videoFetchOn = False
	if soundOn == True:
		if videoCount == 1:
			playSound()
	if videoCount <= 39:
		videoCount += 1
		if videoCount == 3 or videoCount == 21 or videoCount == 12:
			picture.value = "images/load1.png"
		if videoCount == 6 or videoCount == 24 or videoCount == 15 or videoCount == 33:
			picture.value = "images/load2.png"
		if videoCount == 9 or videoCount == 18 or videoCount == 27 or videoCount == 36:
			picture.value = "images/load3.png"
		if videoCount == 30:
			picture.value = "images/load4.png"
	if videoCount >= 39:
		videoBool = False
		window.hide()
		videoCount = 0
		picture.value = "images/load1.png"
		#resets focus to text box so insertion cursor is visible 
		displayText.tk.focus_set()
	
def fetchNew():
	grabNewHeadlines()
	getAllTypes()
	print("Fetched new headlines at", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

# gets called every hour. when true, the fetchNew function runs during video
def videoFetch():
	global videoFetchOn
	videoFetchOn = True	
	
#plays the startup chime
def playSound():
	global soundOn
	mixer.init()
	sound = mixer.Sound("audio/chime.ogg")
	sound.play()
	soundOn = False
    
def soundTimer():
	global soundOn
	soundOn = True
    
# GUIzero Properties 
# ————————————————————————————————————————————————————————————————————————————————————————————————————

#initiates the GUI
app = App(title = "Infinite Scroll 2.0", bg = "#000000", layout = "grid", width = 640, height = 480)
app.tk.config(cursor = "none")
app.full_screen = True

#sets full screen
app.set_full_screen()

#window for video 
window = Window(app, title = "", width = 640, height = 480, bg = "#000000", layout = "grid")
picture = Picture(window, image="images/load1.png", grid = [0, 0])

#window properties 
window.hide()
window.tk.config(cursor = "none")
window.full_screen = True

#sets the logo
logo = Picture(app, image="images/logo.png", grid = [1, 3])
logo.tk.config(bd = 0, cursor = "none")
logo.align = "left"
logo.tk.config(cursor = "none")

#padding for logo
top_pad = Box(app, align = "left", height = 30, width = 5, grid = [1, 0])
bottom_pad = Box(app, align = "left", height = 15, width = 5, grid = [1, 2])
left_pad = Box(app, align = "left", height = 30, width = 45, grid = [0, 0])

#top_pad.bg = "#ffffff"
#bottom_pad.bg = "red"
#left_pad.bg = "YELLOW"

#main text display 
displayText = TextBox(app, text = "", multiline = True, grid = [1, 1])

#textBox properties 
displayText.font = "GT America Mono"
displayText.text_color = "#00ff00"
displayText.text_size = 39
displayText.align = "left"
displayText.tk.grid(ipadx = 30)
displayText.tk.config(cursor = "none", highlightbackground = "#000000", bd = 0)
	# Insertion cursor options
displayText.tk.config(insertbackground = "#00ff00", blockcursor = True, insertofftime = 0)
#displayText.tk.focus_set()
displayText.tk.bind("<Key>", "pass")

displayText.height = 5
displayText.width = 16

# Main loop and scheduled functions
# ————————————————————————————————————————————————————————————————————————————————————————————————————

# Main Text Loop — Calls updateText repeatedly in the app loop — gets new letters to pass to the GUI and runs everything else...
app.repeat(200, updateText)

#gets new headlines every hour
app.repeat(3600000, videoFetch)

#plays sound with video every 20 minutes
app.repeat(1200000, soundTimer)

#startup sequences
#checks if new headlines needed on startup, loads words, and sets the initial sentence
checkAge()
getAllTypes()
typeSen()

#this is the main GUI loop
app.display()
