import pickle
import nltk
from nltk import word_tokenize
from string import punctuation
from collections import defaultdict
from random import randint

def wordparse(txt):
    if type(txt) == str:
        words = word_tokenize(txt)
    if type(txt) == list:
        # For already tokenized texts
        words = txt
    punct = tuple(list(punctuation))
    # Will filter links out later with regex
    for i in words:
        if i in punct:
            words.remove(i)
        
    text = nltk.Text(words)

    wordpkl = open("worddict.pkl", "rb")
    worddict = pickle.load(wordpkl)
    wordpkl.close()

    articles = ["the", "a", "an", "some", "not"]
    for i in range(len(words)-1):
        # Adding addition context for articles by including the previous word
        if words[i].lower() in articles and i > 0:
            try:
                worddict[words[i]][1][words[i+1]] += 1
                worddict[words[i]][2][words[i-1]] += 1
            except TypeError:
                worddict[words[i]] = {1 : worddict[words[i]], 2 : defaultdict(int)}
                worddict[words[i]][2][words[i-1]] += 1
            except KeyError:
                worddict[words[i]] = {1 : defaultdict(int), 2 : defaultdict(int)}
                worddict[words[i]][1][words[i+1]] += 1
                worddict[words[i]][2][words[i-1]] += 1
        else:
            try:
                worddict[words[i]][1][words[i+1]] += 1
            except KeyError:
                worddict[words[i]] = {1 : defaultdict(int)}
                worddict[words[i]][1][words[i+1]] += 1

    wordpkl = open("worddict.pkl", "wb")
    pickle.dump(worddict, wordpkl, protocol=pickle.HIGHEST_PROTOCOL)
    wordpkl.close()

def firstword():
    wordpkl = open("worddict.pkl", "rb")
    worddict = pickle.load(wordpkl)
    wordpkl.close()

    fwordlist = list(worddict.keys())
    return fwordlist[randint(0,len(fwordlist[:-1]))]
