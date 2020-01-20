import nltk.tag
from nltk.corpus import brown
import itertools
import pickle

def backoff_tagger(tagged_sents, tagger_classes, backoff=None):
    if not backoff:
        backoff = tagger_classes[0](tagged_sents)
        del tagger_classes[0]
 
    for cls in tagger_classes:
        tagger = cls(tagged_sents, backoff=backoff)
        backoff = tagger
 
    return backoff

brown_review_sents = brown.tagged_sents(categories=['reviews'], tagset = "universal")
brown_lore_sents = brown.tagged_sents(categories=['lore'], tagset = "universal")
brown_news_sents = brown.tagged_sents(categories=['news'], tagset = "universal")

brown_train = list(itertools.chain(brown_review_sents, brown_lore_sents, brown_news_sents))
 
raubt_tagger = backoff_tagger(brown_train, [nltk.tag.AffixTagger,
    nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],
    backoff=nltk.DefaultTagger('NOUN'))

templates = nltk.tag.brill.fntbl37()
 
#brill_trainer = nltk.tag.BrillTaggerTrainer(raubt_tagger, templates)
brill_trainer = nltk.tag.BrillTaggerTrainer(nltk.tag.ClassifierBasedPOSTagger(train=brown_train), templates)
braubt_tagger = brill_trainer.train(brown_train, max_rules=100, min_score=3)

#Check Accuracy
#print braubt_tagger.evaluate(conll_test)
#
#Save
f = open('tagger.pickle', 'wb')
pickle.dump(braubt_tagger, f)
f.close()
