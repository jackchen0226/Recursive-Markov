import pandas as pd
import os
import pickle

txtinput = ""

def wordparse(text):
    words = text.split(" ")
    for i in range(len(words)):
        pth = "{1}/{2}/{3}.pkl".format(words[0][0], words[0][1], words[0])
        if os.path.isfile(pth):
            m_words = pd.read_pickle(pth)
            if words[1] in m_words:
                m_words[words[1]] += 1
            else:
                m_words[words[1]] = 1
            m_words.to_pickle(pth)
