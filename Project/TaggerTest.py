import nltk.tag
from nltk.corpus import brown
from nltk import word_tokenize, RegexpParser
import pickle
import itertools

f = open('tagger.pickle', 'rb')
braubt_tagger = pickle.load(f)
f.close()

def pftokenize(sent):
    return [word for word in word_tokenize(sent.lower())]

def tagtosem(sent):
    cp = nltk.RegexpParser('''
        P:  {<PRON> <PRT>}
        NP: {<DET>? <A..>* <CONJ>* (<NOUN>|<NUM>)* <PRON>?}
        R:  {(<PRT> <VERB>?)* <A..>* <PRON>?}
        V:  {<VERB>*}
        PNC:{<\.>}
        ''')
    return cp.parse(sent)
            
cmd = ''
while cmd != 'quit':
    sent = raw_input("Enter sentence:")
    if sent != 'quit':
        print tagtosem(braubt_tagger.tag(pftokenize(sent)))
