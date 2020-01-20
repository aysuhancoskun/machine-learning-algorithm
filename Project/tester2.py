import nltk.corpus, nltk.tag, itertools
from nltk.tag import brill

brown_review_sents = nltk.corpus.brown.tagged_sents(categories=['reviews'], tagset="universal")
brown_lore_sents = nltk.corpus.brown.tagged_sents(categories=['lore'], tagset="universal")
brown_romance_sents = nltk.corpus.brown.tagged_sents(categories=['romance'], tagset="universal")
brown_train = list(itertools.chain(brown_review_sents[:1000], brown_lore_sents[:1000], brown_romance_sents[:1000]))
train_sents = list(itertools.chain(brown_review_sents[:1000], brown_lore_sents[:1000], brown_romance_sents[:1000]))
brown_test = list(itertools.chain(brown_review_sents[1000:2000], brown_lore_sents[1000:2000], brown_romance_sents[1000:2000]))
 
conll_sents = nltk.corpus.conll2000.tagged_sents(tagset="universal")
conll_train = list(conll_sents[:3000])
conll_test = list(conll_sents[3000:6000])
 
treebank_sents = nltk.corpus.treebank.tagged_sents(tagset="universal")
treebank_train = list(treebank_sents[:3000])
treebank_test = list(treebank_sents[3000:6000])

templates = nltk.tag.brill.fntbl37()

word_patterns = [
    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
    (r'.*ould$', 'MD'),
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*ness$', 'NN'),
    (r'.*ment$', 'NN'),
    (r'.*ful$', 'JJ'),
    (r'.*ious$', 'JJ'),
    (r'.*ble$', 'JJ'),
    (r'.*ic$', 'JJ'),
    (r'.*ive$', 'JJ'),
    (r'.*ic$', 'JJ'),
    (r'.*est$', 'JJ'),
    (r'^a$', 'PREP'),
]

def backoff_tagger(tagged_sents, tagger_classes, backoff=None):
    if not backoff:
        backoff = tagger_classes[0](tagged_sents)
        del tagger_classes[0]
 
    for cls in tagger_classes:
        tagger = cls(tagged_sents, backoff=backoff)
        backoff = tagger
 
    return backoff

