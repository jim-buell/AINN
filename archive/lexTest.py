import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn



#print(wn.synset('dog.n.01').definition())

for synset in list(wn.all_synsets('v'))[:10]:
	print(synset)
    

