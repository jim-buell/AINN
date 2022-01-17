#Infinite Scroll 2.0

from newsapi import NewsApiClient
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from itertools import groupby
import random
from guizero import App, TextBox, Picture, Box
import time
import re

#global variables that persist to facilitate GUI display refresh
mainStr = ""
counter = 0
dispStr = ""
blinkTime = 0
wordWrap = 0
wordDict = {"NN": [""], "JJ": [""], "NNP": [""], "verbTrans": [""]}

def grabNewHeadlines():
	# Init
	newsapi = NewsApiClient(api_key='2a547104c0d14649850d41b220871320')
	headlineList = []
	
	# Grab headlines from NewsAPI 
	sourceName = ['the-washington-post', 'CNN', 'BBC-news']
	for item in sourceName: 
		top_headlines = newsapi.get_top_headlines(sources='{}'.format(item))

		# Format the headlines and remove extra data 
		Headlines = top_headlines['articles']
		if Headlines:
				for articles in Headlines:
					#b = articles['title'][::-1].index("-")
					if "news" in (articles['title']).lower():
						headlineList.append(f"{articles['title']}.")
					else:
						headlineList.append(f"{articles['title']}.")
	print(headlineList)
	
	#record time of headline fetch in milliseconds from epoch
	currentTime = round(time.time() * 1000)
	f = open("elapsedTime.txt", "w")
	timeStr = str(currentTime)
	f.write(timeStr)
	f.close()
	
	#append headlines to master file
	f = open("masterHeadlines.txt", "a")
	for element in headlineList:
		f.write(element + "\n")
		#print(element)
	else:
		f.close()
	
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
	#open the file with the Headlines and put them in a str
	File = open(r"newHeadlines.txt", "r")
	headlineStrs = ""
	Lines = File.readlines()
	for item in Lines:
		headlineStrs = headlineStrs + " " + item.strip()
	#print(headlineStrs)
	stop_words = set(stopwords.words('english'))
	tokenized = sent_tokenize(headlineStrs)
	#
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
	
	#loads static words stored in files
	if "verbTrans" not in part:
		overWrite = "w"
		f = open("words/{}.txt".format(part), "{}".format(overWrite))
		for element in typeList:
			newStr = element.strip("'")
			f.write(newStr + " \n")
		else:
			f.close()
	
	#add words to global wordDict
	if "verbTrans" in part:
		wordDict["{}".format(part)] = []
		edgeFile = open("words/{}.txt".format(part), "r")
		listTemp = edgeFile.readlines()
		edgeList = []
		for item in listTemp:
			edgeList.append(item.strip())
		wordDict.update({"{}".format(part): edgeList})
		edgeFile.close()
	else:
		for element in typeList:
			wordDict["{}".format(part)] = []
			wordDict.update({"{}".format(part): typeList})
	
#this function passes every part of speech to the main sortAndStore function	
def getAllTypes():
	typeList = ["JJ", "NN", "NNP", "verbTrans"]
	#old: "JJR", "JJS", "NNS","NNPS", "PDT", "RB", "RBR", "RBS", "RP", "VB", "VBG", "VBD", "VBN", "VBP", "VBZ"]	
	for item in typeList:
		sortAndStore("{}".format(item))

def fetchNew():
	grabNewHeadlines()
	getAllTypes()
	print("Fetched new headlines at", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

#gets a random word from a list of specified word types. Pass a str indicating the 
#part of speech to get that type of word. 
def getword(wordType):
	nextWord = wordDict["{}".format(wordType)][random.randrange(0, len(wordDict["{}".format(wordType)]))]
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
	#mainStr = titlecase(mainStr)
	mainStr = mainStr.upper()
	#skips sentences that will cause the text to jump on the first line
	if len(mainStr) >= 17:
		if mainStr[16] == " ":
			print("skipping a 16er")
			typeSen()
	else:
		return mainStr

#function that updates the display, scrolls the text and calls the sentence creator when finished
def updateText():
	global counter
	global dispStr
	global mainStr
	global blinkTime
	global wordWrap
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
			wordWrap = 0
	else:
		if wordWrap > 7 and (counter + 8) < len(mainStr):			
			#if it's been a lot of letters and there's a space, hit return
			if " " in mainStr[counter]:
				dispStr = dispStr + "\n"
				dispStr = dispStr.replace("█", "")
				dispStr = dispStr + "█"
				displayText.value = dispStr
				counter += 1
				wordWrap = 0
			#if there's been a lot of letter but no space yet, keep typing
			else:
				dispStr = dispStr.replace("█", "")
				dispStr = dispStr + mainStr[counter] + "█"
				displayText.value = dispStr
				counter += 1
				wordWrap += 1
		else:
			dispStr = dispStr.replace("█", "")
			dispStr = dispStr + mainStr[counter] + "█"
			displayText.value = dispStr
			counter += 1
			wordWrap += 1
			#print(dispStr)

#checks to see if headlines are more than 1 hours old and gets new if so	
def checkAge():
	f = open(r"elapsedTime.txt", "r")
	lastTime = int(f.read().rstrip())
	currentTime = round(time.time() * 1000)
	elapsedTime = (currentTime - lastTime)
	print("Elapsed time is", round((elapsedTime / 60000)), "minutes.")
	if elapsedTime >= 3600000:
		print("Headlines are more than an hour old. Need to get a new set.")
		fetchNew()
	else:
		print("Keeping existing headlines.")

#turns headline to title case		
def titlecase(s):
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda word: word.group(0).capitalize(), s)
	
#initiates the GUI
app = App(title="Infinite Scroll 2.0", bg = "#000000", layout = "grid", width = 640, height = 480)

#sets the logo
logo = Picture(app, image="logo.png", grid = [1, 1])
logo.tk.config(bd = 0, cursor = "none")
logo.align = "left"

#main text display 
displayText = TextBox(app, text = "", multiline = True, grid = [1, 3])

#textBox properties 
displayText.font = "GT America Mono"
displayText.text_color = "#00ff00"
displayText.text_size = 50
displayText.align = "left"
displayText.tk.config(cursor = "none", highlightbackground = "#000000", bd = 0)
displayText.height = 8
displayText.width = 16

#padding for logo
top_pad = Box(app, align = "left", height = 30, width = 5, grid = [1, 0])
bottom_pad = Box(app, align = "left", height = 30, width = 5, grid = [1, 2])
left_pad = Box(app, align = "left", height = 30, width = 45, grid = [0, 0])

#calls updateText repeatedly in the app loop — gets new letters to pass to the GUI
app.repeat(200, updateText)

#gets new headlines every 2 hours
app.repeat(7200000, fetchNew)

#startup sequences
#checks if new headlines needed on startup, loads words, and sets the initial sentence
checkAge()
getAllTypes()
typeSen()

#sets full screen
#app.set_full_screen()

#this is the main GUI loop
app.display()