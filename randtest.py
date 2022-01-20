import random

def typeSen():
	#sentence parts
	senParts = ["NN", "NNP", "ideo"]
	
	#sentence structures 
	struct1 = [(senParts[random.randrange(0, len(senParts))]), "verbTrans", (senParts[random.randrange(0, len(senParts))])] 
	struct2 = ["{}".format(senParts), "verbTrans", "JJ", "{}".format(senParts)]
	struct3 = [ "JJ", "{}".format(senParts), "verbTrans", "JJ", "{}".format(senParts)]
	struct4 = [ "JJ", "{}".format(senParts), "verbTrans", "{}".format(senParts)]
	
	allSentences = [struct1]
	print(struct1)
	
typeSen()
