from appJar import gui
from itertools import chain
from glob import glob
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import re
import json as simplejson
from math import*
import operator
from appJar import gui
ps = PorterStemmer()

class TweetsUser:
    
    def __init__(self,nomFichier,ContenuFichier):
        self.nomFichier=nomFichier
        self.ContenuFichier=ContenuFichier
        ListeUsers.append(self)
        ListNomFichier.append(nomFichier)
        
def getUser():
    for s in ListeUsers:
        if s.nomFichier == app.getOptionBox("Users"):
            FichierAff=s.ContenuFichier[:]
            app.updateListBox("List", FichierAff, select=False, callFunction=True)

def removeDups(inputfile):
        lines=open(inputfile, 'r',encoding="utf8").readlines()
        lines_set = set(lines)        
        out=open(inputfile, 'w',encoding="utf8")
        for line in lines_set:
                out.write(line)
                
def press():
    d=traitementDBS()
    k=app.getOptionBox("Users")
    e="l'intérêt de l'utilisateur "+k+" est :"
    app.setLabel("Interest",e)
    app.setLabel("choix",d)


def similarity(X,Y):
     intersection_jar = len(set.intersection(*[set(X), set(Y)]))
     return intersection_jar/len(Y)

def calculLigneFichier(inputfile):
    i=0
    with open(inputfile,'r') as L:
        for line in L.readlines():
            i=i+1
    return i


def miniscul(inputfile):
        file=open(inputfile,'r',encoding="utf8")
        lines=[line.lower() for line in file]
        with open(inputfile, 'w', encoding="utf8") as out:
            out.writelines(sorted(lines))
            
