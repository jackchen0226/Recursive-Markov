import parser
import pickle
from timeit import default_timer as timer

start = timer()

text = open('ALtext.txt', 'r')
parse = text.readlines()
'''
text = open("MobyDick.pkl", "rb")
parse = pickle.load(text)
text.close()
'''
parser.wordparse(parse[1])
end = timer()
print("Time elapsed: " + str((end - start) * 60))
