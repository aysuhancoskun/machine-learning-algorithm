import nltk.corpus, nltk.tag, itertools
brown_review_sents = nltk.corpus.brown.tagged_sents(categories=['reviews'], tagset="universal")
brown_lore_sents = nltk.corpus.brown.tagged_sents(categories=['lore'], tagset="universal")
brown_romance_sents = nltk.corpus.brown.tagged_sents(categories=['romance'], tagset="universal")
brown_train = list(itertools.chain(brown_review_sents[:1000], brown_lore_sents[:1000], brown_romance_sents[:1000]))
train_sents = list(itertools.chain(brown_review_sents[:1000], brown_lore_sents[:1000], brown_romance_sents[:1000]))
brown_test = list(itertools.chain(brown_review_sents[1000:2000], brown_lore_sents[1000:2000], brown_romance_sents[1000:2000]))
 
conll_sents = nltk.corpus.conll2000.tagged_sents(tagset="universal")
conll_train = list(conll_sents[:4000])
conll_test = list(conll_sents[4000:8000])
 
treebank_sents = nltk.corpus.treebank.tagged_sents(tagset="universal")
treebank_train = list(treebank_sents[:1500])
treebank_test = list(treebank_sents[1500:3000])

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

       


       
