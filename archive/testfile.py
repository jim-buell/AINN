import random

typeList = ["tiny", "baby"]

part = "verbTrans"

wordDict = {"NN": [""], "JJ": [""], "NNP": [""], "verbTrans": ["hmm"]}

#add words to global wordDict
if "verbTrans" in part:
	print("hi")
	edgeFile = open("words/{}.txt".format(part), "r")
	listTemp = edgeFile.readlines()
	for item in listTemp:
		wordDict["{}".format(part)] = []
		wordDict.update({"{}".format(part): typeList})
		print(wordDict["verbTrans"])
else:
	for element in typeList:
		wordDict["{}".format(part)] = []
		wordDict.update({"{}".format(part): typeList})
		
print(wordDict)