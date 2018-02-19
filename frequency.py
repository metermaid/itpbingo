from collections import Counter
from nltk.corpus import stopwords
import nltk
import re

s = set(stopwords.words('english'))


text_file = open('common.txt', 'w')

results = file("results.txt", "r").read()

is_noun = lambda pos: pos[:2] == 'NN'
tokenized = nltk.word_tokenize(results.lower())
nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 

filtered_results = filter(lambda w: not w in s, nouns)

wordcount = Counter(filtered_results).most_common()

print wordcount
for k,v in  wordcount:
    text_file.write( "{} {}\n".format(k,v) )

text_file.close()