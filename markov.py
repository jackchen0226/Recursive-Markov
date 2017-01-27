import pickle
import os
from random import randint, shuffle
from string import ascii_lowercase
import collections as coll

txtinput = ""

# Takes a sample text and finds words within them
def wordparse(text):
    # Words are determined with spaces. Will add edge cases (links, punctuation) later
    words = text.split(" ")
    # Double space edge case; they become empty strings
    if "" in words:
        for i in range(words.count("")):
            words.remove("")

    print(words[0])

    wordpkl = open("worddict.pkl", "rb")
    worddict = pickle.load(wordpkl)
    wordpkl.close()

    for i in range(len(words)-1):
        try:
            worddict[words[i]][words[i+1]] += 1
        except KeyError:
            worddict[words[i]] = coll.defaultdict(int)
            worddict[words[i]][words[i+1]] += 1
    wordpkl = open("worddict.pkl", "wb")
    pickle.dump(worddict, wordpkl, protocol=pickle.HIGHEST_PROTOCOL)
    wordpkl.close()
# A markov chain is a mathematical process in which a word, or some object, is taken and the probability of a next word is taken to predict the next word in the sequence. The words with a higher probability of appearing after the first word will, most likely, appear next. That process would be repeated for the second word until some end condition is met. For example, say the word "blue" is first. The words "car", "blanket", and "colored" have %50, %5, and %45 chance of appearing after the word "blue". Most likely the next word is "car" and "colored" having a slightly lower chance of appearing with "blanket" being the last. Say the next word is "blanket", then the process repeats again with "blanket"'s data.
'''
# Next two functions need to be changed to function with new dictionaries
def firstword():
    alpha = string.ascii_lowercase
    w1, w2 = alpha[randint(1, 26)], alpha[randint(1, 26)]
    
    # The directories leading to the word without the actual .pkl file
    pth = "{1}/{2}/".format(w1, w2)
    firstwordlist = os.listdir(pth)
    firstwrd = firstwordlist[randint(0, len(firstwordlist))]
    
    return pth + firstwrd    

# Use probability with a number gen and convert dict to list, repeating a word multiple times based on their value. Number gen's range would be from 0 to size of list. It generates a number and that's the next word. 
# This function could and firstword() could be another file; these only generate the chain while wordparse() collects data.
def markovgen(fworddir):
    firstword = pd.read_pickle(fworddir)
    firstword.to_dict()

    words = list(firstword.keys())
    randwords = []

    for i in words:
        for j in range(d[i]):
            randwords.append(i)

#markovgen(firstword())
'''