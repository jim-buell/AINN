#AI News Network

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from itertools import groupby
import random
from guizero import App, TextBox, Picture, Box, Window
import time
import feedparser
import os
import platform
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

# mac-specific code to get external files
def get_path(filename):
	
	name = os.path.splitext(filename)[0]
	ext = os.path.splitext(filename)[1]

	if platform.system() == "Darwin":
		from AppKit import NSBundle
		file = NSBundle.mainBundle().pathForResource_ofType_(name, ext)
		return file or os.path.realpath(filename)
	else:
		return os.path.realpath(filename)
	
# grabs headlines from RSS feeds and stores them in a local file for later processing. 
def grabNewHeadlines():
	
	# define relative file paths
	timeFile = get_path("words/elapsedTime.txt")
	newHeadlinesFile = get_path("words/newHeadlines.txt")

	headlineList = []
	# Grab headlines from RSS feeds					
	rssNames = ["http://rss.cnn.com/rss/edition.rss", "https://www.japantimes.co.jp/feed", "http://feeds.washingtonpost.com/rss/national", "http://feeds.washingtonpost.com/rss/world", "http://rss.cnn.com/rss/edition_entertainment.rss"] 
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
	for item in headlineList:
		print(item, "\n")
	# gets rid of ’s to prevent weird word combos
	headlineList = [i.replace("’s", ":") for i in headlineList]	
	
	# record time of headline fetch in milliseconds from epoch
	currentTime = round(time.time() * 1000)
	f = open(timeFile, "w", encoding="utf-8")
	timeStr = str(currentTime)
	f.write(timeStr)
	f.close()
	
	# overwrite new headlines to new headline file
	f = open(newHeadlinesFile, "w", encoding="utf-8")
	for element in headlineList:
		f.write(element + "\n")
	else:
		f.close()

# loads headlines from file, categorizes words into parts of speech, and stores them in a global dictionary
def sortAndStore(part):

	typeList = []
	# add names of any static files here. Also add them to the global wordDict dictionary 
	staticFiles = ["verbTrans", "ideo", "verbING", "while", "is", "?", "verbState", "demo"]
	
	# define relative file paths
	newHeadlinesFile = get_path("words/newHeadlines.txt")
	partFile = get_path("words/{}.txt".format(part))

	# open the file with the Headlines and put them in a str
	File = open(newHeadlinesFile, "r", encoding="utf-8")
	headlineStrs = ""
	Lines = File.readlines()
	for item in Lines:
		headlineStrs = headlineStrs + " " + item.strip()
	stop_words = set(stopwords.words("english"))
	tokenized = sent_tokenize(headlineStrs)
	for i in tokenized:
		      
		# Word tokenizers is used to find the words and punctuation in a string
		wordsList = nltk.word_tokenize(i)
  
		# removing stop words from wordList
		wordsList = [w for w in wordsList if not w in stop_words] 
  
		# Using a Tagger. Which is part-of-speech 
		tagged = nltk.pos_tag(wordsList)
		
		# joins words that should stay together 
		groups = groupby(tagged, key=lambda x: x[1])
		typeNames = [[w for w,_ in words] for tag,words in groups if tag=="{}".format(part)]
		typeNames = [" ".join(name) for name in typeNames if len(name)>=0] 
		typeList += typeNames
	File.close()
	
	# overwrites new parts to file
	if not any(x in part for x in staticFiles):
		overWrite = "w"
		f = open(partFile, "{}".format(overWrite), encoding="utf-8")
		for element in typeList:
			f.write(element + " \n")
		else:
			f.close()
	
	# loads static words stored in files and add words to global wordDict
	if any(x in part for x in staticFiles):
		wordDict["{}".format(part)] = []
		edgeFile = open(partFile, "r", encoding="utf-8")
		listTemp = edgeFile.readlines()
		edgeList = []
		for item in listTemp:
			edgeList.append(item.strip())
		wordDict.update({"{}".format(part): edgeList})
		edgeFile.close()
	if part == "NN":
		# for index, item in enumerate(typeList):
			#replaces any multi-word noun with []. Then removes all [] from list.
		#	if " " in item:
		#		typeList[index] = []
		typeList = list(filter(lambda x: x, typeList))
		wordDict["{}".format(part)] = []
		updatedList = [i.replace("'", "") for i in typeList] #remove leftover single quotes		
		wordDict.update({"{}".format(part): updatedList})
	else:
		for element in typeList:
			wordDict["{}".format(part)] = []
			newList = [i.replace("'", "") for i in typeList] #remove leftover single quotes
			wordDict.update({"{}".format(part): newList})
	
