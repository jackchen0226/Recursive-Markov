import pandas as pd
import os
from random import randint, shuffle
from string import ascii_lowercase

txtinput = ""

# Takes a sample text and finds words within them
def wordparse(text):
    # Words are determined with spaces. Will add edge cases (links, punctuation) later
    words = text.split(" ")
    # Double space edge case; they become empty strings
    if "" in words:
        for i in range(words.count("")):
            words.remove("")

    for i in range(len(words)):
        # pth is the directory of the pickled file. Example of the word "Because" would be the path "b/e/because.pkl"
        # In case there are one letter words, it names directories of that letter twice. Example is that "a" is "a/a/a.pkl"
        try:
            pth = "{1}/{2}/{3}.pkl".format(words[i][0], words[i][1], words[i])
        except IndexError:
            pth = "{}/{}/{}.pkl".format(words[i], words[i], words[i])
        pth = pth.lower()

        if os.path.isfile(pth):
            m_words = pd.read_pickle(pth)
            m_words = m_words.to_dict()
            # Find if these words exist in a pickled format and if they do, adds data of proceeding words to dictionary as data for pandas Series
            
            if words[0] in m_words:
                m_words[words[i]] += 1
            else:
                m_words[words[i]] = 1
            
            m_words = pd.Series(m_words)
            m_words.to_pickle(pth)
            
        else:
        # If the pickled file does not exist, it would create one for data storage.
            md_words = {}
            md_words[words[i]] = 1
            
            md_words = pd.Series(md_words)
            md_words.to_pickle(pth)

# A markov chain is a mathematical process in which a word, or some object, is taken and the probability of a next word is taken to predict the next word in the sequence. The words with a higher probability of appearing after the first word will, most likely, appear next. That process would be repeated for the second word until some end condition is met. For example, say the word "blue" is first. The words "car", "blanket", and "colored" have %50, %5, and %45 chance of appearing after the word "blue". Most likely the next word is "car" and "colored" having a slightly lower chance of appearing with "blanket" being the last. Say the next word is "blanket", then the process repeats again with "blanket"'s data.
def firstword():
    alpha = string.ascii_lowercase
    w1, w2 = alpha[randint(1, 26)], alpha[randint(1, 26)]
    
    # The directories leading to the word without the actual .pkl file
    pth = "{1}/{2}/".format(w1, w2)
    firstwordlist = os.listdir(pth)
    firstwrd = firstwordlist[randint(0, len(firstwordlist))]
    
    return pth + firstwrd    

# Use probability with a number gen and convert dict to list, repeating a word multiple times based on their value. Number gen's range would be from 0 to size of list. It generates a number and that's the next word. 
def markovgen(fworddir):
    firstword = pd.read_pickle(fworddir)
    firstword.to_dict()

    

#markovgen(firstword())
