from nltk import word_tokenize
from nltk.tag import PerceptronTagger
from nltk.corpus import conll2000 as cn
import pickle
import time

train = cn.tagged_sents("train.txt")
test = cn.tagged_sents("test.txt")

pt = PerceptronTagger(load=False)
sts=int(time.time())
pt.train(list(train),nr_iter=10)

fts=int(time.time())
pts=fts-sts
print pts

f = open('ptagger.pickle', 'wb')
pickle.dump(pt, f)
f.close()

