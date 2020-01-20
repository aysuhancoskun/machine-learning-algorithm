import nltk
from Tkinter import *
from nltk import word_tokenize, RegexpParser, Tree
from nltk.stem.wordnet import WordNetLemmatizer
import winsound, os, time, webbrowser, subprocess, pickle, praw
from nltk.corpus import wordnet as wn
from nltk.sem.drt import *
import ttk
import tkFont as font
from PIL import Image, ImageTk
import tkFileDialog as filedialog
import tkMessageBox as messagebox
from nltk.draw import TreeWidget
from nltk.draw.util import *

global path
global link
global source
global nword
global nsent
global ngroup

f = open('ptagger.pickle', 'rb')
tagger = pickle.load(f)
f.close()

def chunker(sent):
    cp = RegexpParser('''
        lVERB: {(<ADV>|<MD>)*<RB>?<V.*|IN>+<PRT>*<ADP>*<IN>*<TO>?}
        lVERB: {<MD>(?=<NOT>)}
        lVNEG: {<NOT>}
        lNOUN: {<JJ.*|NN.*|PRP.*|EX|CD|X|RB.*>+}
        lNOUN: {<ADP|DET>*(?=<NOUN>)}
        lNOUN: {<RB>*(?=<MD>)}
        lNOUN: {<PRP>*(?=<V.*>)}
        lNOUN: {<DT>(?=<V.*|lVERB>)}
        lPNCD: {<\.>}
        lPNCC: {<,>}
        lGROUP1: {<DT>*<lNOUN><lVNEG>?<lVERB>+<lVNEG>?((<DT>*<lNOUN>)|<lPNCD>)?}
        lGROUP2: {<lVERB>+<lVNEG>?<DT>*(<lNOUN>+(?=<lPNCD>)|<lNOUN>+(?=$))}
        '''
    )
    return cp.parse(sent)

def pftokenize(sentence):
    global nword
    global nsent
    nsent += 1
    result = word_tokenize(multiple_replace(sentence))
    nword += len(result)
    return result

def process_comments(objects):
    read_dexpr = DrtExpression.fromstring
    outdir = open(path[:-1]+"\output.txt","w")
    outdir.write("Results:\n")
    outdir.write("    Chunks:\n")
    for object in objects:
        if type(object).__name__ == "Comment":
            for sent in sent_tokenize(object.body.replace("\n","")): 
                if sent[-1] == "." and sent.count(' ')>1:
                    record = chunker(tagger.tag(pftokenize(sent)))
                    outdir.write("    "+str(record)+"\n")
                    ng1=[]
                    for gtree in [x for x in record.subtrees(filter=lambda x: x.label() == 'lGROUP1')]:
                        nouns = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lNOUN')]
                        ng1=nouns[0]
                        verbs = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lVERB')]
                        if len(nouns)==2:
                            drs1 = read_dexpr('([x, y], ['+normalize(nouns[0])+'(x), '+normalize(nouns[1])+'(y), '+normalize(verbs)+'(x, y)])')#.draw()
                            outdir.write("    Logic:"+str(drs1)+"\n")
                    for gtree in [x for x in record.subtrees(filter=lambda x: x.label() == 'lGROUP2')]:
                        ngroup += 1
                        verbs = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lVERB')]
                        nouns = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lNOUN')]
                        if len(nouns)==1:
                            drs2 = read_dexpr('([x, y], ['+normalize(ng1)+'(x), '+normalize(nouns[0])+'(y), '+normalize(verbs)+'(x, y)])')#.draw()
                            outdir.write("    Logic:"+str(drs2)+"\n")
            process_comments(object.replies) 
        elif type(object).__name__ == "MoreComments":
            pass
    outdir.close()

def bot_login():
    print ("Loggin in...")
    r = praw.Reddit(client_id = "JXUypf3tAY6eXA",
    client_secret = "7bDh8aYyR5sNOWnCUFiDzohrcbk",
    user_agent = "comment reader test")
    print ("Logged in!")
    return r

def run_bot(r,sub):
    submission = r.submission(sub)
    process_comments(submission.comments)

def multiple_replace(text,write=False):
    patterns = {
        "'m" : " am",
        "'s" : " is",
        u"\u2019" : " i",
        "'re" : " are",
        "n't" : " not",
        "'d" : " would",
        "'ve": " have",
        "*" : "",
        "(" : "",
        ")" : ""
    } 
    regex = re.compile("(%s)" % "|".join(map(re.escape, patterns.keys())))
    tmp=regex.sub(lambda mo: patterns[mo.string[mo.start():mo.end()]], text)
    return tmp

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

def list2str(inp):
    out=""
    for x in inp:
        out+=("_"+x)
    return out

