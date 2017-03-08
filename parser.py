import pickle
import nltk
from nltk import word_tokenize
from string import punctuation
from collections import defaultdict
from random import randint

def wordparse(txt):
    """A parser to collect data from a body of text or pretokenized text through the Natural Language ToolKit (NLTK). Data about the words are stored in a dictionary and pickled for hard storage and, theorectically, produces natural sentences with more information.
    
    Args:
        txt (str or int): A large body of text or a list of tokenized words.
        
    Returns:
        A pickled library in the same directory named worddict.pkl"""
    if type(txt) == str:
        words = word_tokenize(txt)
    if type(txt) == list:
        # For already tokenized texts
        words = txt
    punct = tuple(list(punctuation))
    punct.append('""')
    punct.appemd("''")
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
        # To-Do: make sure that if an article is detected, include the next few words until no article is detected and place unto sentence.
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
    """A simple function that finds and returns a random word from worddict
    
    Returns: A string of one of the keys of worddict.pkl"""
    wordpkl = open("worddict.pkl", "rb")
    worddict = pickle.load(wordpkl)
    wordpkl.close()

    fwordlist = list(worddict.keys())
    return fwordlist[randint(0,len(fwordlist[:-1]))]
