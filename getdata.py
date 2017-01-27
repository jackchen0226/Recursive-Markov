import markov

text = open("ALtext.txt", "r")
text = text.readlines()

markov.wordparse(text[0])