def normalize(part):
    lem=WordNetLemmatizer() 
    if type(part[0]) != tuple:
        return list2str([lem.lemmatize(x[0][0].replace("-","_"),pos=wpos(x[0][1])) for x in part])
    else:
        return list2str([lem.lemmatize(x[0].replace("-","_"),pos=wpos(x[1])) for x in part])

def reddit():
    webbrowser.open("http://www.reddit.com")

def cp():
    clipboardlink=master.clipboard_get()
    clips = str(clipboardlink)
    if clips.find('reddit.com') == -1:
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
        messagebox.showwarning("Link", "Link is invalid!" )
        return False

    url = str(clipboardlink)
    e1.delete(1.0, END)
    e1.insert(END, clipboardlink)

def reset():
    global source
    global path
    global link
    link = ' '
    path = ' '
    e1.delete(1.0, END)
    e2.delete(1.0, END)
    source.set(1)
    b1.configure(state=DISABLED)
    b2.configure(state=DISABLED)
    
def fold():
    location = filedialog.askdirectory()
    if location == "":
        return False
    location = location.replace("/" ,"\\")
    e2.delete(1.0, END)
    e2.insert(END, location)
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    messagebox.showinfo("Folder", location + " is selected for output" )

def mselect():
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    messagebox.showinfo("Selection", "Method " + str(method.get()) + " has been selected.")

def testcp():
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    messagebox.showinfo("Help", str(e1.get(1.0, END)))

def txt():
    fileloc = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text File","*.txt"),("All files","*.*")))
    if fileloc == "":
        return False
    fileloc = fileloc.replace("/" ,"\\")
    e1.delete(1.0, END)
    e1.insert(END, fileloc)
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    messagebox.showinfo("File", fileloc + " is selected for source" )

def sf():

    b2.configure(state=NORMAL)
    b1.configure(state=DISABLED)
    e1.delete(1.0, END)

def sl():

    b1.configure(state=NORMAL)
    b2.configure(state=DISABLED)
    e1.delete(1.0, END)

def sstring():
    b1.configure(state=DISABLED)
    b2.configure(state=DISABLED)
    e1.delete(1.0, END)
   

