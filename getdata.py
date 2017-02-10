import parser
import pickle

text = open('ALtext.txt', 'r')
parse = text.readlines()
'''
text = open("MobyDick.pkl", "rb")
parse = pickle.load(text)
text.close()
'''
parser.wordparse(parse[2])
