import pickle
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, RegexpParser, Tree
from nltk.corpus import wordnet as wn
from nltk.sem.drt import *

f = open('tagger.pickle', 'rb')
tagger = pickle.load(f)
f.close()
read_dexpr = DrtExpression.fromstring

def chunker(sent):
    cp = RegexpParser('''
        lVERB: {(<ADV>|<MD>)*<RB>?<V.*|W.*|IN>+<PRT>*<ADP>*<IN>*<TO>?}
        lVERB: {<MD>(?=<NOT>)}
        lVNEG: {<NOT>}
        lNOUN: {<JJ.*|NN.*|PRP.*|EX|NUM|X|RB.*>+}
        lNOUN: {<ADP|DET>*(?=<NOUN>)}
        lNOUN: {<RB>*(?=<MD>)}
        lNOUN: {<PRP>*(?=<V.*>)}
        lNOUN: {<DT>(?=<V.*|lVERB>)}
        lPNCD: {<\.>}
        lPNCC: {<,>}
        lGROUP1: {<DT>*<lNOUN><lVNEG>?<lVERB>+<lVNEG>?((<DT>*<lNOUN>)|<lPNCD>)?}
        lGROUP2: {<lVERB>+<lVNEG>?<DT>*<lNOUN>+(?=<lPNCD>)}
        lGROUP2: {<lGROUP1><lVERB><lVNEG>?<DT>*<lNOUN>}
        '''
    )
    return cp.parse(sent)

def wpos(tag):
    if tag.startswith('N'):
        return "n"
    elif tag.startswith('V'):
        return "v"
    elif tag.startswith('ADJ'):
        return "a"
    elif tag.startswith('ADV'):
        return "s"
    else:
        return "n"
    
def tagfix(tagged):
    fixed=[]
    for pair in xrange(len(tagged)):
        if tagged[pair][0] == "not":
            fixed.append((tagged[pair][0],"NOT"))
        elif tagged[pair][1] == "VBG" and tagged[pair+1][1].startswith("V"):
            fixed.append((tagged[pair][0],"JJ"))
        else:
            fixed.append(tagged[pair])
    return fixed

def list2str(inp):
    out=""
    for x in inp:
        out+=("_"+x)
    return out

def normalize(part):
    lem=WordNetLemmatizer()
    if type(part[0]) != tuple:
        return list2str([lem.lemmatize(x[0][0],pos=wpos(x[0][1])) for x in part])
    else:
        return list2str([lem.lemmatize(x[0],pos=wpos(x[1])) for x in part])

"""
g = open("reddit.txt","r")
for inp in g:
    record = chunker(tagfix(tagger.tag(word_tokenize(inp))))#.draw()
    for gtree in [x for x in record.subtrees(filter=lambda x: x.label() == 'lGROUP1')]:
        nouns = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lNOUN')]
        verbs = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lVERB')]
        if len(nouns)==2:
            drs1 = read_dexpr('([x, y], ['+normalize(nouns[0])+'(x), '+normalize(nouns[1])+'(y), '+normalize(verbs)+'(x, y)])')#.draw()
            print drs1

"""
inp = "dogs are animals."
record = chunker(tagfix(tagger.tag(word_tokenize(inp))))#.draw()
for gtree in [x for x in record.subtrees(filter=lambda x: x.label() == 'lGROUP1')]:
    nouns = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lNOUN')]
    verbs = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lVERB')]
    if len(nouns)==2:
        drs1 = read_dexpr('([x, y], ['+normalize(nouns[0])+'(x), '+normalize(nouns[1])+'(y), '+normalize(verbs)+'(x, y)])')#.draw()
        print str(drs1)
