import fichier 
import math 
import random 

########################################################################################################
def encipher(text ,cle):
    res=""
    c=''
    for c in text:
        res+=cle[ord(c)-65]

    return res 
########################################################################################################
def decipher(ctext ,cle):
    res=""
    c=''
    for c in ctext:
        res+=chr(cle.index(c)+65)
        
    return res  
########################################################################################################
def genKey(cle,c):
    if(cle==""):                                    # Cas de base: generation d'une cle
        liste=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(liste)
        res="".join(liste)
        
    
    else:                                           # Modification de la cle existante
        res=cle
        l=list(cle)
        for i in range(0,c): #OU 3 ou 1?
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
    n=dictionaire["n"]
    res=0
    liste=list(text)
    for x in range(len(text)-n):
        res+=math.log2(dictionaire.get("".join(liste[x:x+n]),10))
    return res
########################################################################################################
def dict_mono_grams(text): # On construit un dictionnaire avec l'occurence de chaque lettre dans le texte 
    dico = dict()
    nblettre = 0
    res = text
    for i in res : 
        if i not in dico : 
            nblettre+=1
            dico[i]=1
        else :
            dico[i]= dico[i]+1
    for a in dico : 
        dico[a]= dico[a]/nblettre
    return dico
########################################################################################################
def fitness2(dico_text,dico_langue): 
    s1 = 0
    s2 =0
    s3= 0
    moyenne1= 0
    moyenne2= 0
    nb1=0
    nb2=0
    finale = 0
    for lettre in dico_text: 
        moyenne1 = moyenne1 + dico_text[lettre]
        nb1=nb1+1
    for lettre in dico_langue: 
        moyenne2 = moyenne2 + dico_langue[lettre]
        nb2=nb2+1
    moyenne1=moyenne1/nb1
    moyenne2=moyenne2/nb2
    
    for i in dico_text: 
        s1 = s1 + (dico_text[i]-moyenne1)*(dico_langue[i]-moyenne2)
        s2 = s2+ (dico_text[i]-moyenne1)**2
        s3= s3+(dico_langue[i]-moyenne2)**2
    finale = s1/(math.sqrt(s2)*math.sqrt(s3))
    return finale
########################################################################################################
def compare_cle(c1,c2):
    cmp=0
    cl1=list(c1)
    cl2=list(c2)
    for i in range(0,26):
        if(cl1[i]==cl2[i]):
            cmp+=1
    return cmp
########################################################################################################
def ngram(n,path):
    d = dict()
    d=fichier.lire_ngrame(path+str(n )+"grams.txt")
    return d
########################################################################################################    
def hillClimbing(fitness,text,dictionaire,NBITERGLOB,NBITERSTATIC,cle):
    
    scorePar=0
    cmpS=0                                          # Compteur stationaire
    clePar=genKey(cle,1)
    deciphered=decipher(text,clePar)
    score_init=fitness(text,dictionaire)                # Score du texte chiffré initial
    scorePar=fitness(deciphered,dictionaire)
    i=0
    while i<NBITERGLOB and cmpS<NBITERSTATIC:
        cleEnf=genKey(clePar,1)
        deciphered=decipher(text,cleEnf)
        scoreEnf=fitness(deciphered,dictionaire)
        if(scorePar < scoreEnf):                    # La cle enfant a un meilleur score fitness que la cle parent
            scorePar=scoreEnf
            clePar=cleEnf
            cmpS=0
        else:                                       # Cas sans progression
            cmpS+=1
        i+=1
        

    #print("\nTEXTE CHIFFRE : \n"+text+"\n\n  Score initial : "+str(score_init)+"\n")
    #print("\nTEXTE DECHIFFRE : \n"+decipher(text,clePar)+"\n\n  Score final :  "+str(scorePar)+"\n  Cle appliquee : "+clePar)
    fichier.ecriture_fichier("./text/textDECHIFRE.txt",decipher(text,clePar)+"\n Avec la cle :\n"+clePar)
    
    return clePar
########################################################################################################