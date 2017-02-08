import pickle
from random import randint, shuffle
from string import ascii_lowercase, punctuation
from collections import defaultdict
import click
from psutil import virtual_memory
import nltk
from nltk import word_tokenize

txtinput = ""

# Takes a sample text and finds words within them
def wordparse(txt):
    # Words are determined with spaces. Will add edge cases (links, punctuation) later
    words = word_tokenize(txt)
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
        try:
            worddict[words[i]][words[i+1]] += 1
        except KeyError:
            worddict[words[i]] = defaultdict(int)
            worddict[words[i]][words[i+1]] += 1
        # Adding addition context for articles by including the previous word
        if words[i] in articles and i > 0:
            try:
                worddict[(words[i], "article")][words[i-1]] += 1
            except KeyError:
                worddict[(words[i], "article")] = defaultdict(int)
                worddict[(words[i], "article")][words[i-1]] += 1

    wordpkl = open("worddict.pkl", "wb")
    pickle.dump(worddict, wordpkl, protocol=pickle.HIGHEST_PROTOCOL)
    wordpkl.close()
# A markov chain is a mathematical process in which a word, or some object, is taken and the probability of a next word is taken to predict the next word in the sequence. The words with a higher probability of appearing after the first word will, most likely, appear next. That process would be repeated for the second word until some end condition is met. For example, say the word "blue" is first. The words "car", "blanket", and "colored" have %50, %5, and %45 chance of appearing after the word "blue". Most likely the next word is "car" and "colored" having a slightly lower chance of appearing with "blanket" being the last. Say the next word is "blanket", then the process repeats again with "blanket"'s data.

def firstword():
    wordpkl = open("worddict.pkl", "rb")
    worddict = pickle.load(wordpkl)
    wordpkl.close()

    fwordlist = list(worddict.keys())
    return fwordlist[randint(0,len(fwordlist[:-1]))]
'''
@click.command()
@click.option("--maxwords", default=8, help="Maximum possible number of words in a sentence.")
@click.option("--minwords", default=4, help="Minimum number of words allowed in a sentence.")
'''
# Use probability with a number gen and convert dict to list, repeating a word multiple times based on their value. Number gen's range would be from 0 to size of list. It generates a number and that's the next word. 
# This function could and firstword() could be another file; these only generate the chain while wordparse() collects data.
def markovgen(startword, minwords=4, maxwords=8):
    chainoutput = []
    chainoutput.append(startword)
    
    wordpkl = open("worddict.pkl", "rb") 
    worddict = pickle.load(wordpkl)
    wordpkl.close()
    
    # Block for the first and second words
    try:
        worddata = worddict[startword]
        # A defaultdict of the second word in chain
    except KeyError:
        return "Chain failed, no data for {}".format(startword)

    for i in range(randint(minwords + 1, maxwords)):
        l1 = list(worddata.keys())
        l2 = []
        for w in l1:
            for j in range(worddata[w]):
                l2.append(w)
        chainword = l2[randint(0, len(l2[:-1]))]
        chainoutput.append(chainword)
        try:
            worddata = worddict[chainword]
        except KeyError:
            return "Chain failed, no data for chained word: {}".format(chainword)

    return " ".join(chainoutput)

print(markovgen(firstword()))