ubt_tagger = backoff_tagger(train_sents, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
utb_tagger = backoff_tagger(train_sents, [nltk.tag.UnigramTagger, nltk.tag.TrigramTagger, nltk.tag.BigramTagger])
but_tagger = backoff_tagger(train_sents, [nltk.tag.BigramTagger, nltk.tag.UnigramTagger, nltk.tag.TrigramTagger])
btu_tagger = backoff_tagger(train_sents, [nltk.tag.BigramTagger, nltk.tag.TrigramTagger, nltk.tag.UnigramTagger])
tub_tagger = backoff_tagger(train_sents, [nltk.tag.TrigramTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger])
tbu_tagger = backoff_tagger(train_sents, [nltk.tag.TrigramTagger, nltk.tag.BigramTagger, nltk.tag.UnigramTagger])
ubta_tagger = backoff_tagger(train_sents, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger, nltk.tag.AffixTagger])
ubat_tagger = backoff_tagger(train_sents, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.AffixTagger, nltk.tag.TrigramTagger])
uabt_tagger = backoff_tagger(train_sents, [nltk.tag.UnigramTagger, nltk.tag.AffixTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
aubt_tagger = backoff_tagger(train_sents, [nltk.tag.AffixTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
aubtr_tagger = nltk.tag.RegexpTagger(word_patterns, backoff=aubt_tagger)
raubt_tagger = backoff_tagger(train_sents, [nltk.tag.AffixTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],backoff=nltk.tag.RegexpTagger(word_patterns))
cpos_tagger = nltk.tag.ClassifierBasedPOSTagger(train=brown_train)
brill_trainer = nltk.tag.BrillTaggerTrainer(nltk.tag.ClassifierBasedPOSTagger(train=brown_train), templates)
braubt_tagger = brill_trainer.train(brown_train, max_rules=100, min_score=3)
brill_trainer = nltk.tag.BrillTaggerTrainer(raubt_tagger, templates)
braubt1_tagger = brill_trainer.train(brown_train, max_rules=100, min_score=3)
brill_trainer = nltk.tag.BrillTaggerTrainer(nltk.tag.ClassifierBasedPOSTagger(train=brown_train), templates)
braubt2_tagger = brill_trainer.train(brown_train, max_rules=100, min_score=4)

print(ubt_tagger.evaluate(brown_test))
print(utb_tagger.evaluate(brown_test))
print(but_tagger.evaluate(brown_test))
print(btu_tagger.evaluate(brown_test))
print(tub_tagger.evaluate(brown_test))
print(tbu_tagger.evaluate(brown_test))
print(ubta_tagger.evaluate(brown_test))
print(ubat_tagger.evaluate(brown_test))
print(uabt_tagger.evaluate(brown_test))
print(aubt_tagger.evaluate(brown_test))
print(cpos_tagger.evaluate(brown_test))
print(braubt_tagger.evaluate(brown_test))
print(braubt1_tagger.evaluate(brown_test))
print(braubt2_tagger.evaluate(brown_test))

"""
print("------------------------------Tree Bank----------------------------")
ubt_tagger = backoff_tagger(treebank_train, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
utb_tagger = backoff_tagger(treebank_train, [nltk.tag.UnigramTagger, nltk.tag.TrigramTagger, nltk.tag.BigramTagger])
but_tagger = backoff_tagger(treebank_train, [nltk.tag.BigramTagger, nltk.tag.UnigramTagger, nltk.tag.TrigramTagger])
btu_tagger = backoff_tagger(treebank_train, [nltk.tag.BigramTagger, nltk.tag.TrigramTagger, nltk.tag.UnigramTagger])
tub_tagger = backoff_tagger(treebank_train, [nltk.tag.TrigramTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger])
tbu_tagger = backoff_tagger(treebank_train, [nltk.tag.TrigramTagger, nltk.tag.BigramTagger, nltk.tag.UnigramTagger])
ubta_tagger = backoff_tagger(treebank_train, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger, nltk.tag.AffixTagger])
ubat_tagger = backoff_tagger(treebank_train, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.AffixTagger, nltk.tag.TrigramTagger])
uabt_tagger = backoff_tagger(treebank_train, [nltk.tag.UnigramTagger, nltk.tag.AffixTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
aubt_tagger = backoff_tagger(treebank_train, [nltk.tag.AffixTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
aubtr_tagger = nltk.tag.RegexpTagger(word_patterns, backoff=aubt_tagger)
raubt_tagger = backoff_tagger(train_sents, [nltk.tag.AffixTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],backoff=nltk.tag.RegexpTagger(word_patterns))
cpos = nltk.tag.ClassifierBasedPOSTagger(train=treebank_train)
brill_trainer = nltk.tag.BrillTaggerTrainer(nltk.tag.ClassifierBasedPOSTagger(train=treebank_train), templates)
braubt_tagger = brill_trainer.train(treebank_train, max_rules=100, min_score=3)
brill_trainer = nltk.tag.BrillTaggerTrainer(raubt_tagger, templates)
braubt1_tagger = brill_trainer.train(brown_train, max_rules=100, min_score=3)
brill_trainer = nltk.tag.BrillTaggerTrainer(nltk.tag.ClassifierBasedPOSTagger(train=treebank_train), templates)
braubt2_tagger = brill_trainer.train(treebank_train, max_rules=100, min_score=4)

print(ubt_tagger.evaluate(treebank_test))
print(utb_tagger.evaluate(treebank_test))
print(but_tagger.evaluate(treebank_test))
print(btu_tagger.evaluate(treebank_test))
print(tub_tagger.evaluate(treebank_test))
print(tbu_tagger.evaluate(treebank_test))
print(ubta_tagger.evaluate(treebank_test))
print(ubat_tagger.evaluate(treebank_test))
print(uabt_tagger.evaluate(treebank_test))
print(aubt_tagger.evaluate(treebank_test))
print(cpos_tagger.evaluate(treebank_test))
print(braubt_tagger.evaluate(treebank_test))
print(braubt1_tagger.evaluate(treebank_test))
print(braubt2_tagger.evaluate(treebank_test))

print("------------------------------Conll2000----------------------------")
ubt_tagger = backoff_tagger(conll_train, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
utb_tagger = backoff_tagger(conll_train, [nltk.tag.UnigramTagger, nltk.tag.TrigramTagger, nltk.tag.BigramTagger])
but_tagger = backoff_tagger(conll_train, [nltk.tag.BigramTagger, nltk.tag.UnigramTagger, nltk.tag.TrigramTagger])
btu_tagger = backoff_tagger(conll_train, [nltk.tag.BigramTagger, nltk.tag.TrigramTagger, nltk.tag.UnigramTagger])
tub_tagger = backoff_tagger(conll_train, [nltk.tag.TrigramTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger])
tbu_tagger = backoff_tagger(conll_train, [nltk.tag.TrigramTagger, nltk.tag.BigramTagger, nltk.tag.UnigramTagger])
ubta_tagger = backoff_tagger(conll_train, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger, nltk.tag.AffixTagger])
ubat_tagger = backoff_tagger(conll_train, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.AffixTagger, nltk.tag.TrigramTagger])
uabt_tagger = backoff_tagger(conll_train, [nltk.tag.UnigramTagger, nltk.tag.AffixTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
aubt_tagger = backoff_tagger(conll_train, [nltk.tag.AffixTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
aubtr_tagger = nltk.tag.RegexpTagger(word_patterns, backoff=aubt_tagger)
raubt_tagger = backoff_tagger(train_sents, [nltk.tag.AffixTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],backoff=nltk.tag.RegexpTagger(word_patterns))
cpos_tagger = nltk.tag.ClassifierBasedPOSTagger(train=conll_train)
brill_trainer = nltk.tag.BrillTaggerTrainer(nltk.tag.ClassifierBasedPOSTagger(train=conll_train), templates)
braubt_tagger = brill_trainer.train(conll_train, max_rules=100, min_score=3)
brill_trainer = nltk.tag.BrillTaggerTrainer(raubt_tagger, templates)
braubt1_tagger = brill_trainer.train(conll_train, max_rules=100, min_score=3)
brill_trainer = nltk.tag.BrillTaggerTrainer(nltk.tag.ClassifierBasedPOSTagger(train=conll_train), templates)
braubt2_tagger = brill_trainer.train(conll_train, max_rules=100, min_score=4)

print(ubt_tagger.evaluate(conll_test))
print(utb_tagger.evaluate(conll_test))
print(but_tagger.evaluate(conll_test))
print(btu_tagger.evaluate(conll_test))
print(tub_tagger.evaluate(conll_test))
print(tbu_tagger.evaluate(conll_test))
print(ubta_tagger.evaluate(conll_test))
print(ubat_tagger.evaluate(conll_test))
print(uabt_tagger.evaluate(conll_test))
print(aubt_tagger.evaluate(conll_test))
print(cpos_tagger.evaluate(conll_test))
print(braubt_tagger.evaluate(conll_test))
print(braubt1_tagger.evaluate(conll_test))
print(braubt2_tagger.evaluate(conll_test))

print("---------------------------Regexp-----------------------------")
"""
       


       
