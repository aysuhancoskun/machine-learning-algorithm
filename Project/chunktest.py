from nltk import ChunkParserI, TrigramTagger
import nltk.corpus
import pickle
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.corpus import conll2000
import random

f = open('tagger.pickle', 'rb')
tagger = pickle.load(f)
f.close()
 
 
class TrigramChunkParser(ChunkParserI):
    def __init__(self, train_sents):
        # Extract only the (POS-TAG, IOB-CHUNK-TAG) pairs
        train_data = [[(pos_tag, chunk_tag) for word, pos_tag, chunk_tag in tree2conlltags(sent)] 
                      for sent in train_sents]
 
        # Train a TrigramTagger
        self.tagger = TrigramTagger(train_data)
 
    def parse(self, sentence):
        pos_tags = [pos for word, pos in sentence]
 
        # Get the Chunk tags
        tagged_pos_tags = self.tagger.tag(pos_tags)
 
        # Assemble the (word, pos, chunk) triplets
        conlltags = [(word, pos_tag, chunk_tag) 
                     for ((word, pos_tag), (pos_tag, chunk_tag)) in zip(sentence, tagged_pos_tags)]
 
        # Transform to tree
        return conlltags2tree(conlltags)
 
shuffled_conll_sents = list(conll2000.chunked_sents(tagset="universal"))
random.shuffle(shuffled_conll_sents)
train_sents = shuffled_conll_sents[:int(len(shuffled_conll_sents) * 0.9)]
trigram_chunker = TrigramChunkParser(train_sents)
print trigram_chunker.parse(tagger.tag(["this","explains","so","much","and","is","crazy","facinating"]))