# passes every part of speech to the main sortAndStore function	
def getAllTypes():
	typeList = ["JJ", "NN", "NNP", "verbTrans", "ideo", "verbING", "while", "is", "?", "verbState", "demo"]
	for item in typeList:
		sortAndStore("{}".format(item))

# gets a random word from a list of specified word types. Pass a str indicating the 
# part of speech to get that type of word. Returns a single word as str.
def getword(wordType):
	nextWord = wordDict["{}".format(wordType)][random.randrange(0, len(wordDict["{}".format(wordType)]))]
	return nextWord
	
# function that picks a sentence structure and then grabs random words to form a sentence
def typeSen():
	# sentence parts !MUST ALSO ADD TO getAllTypes() and global wordDict!
	if ideoOn == True:
		senParts = ["NN", "NNP", "NNP", "NNP", "NNP", "ideo"]
		proper = ["NNP", "NNP", "NNP", "NNP", "ideo"]
	if demoOn == True:
		senParts = ["NN", "NNP", "NNP", "NNP", "NNP", "demo"]
		proper = ["NNP", "NNP", "NNP", "NNP", "demo"]
	else:
		senParts = ["NN", "NNP", "NNP", "NNP", "NNP"]
		proper = ["NNP", "NNP", "NNP", "NNP"]
	
	# sentence structures 
	struct1 = [(proper[random.randrange(0, len(proper))]), "verbTrans", (senParts[random.randrange(0, len(senParts))])] 
	struct2 = [(proper[random.randrange(0, len(proper))]), "verbTrans", "JJ", "NN"] 
	struct3 = [(proper[random.randrange(0, len(proper))]), "verbTrans", (senParts[random.randrange(0, len(senParts))]), "while", "verbING", (senParts[random.randrange(0, len(senParts))])]
	struct4 = ["is", (proper[random.randrange(0, len(proper))]), "verbING", (proper[random.randrange(0, len(proper))]), "?"]
	struct5 = [(proper[random.randrange(0, len(proper))]), "verbTrans", (proper[random.randrange(0, len(proper))])]
	struct6 = [(proper[random.randrange(0, len(proper))]), "verbState", "while", "verbING", (senParts[random.randrange(0, len(senParts))])]
	struct7 = ["JJ", "NN", "verbTrans", (proper[random.randrange(0, len(proper))])]
	struct8 = ["NN", "verbTrans", (proper[random.randrange(0, len(proper))])]
	struct9 = ["is", "JJ", "NN", "verbING", (proper[random.randrange(0, len(proper))]), "?"]
	struct10 = ["JJ", "NN", "verbState", "while", "verbING", (senParts[random.randrange(0, len(senParts))])]
	strcut11 = ["JJ", "NN", "verbTrans", "JJ", "NN"]

	allSentences = [struct1, struct2, struct3, struct4, struct5, struct6, struct7, struct8, struct9, struct10, strcut11]
	
	# add words to the main string.
	global mainStr
	mainStr = ""
	wordSeq = allSentences[random.randrange(0, len(allSentences))]
	for item in wordSeq:
		if "?" in item:
			mainStr = mainStr[:-1] + getword("{}".format(item)) + " "
		else:
			addMe = getword("{}".format(item))
			mainStr = mainStr + addMe  + " "
	mainStr = mainStr.upper() #makes string uppercase 
	# skips strings that might be too long for screen
	if len(mainStr) >= 65:
		print("String was", len(mainStr), "characters long, so skipping.")
		print("The long string was: ", mainStr)
		typeSen()
	else:
		return mainStr

# updates the display, scrolls the text and calls the sentence creator when finished
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
			# this blinks the cursor at the end of typing
			if blinkTime <= 6:
				displayText.tk.config(insertofftime = 400)
				blinkTime += 1
			# resets everything for next headline
			else:			
				window.tk.focus_force()
				mainStr = ""
				displayText.value = ""
				typeSen()
				counter = 0
				dispStr = ""
				blinkTime = 0
				wordWrap = 0
				# plays the loading screen after x number of headlines
				loadingCounter += 1
				if loadingCounter >= headlinesInRow:
					videoBool = True
					loadingCounter = 0
		else:
			if wordWrap > 8 and (counter + 7) < len(mainStr):			
				# if it's been a lot of letters and there's a space, hit return
				if " " in mainStr[counter]:
					dispStr = dispStr + "\n"
					displayText.value = dispStr
					counter += 1
					wordWrap = 0
				# if there's been a lot of letters but no space yet, keep typing
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

