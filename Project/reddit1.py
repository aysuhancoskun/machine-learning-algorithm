import praw, pickle
from nltk import word_tokenize, RegexpParser

def bot_login():
    print "Loggin in..."
    r = praw.Reddit(client_id = "JXUypf3tAY6eXA",
    client_secret = "7bDh8aYyR5sNOWnCUFiDzohrcbk",
    user_agent = "comment reader test")
    print "Logged in!"
    return r

def run_bot(r):
    submission = r.submission("82fahc")
    process_comments(submission.comments)

def pftokenize(sent):
    return word_tokenize(sent.lower())

def tagtosem(sent):
    cp = RegexpParser('''
        NP: {<DET>? (<ADJ>|<ADV>)* <CONJ>* (<NOUN>|<NUM>|<X>|(<PRON> <PRT>))* <PRON>?}
        R:  {(<PRT> <VERB>?)* <A..>* <PRON>?}
        V:  {<VERB>*(<PRT>*|<VERB>)*}
        PNC:{<\.>}
        C:  {<ADP>}
        ''')
    return cp.parse(sent)
        
def process_comments(objects):
    for object in objects:
        if type(object).__name__ == "Comment":
            #print object.body.replace("\n","")
            print tagtosem(braubt_tagger.tag(pftokenize(object.body.replace("\n",""))))
            process_comments(object.replies) 
        elif type(object).__name__ == "MoreComments":
            pass
        
f = open('tagger.pickle', 'rb')
braubt_tagger = pickle.load(f)
f.close()

r = bot_login()
run_bot(r)