def show_entry_fields():
    global source
    global path
    global link
    global nword
    global nsent
    global ngroup
    nsent = 0
    nword = 0
    ngroup = 0
    path = str(e2.get(1.0, END))
    link = str(e1.get(1.0, END))
    if path=="\n":
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
        messagebox.showwarning("Folder", "Folder is invalid!" )
        return False
   
    sourcetype = source.get()

    if sourcetype == 1:
        if link == "\n":
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
            messagebox.showwarning("Input", "String is invalid!" )
            return False
        sts=int(time.time())
        #HERE
        cf = CanvasFrame()
        record = chunker(tagger.tag(pftokenize(link.lower())))
        read_dexpr = DrtExpression.fromstring
        outdir = open(path[:-1]+"\output.txt","w")
        outdir.write("Results:\n")
        outdir.write("    Chunks:"+str(record)+"\n")
        n1="tmp"
        ng1=[]
        for gtree in [x for x in record.subtrees(filter=lambda x: x.label() == 'lGROUP1')]:
            ngroup += 1
            nouns = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lNOUN')]
            ng1=nouns[0]
            verbs = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lVERB')]
            if len(nouns)==2:
                drs1 = read_dexpr('([x, y], ['+normalize(nouns[0])+'(x), '+normalize(nouns[1])+'(y), '+normalize(verbs)+'(x, y)])')
                outdir.write("    Logic:"+str(drs1)+"\n")
        for gtree in [x for x in record.subtrees(filter=lambda x: x.label() == 'lGROUP2')]:
            ngroup += 1
            verbs = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lVERB')]
            nouns = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lNOUN')]
            if len(nouns)==1:
                drs2 = read_dexpr('([x, y], ['+normalize(ng1)+'(x), '+normalize(nouns[0])+'(y), '+normalize(verbs)+'(x, y)])')#.draw()
                outdir.write("    Logic:"+str(drs2)+"\n")
        tc = TreeWidget(cf.canvas(), record)
        tc['yspace'] = 20
        tc['xspace'] = 15
        cf.add_widget(tc, 10, 10)
        cf.print_to_file('tree.ps')
        outdir.close()
        #HERE
        #Punctuation Count#
        with open(path[:-1]+"\output.txt","r") as myfile:
            punct = 0
            punct = myfile.read().count("lPNCD")
            nword = nword - punct
        #Punctuation Count#
        fts=int(time.time())
        pts=fts-sts
        print "Words count: " + str(nword)
        print "Sentences count: " + str(nsent)
        print "Groups count: " + str(ngroup)
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        messagebox.showinfo("Completed", "Analyzing process completed in " + time.strftime("%H:%M:%S", time.gmtime(pts)) + "..." + "\n" + "Words count: "+ str(nword) + "\n" + "Sentences count: "+ str(nsent) + "\n" + "Groups count: "+ str(ngroup)) 
        subprocess.Popen('explorer ' + path)

    if sourcetype == 2:
        if link == "\n":
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
            messagebox.showwarning("Input", "File is invalid!")
            return False
        txtlink = link
        txtlink = txtlink.replace("\\" ,"/")
        txtlink = txtlink.replace("\n" ,"")
        if txtlink == "\n":
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
            messagebox.showwarning("Input", "File String is invalid!" )
            return False
        sts=int(time.time())
        #HERE#
        read_dexpr = DrtExpression.fromstring
        outdir = open(path[:-1]+"\output.txt","w")
        #cf = CanvasFrame()
        #yof = -40
        data = ""
        with open(txtlink, 'r') as myfile:
            data=myfile.read().replace('\n', ' ')
            data=data.replace("[","")
            data=data.replace("]","")
            data=data.replace("(","")
            data=data.replace(")","")
        for sent in data.split("."):
            if len(sent)>1:
                  record = chunker(tagger.tag(pftokenize(sent)))
            #tc = TreeWidget(cf.canvas(), record)
            #tc['yspace'] = 20
            #tc['xspace'] = 15
            #yof = yof + 20 + tc.bbox()[3]
            #cf.add_widget(tc, 10, yof)
            outdir.write("Results:\n")
            outdir.write("    Chunks:\n")
            outdir.write("    "+str(record)+"\n")
            ng1=[]
            for gtree in [x for x in record.subtrees(filter=lambda x: x.label() == 'lGROUP1')]:
                ngroup += 1
                nouns = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lNOUN')]
                ng1=nouns[0]
                verbs = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lVERB')]
                if len(nouns)==2:
                    drs1 = read_dexpr('([x, y], ['+normalize(nouns[0])+'(x), '+normalize(nouns[1])+'(y), '+normalize(verbs)+'(x, y)])')#.draw()
                    outdir.write("    Logic:"+str(drs1)+"\n")
            for gtree in [x for x in record.subtrees(filter=lambda x: x.label() == 'lGROUP2')]:
                ngroup += 1
                verbs = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lVERB')]
                nouns = [x.leaves() for x in gtree.subtrees(filter=lambda x: x.label() == 'lNOUN')]
                if len(nouns)==1:
                    drs2 = read_dexpr('([x, y], ['+normalize(ng1)+'(x), '+normalize(nouns[0])+'(y), '+normalize(verbs)+'(x, y)])')#.draw()
                    outdir.write("    Logic:"+str(drs2)+"\n")
        outdir.close()
        #HERE#
        #Punctuation Count#
        with open(path[:-1]+"\output.txt","r") as myfile:
            punct = 0
            punct = myfile.read().count("lPNCD")
            nword = nword - punct
        #Punctuation Count#
        #cf.print_to_file('tree.ps')
        fts=int(time.time())
        pts=fts-sts
        print "Words count: " + str(nword)
        print "Sentences count: " + str(nsent)
        print "Groups count: " + str(ngroup)
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        messagebox.showinfo("Completed", "Analyzing process completed in " + time.strftime("%H:%M:%S", time.gmtime(pts)) + "..." + "\n" + "Words count: "+ str(nword) + "\n" + "Sentences count: "+ str(nsent) + "\n" + "Groups count: "+ str(ngroup))
        subprocess.Popen('explorer ' + path)

    if sourcetype == 3:
        if link.find('reddit.com') == -1:
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
            messagebox.showwarning("Source", "Source is invalid!" )
            return False
        sts=int(time.time())
        #HERE#
        r = bot_login()
        run_bot(r,link.split("/")[-3])
        #HERE#
        #Punctuation Count#
        with open(path[:-1]+"\output.txt","r") as myfile:
            punct = 0
            punct = myfile.read().count("lPNCD")
            nword = nword - punct
        #Punctuation Count#
        fts=int(time.time())
        pts=fts-sts
        print "Words count: " + str(nword)
        print "Sentences count: " + str(nsent)
        print "Groups count: " + str(ngroup)
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        messagebox.showinfo("Completed", "Analyzing process completed in " + time.strftime("%H:%M:%S", time.gmtime(pts)) + "..." + "\n" + "Words count: "+ str(nword) + "\n" + "Sentences count: "+ str(nsent) + "\n" + "Groups count: "+ str(ngroup))
        subprocess.Popen('explorer ' + path)

      
def help():
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    messagebox.showinfo("Help", "First of all, choose type of source...")
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    messagebox.showinfo("Help", "Then write the text or select input text file or paste Reddit URL...")
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    messagebox.showinfo("Help", "After that, choose output folder for analyze output, then press start...")

def abouta():
    webbrowser.open("http://atilim.edu.tr/")
 
def aboutp():
    webbrowser.open("https://www.python.org/")

