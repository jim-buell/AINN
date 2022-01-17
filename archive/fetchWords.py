from newsapi import NewsApiClient
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from itertools import groupby

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
	
	#append headlines to master file
	f = open("masterHeadlines.txt", "a")
	for element in headlineList:
		f.write(element + "\n")
		print(element)
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
		      
		# Word tokenizers is used to find the words 
		# and punctuation in a string
		wordsList = nltk.word_tokenize(i)
  
		# removing stop words from wordList
		wordsList = [w for w in wordsList if not w in stop_words] 
  
		#  Using a Tagger. Which is part-of-speech 
		tagged = nltk.pos_tag(wordsList)
		
		groups = groupby(tagged, key=lambda x: x[1])
		typeNames = [[w for w,_ in words] for tag,words in groups if tag=="{}".format(part)]
		#if part == "NNPq":
		#	typeNames = [" ".join(name) for name in typeNames if len(name)>=2]
		#else:
		typeNames = [" ".join(name) for name in typeNames if len(name)>=0] 
		typeList += typeNames
	
	#write words to files — overwrites	
#	if "VB" or "VBG" or "VBD" or "VBN" or "VBP" or "VBZ" in part:
#		overWrite = "a"
#	else:
#		overWrite = "w"
	overWrite = "w"
	f = open("words/{}.txt".format(part), "{}".format(overWrite))
	for element in typeList:
		newStr = element.strip("'")
		f.write(newStr + " \n")
	else:
		f.close()
	print("{}".format(part) + ":", typeList)
	
#this function passes every part of speech to the main sortAndStore function	
def getAllTypes():
	typeList = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "PDT", "RB", "RBR", "RBS", "RP", "VB", "VBG", "VBD", "VBN", "VBP", "VBZ"]	
	for item in typeList:
		sortAndStore("{}".format(item))

def main():
	answer = input("Do you want to get new headlines? y or n ")
	if "y" in answer:
		print("Getting new headlines.")
		grabNewHeadlines()
	getAllTypes()
	
#this is the main function
main()