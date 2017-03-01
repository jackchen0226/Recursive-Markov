import pickle
from random import randint, shuffle
from string import ascii_lowercase, punctuation
from collections import defaultdict
import click
from psutil import virtual_memory
import nltk
from nltk import word_tokenize
import parser
import time
from timeit import default_timer as timer

''' A markov chain is a mathematical process in which a word, or some object, is taken and the probability of a next word is taken to predict the next word in the sequence. The words with a higher probability of appearing after the first word will, most likely, appear next. That process would be repeated for the second word until some end condition is met. For example, say the word "blue" is first. The words "car", "blanket", and "colored" have %50, %5, and %45 chance of appearing after the word "blue". Most likely the next word is "car" and "colored" having a slightly lower chance of appearing with "blanket" being the last. Say the next word is "blanket", then the process repeats again with "blanket"'s data.'''
start = timer()
# Use probability with a number gen and convert dict to list, repeating a word multiple times based on their value. Number gen's range would be from 0 to size of list. It generates a number and that's the next word. 
# This function could and firstword() could be another file; these only generate the chain while wordparse() collects data.
funcRunning = [False]
def markovgen(minw : int, maxw : int, startword : str):
    """Uses markov chains to generate a sentence of variable length from a pickled dataset.
    
    Args:
        minw (int): The bare minimum amount of words in the sentence.
        maxw (int): The maximum amount of words allowed in the sentence
        startword (str): A starting word for the chain. The default is declared in genwrapper() as firstword() from the parser module.
        
    Returns:
        str: The generated sentence or an error of the chain failing if not enough data is present."""

    if minw >= maxw:
        maxw = minw
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

    for i in range(randint(minw, maxw)):
        l1 = list(worddata[1].keys())
        l2 = []
        for w in l1:
            # Clean this up, breaks when articles are listed!!!!
            for j in range(worddata[1][w]):
                l2.append(w)
                shuffle(l2)
        chainword = l2[randint(0, len(l2[:-1]))]
        chainoutput.append(chainword)
        # if the word appended is an article, do the process again
        
        if 2 in worddict[chainword]:
            l1 = list(worddict[chainword][1].keys())
            l2 = []
            for w in l1:
                for j in range(worddict[chainword][1][w]):
                    l2.append(w)
                    shuffle(l2)
            chainword = l2[randint(0, len(l2[:-1]))]
            chainoutput.append(chainword)

        try:
            worddata = worddict[chainword]
        except KeyError:
            return "Chain failed, no data for chained word: {}".format(chainword)
    funcRunning[0] = False
    return " ".join(chainoutput)
    
def markovRunning():
    """Measures the memory usage of markovgen() as it is running."""
    mems = [virtual_memory().used]
    while funcRunning[0]:
        mems.append(virtual_memory().used)
        time.sleep(0.001)
 #       if len(mems) > 1000000:
  #          break
    maxmem = max(mems)
    maxmem = maxmem / 1048576 
    print("The starting memory was {} megabytes".format(mems[0]/1048576))
    print("The highest memory marked was {} megabytes".format(maxmem))

@click.command()
@click.option('--minwords', default=4, help='Sets the minimum amount of words in a sentence')
@click.option('--maxwords', default=8, help='Sets the maximum possible words in a sentence')
def genwrapper(minwords, maxwords):
    """A wrapper for markovgen() for click implementation"""
    print(markovgen(minwords, maxwords, startword=parser.firstword()))

import threading

if __name__ == '__main__':
    tmem = threading.Thread(target=markovRunning)
    funcRunning[0] = True
    tmem.start()
    #genwrapper()
    print(markovgen(4, 8, startword=parser.firstword()))
    end = timer()
    print("Time elapsed: {} seconds".format((end - start)*60))
    tmem.join()    
