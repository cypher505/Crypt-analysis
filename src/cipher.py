import fichier 
import math 
import random 
import numpy as np 
import matplotlib.pyplot as plt 
import os

if (os.path.exists("./text")==True) :
    text_path="./text"
else :
    text_path="../text"

alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
########################################################################################################

def txt(text):
    #(text : string )
    #puts a \n (new line ) evry 100 caracter in the string text
    
    
    cmp=0
    res=""
    for c in text:
        res+=c
        if cmp>=100:
            cmp=0
            res+="\n"
        else :
            cmp+=1
    return res
########################################################################################################

def encipher(text ,cle):
    #(text : string )
    #(cle : string ) length = 26 
    #encrypt the string (text) using the key (cle)
    
    
    res=""
    c=''
    for c in text:
        res+=cle[ord(c)-65]
    return res 

########################################################################################################

def decipher(ctext ,cle):
    #(ctext : string )
    #(cle : string ) length = 26 
    #decrypt the string (ctext) using the key (cle)
    
    
    res=""
    c=''
    
    for c in ctext:
        res+=chr(cle.index(c)+65)
        
        
    return res  

########################################################################################################

def genKey(cle,c):
    #(cle : string ) length = 26 
    #(c : int ) number of pairs to shuffle
    #exchange c eandom pairs between each other of the string cle  
    
    
    if(cle==""):                                    # Cas de base: generation d'une cle
        liste=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        shuffle=random.shuffle(liste)
        res="".join(shuffle)

    else:                                           # Modification de la cle existante
        l=list(cle)
        for i in range(0,c): 
            r1=1
            r2=1
            while(r1==r2):         
                r1=random.randint(0,25)
                r2=random.randint(0,25)
            
            tmp=l[r1]
            l[r1]=l[r2]
            l[r2]=tmp
        res = "".join(l)    
        
    return res

########################################################################################################

def fitness1(text,dictionaire): 
    #(text : string )
    #(dictionaire : dictionary )  
    #measures the score of the string (text) for each ngram substitution in the dictionary (dictionaire) 
    

    n=dictionaire["-n"]
    res=0
    liste=list(text)
    for x in range(len(text)-n):
        res+=math.log2(dictionaire.get("".join(liste[x:x+n]),10))
    return res

########################################################################################################

def fitness2(text,dico_langue): 
    #(text : string )
    #(dico_langue : dictionary )  
    #measures the Correlation Coefficient of the string (text) using the 1gramme from the dictionary (dictionaire) 


    dico_text = dict_mono_grams_de_texte(text)
    X=[v for k, v in dico_text.items() if k!="-n"]
    Y=[v for k, v in dico_langue.items() if k!="-n" ]
    # prend deux listes de meme taille
    # calcule la correlation lineaire de Pearson
    mX = math.fsum(X) / len(X)
    mY = math.fsum(Y) / len(Y)
    num = 0
    denX = 0
    denY = 0
    for i in range(len(X)):
        num = num + (X[i] - mX) * (Y[i] - mY)
        denX = denX + (X[i] - mX) * (X[i] - mX)
        denY = denY + (Y[i] - mY) * (Y[i] - mY)
    return num / math.sqrt(denX * denY)
    
########################################################################################################

def compare_cle(c1,c2):
    #(c1 : string ) length = 26 
    #(c2 : string ) length = 26 
    #compares the 2 strings c1 and c2 retrun the number of caracters that matches

 
    cmp=0
    cl1=list(c1)
    cl2=list(c2)
    for i in range(0,26):
        if(cl1[i]==cl2[i]):
            cmp+=1
    return cmp

########################################################################################################

def ngram(n,filepath):
    #(n : int )
    #(path : string )
    #returns the dictionary created by reading the file (filepath)


    d = dict()
    d=fichier.lire_ngrame(filepath+str(n)+"grams.txt")
    return d

########################################################################################################

def dict_mono_grams_de_texte(text): 
    #(text : string )
    #builds a dictionary with the occurrence of each letter in the string(text)


    dico = dict()
    
    for s in alphabet:
        dico[s]=0
    for i in text : 
        dico[i]+=1
    dico["-n"]=1
    return dico


########################################################################################################  

def comp1 (x,y):
    #compare x and y 
    return x<y

def comp2 (x,y):
    return (abs(x) > abs(y))
    
########################################################################################################  
 
def hillClimbing(fitness,text,dictionnaire,NBITERGLOB,NBITERSTATIC,cle,compare):
    #(fitness : fun)
    #(text : string)
    #(dictionnaire : dictionary )
    #(NBITERGLOB : int )
    #(NBITERSTATIC : int )
    #(cle : string ) length=26
    #(compare : fun)
    #apply the Hill Climbing algorithm to the string(text) 
    #by using the function fitness to mesure the score of the text 
    #and using the function (compare) to compare the scores 
    #starting with the key (cle) 


    scorePar=0
    cmpS=0   
    if cle == "":                                        # Compteur stationaire                                           
        clePar=genKey(cle,1)
    else : 
        clePar = cle
    deciphered=decipher(text,clePar)
    score_init=fitness(text,dictionnaire)                # Score du texte chiffré initial
    scorePar=fitness(deciphered,dictionnaire)
    i=0
    while i<NBITERGLOB and cmpS<NBITERSTATIC:
        cleEnf=genKey(clePar,1)
        deciphered=decipher(text,cleEnf)
        scoreEnf=fitness(deciphered,dictionnaire)
        if(compare (scorePar,scoreEnf)):
            scorePar=scoreEnf
            clePar=cleEnf
            cmpS=0
        else:                                       # Cas sans progression
            cmpS+=1
        i+=1
    #print("\nTEXTE CHIFFRE : \n"+text+"\n\n  Score initial : "+str(score_init)+"\n")
    #print("\nTEXTE DECHIFFRE : \n"+decipher(text,clePar)+"\n\n  Score final :  "+str(scorePar)+"\n  Cle appliquee : "+clePar)
    fichier.ecriture_fichier(text_path+"/textDECHIFRE.txt","text de depart: \n\n"+txt(text)+"\n\ntext obtenu:\n\n"+txt(decipher(text,clePar))+"\n\n Avec la cle :\n\n"+clePar+"\n\n")
    return clePar

######################################################################################################





