import praw

def bot_login():
    print "Loggin in..."
    r = praw.Reddit(client_id = "JXUypf3tAY6eXA",
    client_secret = "7bDh8aYyR5sNOWnCUFiDzohrcbk",
    user_agent = "comment reader test")
    print "Logged in!"
    return r

def run_bot(r):
    #submissions = r.subreddit('todayilearned').rising(limit=1)
    #for sid in submissions:
    #    submission = r.submission(sid)
    #    process_comments(submission.comments,1)
    submission = r.submission("82fahc")
    process_comments(submission.comments,1)
        
def process_comments(objects,dpt):
    for object in objects:
        if type(object).__name__ == "Comment":
            print "    "*dpt+object.body.replace("\n","")
            #print "    "*dpt+"comment"
            print len(object.replies)
            process_comments(object.replies,dpt+1) # Get replies of comment
            # Do stuff with comment (object)
        elif type(object).__name__ == "MoreComments":
            # Get more comments at same level
            #process_comments(object.comments(),dpt) 
            pass

r = bot_login()
run_bot(r)