# checks to see if headlines are more than 1 hours old and gets new if so	
def checkAge():
	timeFile = get_path("words/elapsedTime.txt")
	global videoFetchOn
	f = open(timeFile, "r", encoding="utf-8")
	lastTime = int(f.read().rstrip())
	currentTime = round(time.time() * 1000)
	elapsedTime = (currentTime - lastTime)
	print("Elapsed time is", round((elapsedTime / 60000)), "minutes.")
	if elapsedTime >= 3600000:
		print("Headlines are more than an hour old. Need to get a new set.")
		videoFetchOn = True
	else:
		print("Keeping existing headlines.")
	f.close()
        
# plays the loading screen video
def playVideo():
	global videoCount 
	global videoBool
	global soundOn
	global videoFetchOn
	window.show()
	if videoFetchOn == True:
		print("\n", "New headlines:")
		fetchNew()
		videoFetchOn = False
	if soundOn == True:
		if videoCount == 1:
			playSound()
	if videoCount <= 39:
		videoCount += 1
		if videoCount == 3 or videoCount == 21 or videoCount == 12:
			picture.value = get_path("images/load1.png")
		if videoCount == 6 or videoCount == 24 or videoCount == 15 or videoCount == 33:
			picture.value = get_path("images/load2.png")
		if videoCount == 9 or videoCount == 18 or videoCount == 27 or videoCount == 36:
			picture.value = get_path("images/load3.png")
		if videoCount == 30:
			picture.value = get_path("images/load4.png")
	if videoCount >= 39:
		videoBool = False
		window.hide()
		videoCount = 0
		picture.value = get_path("images/load1.png")
		# resets focus to text box so insertion cursor is visible 
		displayText.tk.focus_set()
	
def fetchNew():
	grabNewHeadlines()
	getAllTypes()
	print("Fetched new headlines at", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

# gets called every hour. when true, the fetchNew function runs during video
def videoFetch():
	global videoFetchOn
	videoFetchOn = True	
	
# plays the startup chime
def playSound():
	global soundOn
	mixer.init()
	sound = mixer.Sound(get_path("audio/chime.ogg"))
	sound.play()
	soundOn = False

# gets called after a certain amount of time, switches the sound on, and then waits until the video is played  
def soundTimer():
	global soundOn
	soundOn = True
    
# GUIzero Properties 
# ————————————————————————————————————————————————————————————————————————————————————————————————————

# initiates the GUI
app = App(title = "Infinite Scroll 2.0", bg = "#000000", layout = "grid", width = 640, height = 480)
app.tk.config(cursor = "none")
app.full_screen = True

# sets full screen for the main app
app.set_full_screen()

# initiates the window for video and the pictures it shows 
window = Window(app, title = "", width = 640, height = 480, bg = "#000000", layout = "grid")
picture = Picture(window, image = get_path("images/load1.png"), grid = [0, 0])

# video window properties 
window.hide()
window.tk.config(cursor = "none")
window.full_screen = True

# sets the logo in the main app
logo = Picture(app, image = get_path("images/logo.png"), grid = [1, 3])
logo.tk.config(bd = 0, cursor = "none")
logo.align = "left"
logo.tk.config(cursor = "none")

# padding for logo
top_pad = Box(app, align = "left", height = 30, width = 5, grid = [1, 0])
bottom_pad = Box(app, align = "left", height = 15, width = 5, grid = [1, 2])
left_pad = Box(app, align = "left", height = 30, width = 45, grid = [0, 0])

# initiates the main text display 
displayText = TextBox(app, text = "", multiline = True, grid = [1, 1])

# textBox properties 
displayText.font = "GT America Mono"
displayText.text_color = "#00ff00"
displayText.text_size = 39
displayText.align = "left"
displayText.tk.grid(ipadx = 30)
displayText.tk.config(cursor = "none", highlightbackground = "#000000", bd = 0)
	# Insertion cursor options
displayText.tk.config(insertbackground = "#00ff00", blockcursor = True, insertofftime = 0)
	# displayText.tk.focus_set()
displayText.tk.bind("<Key>", "pass")
displayText.height = 5
displayText.width = 16

# Main loop and scheduled functions
# ————————————————————————————————————————————————————————————————————————————————————————————————————

# Main Text Loop — Calls updateText repeatedly in the app loop — gets new letters to pass to the GUI and runs everything else...
app.repeat(200, updateText)

# gets new headlines every hour
app.repeat(3600000, videoFetch)

# plays sound with video every 20 minutes
app.repeat(1200000, soundTimer)

# startup sequences
# checks if new headlines needed on startup, loads words, and sets the initial sentence
checkAge()
getAllTypes()
typeSen()

# main GUI loop
app.display()