def traitementDBS():
    filDB = []
    poids = [["Computer",0],["Games",0],["Arts",0],["Shopping",0],["Science",0],["Sports",0],["Recreation",0],["Society",0],["Health",0]]
    DBS = ["Computer","Games","Arts","Shopping","Science","Sports","Recreation","Society","Health"]
    for DB in DBS:
        file= open(DB, 'r', encoding="utf8")
        fil=[]
        lines=[line.lower() for line in file] #Lines is a list
        with open('BDDT.txt', 'w', encoding="utf8") as out:
            out.writelines(sorted(lines))
               #Remove Duplicate in BDDT.txt
        removeDups('BDDT.txt')
        stop_words=set(stopwords.words("english"))
        stop_words=list(stop_words)
        ponctuation=['``','.',',','--','_','==','!','?','$','...','(',')','[',']','{','}','-','_','=',':','…','”','scoop','grab','off',
                     'it','start','need','nominations','interview','secret','also','new','with','great','allows','cat','of','to','in','smokings','kids','specials'
                     'ran','flop','say','next','woke','up','bed','nap','cute','sweet','before','after','ever','amazing','smell'
                     'according','more','best','worst','time','morning','switching','all','tonight','differents','tomorrow','favorite',
                     'way','better','chance','year','more','please','hear','hour','day','say','more','from','depth','look','also',
                     'month','good','try','check','out','first','full','find','them','why','not','what','set','miss','high','low',
                     'never','always','away','go','where','dead','alive','could','key','thank','such',
                     'saturday','sunday','monday','tuesday','wednesday','thursday','friday','last','first','voting',
                     'january','february','march','april','may','june','july','august','september','october','november','december',
                     'or','maybe','can','blog','seeks','an','with','known','literally',
                     '2010','2011','2012','2013','2014','2015','2016','2017','2018']
        for p in ponctuation:
            stop_words.append(p)
        with open("BDDT.txt","r",encoding="utf8") as f :
            for line in f.readlines():
                result=result = re.sub(r"http\S+", "", line.strip())
                result1= re.sub(r"'\S+", "", result)
                result2= re.sub(r"@\S+", "", result1)
                result3 = re.sub(r"pic.\S+","",result2)
                words = word_tokenize(result3)
                for w in words:
                    if w not in stop_words:
                        fil.append(w)
        #construction représentant & stemming
        fil2= []
        for word in fil:
            fil2.append(ps.stem(word))
        fil2=list(set(fil2))
        fil2.insert(0,DB)
        filDB.append(fil2)
    
    miniscul(app.getOptionBox("Users"))
    fil4=[]
    fil5=[]
    filU=[]

    with open(app.getOptionBox("Users"),"r", encoding="utf8") as f:
        for line in f.readlines():
            print(line)
            result = re.sub(r"http\S+", "", line.strip())
            result1 = re.sub(r"'\S+", "", result)
            result2= re.sub(r"@\S+", "",result1)
            result3= re.sub(r"pic.\S+", "", result2)
            words= word_tokenize(result3)
            for p in ponctuation:
                stop_words.append(p)
            for word in words:
                if word not in stop_words:
                    fil4.append(word)
            for word in fil4:
                fil5.append(ps.stem(word))
            filU.append(fil5)
            fil4=[]
            fil5=[]
    with open(app.getOptionBox("Users"),"r", encoding="utf8") as F:
        for U, line in zip(filU, F.readlines()):
            simi=[[]]
            i=0
            for DB in filDB:
                simi[i].append(DB[0])
                simi[i].append(similarity(DB,U))
                simi.append([])
                i +=1
            simi.remove(simi[-1])
            simi.sort(reverse=True, key = operator.itemgetter(1))
            print(simi)
            if (simi[0][1]!= 0):
                B= open (simi[0][0], "a", encoding="utf8")
                #Ajout du tweet à la classe
                B.write('\n'+line)
                B.close()
                removeDups(simi[0][0])
                for poid in poids:
                    if poid[0] == simi[0][0]:
                        poid[1] += 1
    draw=[]
    interest=[]
    for x in poids:
        draw.append(x[1])
    poids.sort(reverse=True, key = operator.itemgetter(1))
    if (poids[0][1]==0):
        d=" N'a aucun intérêt particulier "
    else:
        S=calculLigneFichier(app.getOptionBox("Users"))
        print(S)
        if (S>=3):
            if (poids[0][1] >= S//3):
                for CLV in poids:
                    if (CLV[1] >= S//3):
                        interest.append(CLV[0])
                d = ', '.join(interest)
            else:
                interest.append(poids[0][0])
                for c in poids[1:]:
                    if poids[0][1]==c[1]:
                        interest.append(c[0])
                d =', '.join(interest)
        else:
            interest.append(poids[0][0])
            print(poids[1:])
            for c in poids[1:]:
                if poids[0][1]==c[1]:
                    interest.append(c[0])
                d=', '.join(interest)
            

    app.deleteAllTableRows("g1")
    app.addTableRow("g1",draw)
    return d

    
app=gui("Dig","1080x720")

k=int()

ListNomFichier=[]
listeNoms=["USER1","USER2","USER3Computer","USER4AllClass","testUserVide","USERTEST"]
ListeUsers=[]

#Création des classes
for s in listeNoms:
    list1=[]
    with open(s,"r") as f:
        for line in f.readlines():
            list1.append(line)
        TweetsUser(s,list1)


#startFrame
#Frame1
app.startFrame("LEFT",row=0, column=0)

draw=list()
app.setFont(16)
app.setBg("White")
app.setSticky("N")
#Menu
app.addOptionBox("Users",ListNomFichier)
app.setStretch("both")

#select option
app.setOptionBoxChangeFunction("Users", getUser)

FichierAff=list()
app.addEmptyLabel("Interest")
app.addEmptyLabel("choix")

app.addButton("Trouver l'intérêt", press)
app.stopFrame()
#Fin Frame1
#Frame2
app.startFrame("RIGHT",row =0, column=1)
app.setFont(size=15, family="Courier", underline=False)
#Ajouter listbox

app.addListBox("List",[])
app.setStretch("both")

app.stopFrame()

#Frame3
#Tableau
app.startFrame("SOUTH",row=3,colspan=2)
app.setSticky("EWS")
draw=[]
app.addTable("g1",
    [["Computer", "Games", "Arts","Shopping","Science","Sports","Recreation","Society","Health"],draw])
app.stopFrame()
app.go()
