#verbs

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from itertools import groupby

typeList = []
#open the file with the Headlines and put them in a str
File = open(r"masterHeadlines.txt", "r")
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
	typeNames = [[w for w,_ in words] for tag,words in groups if tag=="VBZ"]
	#if part == "NNPq":
	#	typeNames = [" ".join(name) for name in typeNames if len(name)>=2]
	#else:
	typeNames = [" ".join(name) for name in typeNames if len(name)>=0] 
	typeList += typeNames

f = open("words/verbsNews.txt", "w")
for element in typeList:
	f.write(element + " \n")
else:
	f.close()