def aboutr():
    webbrowser.open("http://about.reddit.com")

def aboutn():
    webbrowser.open("http://www.nltk.org/")
      
def aboutabout():
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    messagebox.showinfo("About", "CMPE494 Senior Project")


def qq():
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    result = messagebox.askquestion("Exit", "Are You Sure?")
    if result == 'yes':
        quit()

def prntall():
    global path
    global link
    global method
    print ("path = " + str(path))
    print ("link = " + str(link))
    print ("method = " + str(method.get()))

master = Tk(className =" Text Analyzer ")

frametop = Frame(master)
frametop.pack(fill=X, expand=1)
framesource = Frame(master)
framesource.pack(fill=X, expand=1)
frameoutput = Frame(master)
frameoutput.pack(fill=X, expand=1)
framebottom = Frame(master)
framebottom.pack(fill=X, expand=1)

#Font configs
helv32=font.Font(family='Helvetica', size=32)
helv18=font.Font(family='Helvetica', size=18)
helv12=font.Font(family='Helvetica', size=12)

#Image section start
au=Image.open("au.png")
nl=Image.open("nltk.png")
iau=ImageTk.PhotoImage(au)
inl=ImageTk.PhotoImage(nl)
Label(frametop, image=inl).pack(side=LEFT, fill=BOTH, expand=1, anchor=NW, padx=10, pady=10)
Label(frametop, text="  Text Analyzer  ", font=helv32).pack(side=LEFT, fill=BOTH, expand=1, anchor=N, padx=10, pady=10)
Label(frametop, image=iau).pack(side=LEFT, fill=BOTH, expand=1, anchor=NE, padx=10, pady=10)
#Image section end

#Initialize of text boxes
path = " "
link = " "

#Top menu section Starts
menu=Menu(master)
master.config(menu=menu)

#File Section
filemenu= Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open Reddit", command=reddit)
filemenu.add_command(label="Reset", command=reset)
filemenu.add_command(label="Select Output Folder", command=fold)
filemenu.add_command(label="Exit", command=qq)

#Help Section
helpmenu = Menu(menu, tearoff=False)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Help", command=help)

#About Section
aboutmenu = Menu(menu, tearoff=False)
menu.add_cascade(label="About", menu=aboutmenu)
aboutmenu.add_command(label="Atılım University", command=abouta)
aboutmenu.add_command(label="NLTK", command=aboutn)
aboutmenu.add_command(label="Python", command=aboutp)
aboutmenu.add_command(label="Reddit", command=aboutr)
aboutmenu.add_command(label="About", command=aboutabout)
#Top menu section ends...

#Text boxes
e1 = Text(framesource, font=helv12, height=1, wrap=NONE)
e2 = Text(frameoutput, font=helv12, height=1, wrap=NONE)

#Source section starts
Label(framesource, text="Source", font=helv18).pack(side=TOP, expand=1, anchor=W, padx=10, pady=10)
e1.pack(side=TOP, fill=X, expand=1, padx=10, pady=10)

global source
source = IntVar(value=1)

S3 = Radiobutton(framesource, text="Text String", font=helv12, variable=source, value=1, command = sstring).pack(side=LEFT, expand=1, anchor=W, padx=10, pady=10)
S2 = Radiobutton(framesource, text="Text File", font=helv12, variable=source, value=2, command = sf).pack(side=LEFT, expand=0, anchor=E, padx=10, pady=10)
b2 = Button(framesource, text='Select Text File', state=DISABLED, font=helv12, command = txt)
b2.pack(side=LEFT, expand=1, anchor=W, padx=10, pady=10)
S1 = Radiobutton(framesource, text="Web URL", font=helv12, variable=source, value=3, command = sl).pack(side=LEFT, expand=0, anchor=E, padx=10, pady=10)
b1 = Button(framesource, text='Paste Reddit URL', state=DISABLED, font=helv12, command = cp)
b1.pack(side=LEFT, expand=1, anchor=W, padx=10, pady=10)
#Source section ends

#Output section starts
Label(frameoutput, text="Output Location", font=helv18).pack(side=TOP, expand=1, anchor=W, padx=10, pady=10)
e2.pack(side=TOP, fill=X, expand=1, padx=10, pady=10)
SelectFolder = Button(frameoutput, text='Select Folder', font=helv12, command = fold)
SelectFolder.pack(side=RIGHT, expand=0, anchor=E, padx=10, pady=10)
#Output section ends

#Bottom buttons
Button(framebottom, text='Start', font=helv18, command = show_entry_fields, width = 10).pack(side=LEFT, expand=0, anchor=W, padx=10, pady=10)
Button(framebottom, text='Quit', font=helv18, command = qq, width = 10).pack(side=RIGHT, expand=0, anchor=E, padx=10, pady=10)

#Windows size
master.minsize(800,560)

   
mainloop( )
