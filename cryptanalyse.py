import os
import sys

src_dir = os.path.dirname( __file__ )
src_dir = os.path.join( src_dir,'src')
sys.path.append( src_dir )

import fichier
import cipher 
import time

# A scrypt that apply the Hill Climbing algorithm for the ngramme(passed as an arument ) 
# on the text (passed as an arument) 
# on the language (English or French) passed as arument (EN for English) (FR for French)
########################################################################################################

def clear():
     os.system('cls' if os.name == 'nt' else 'clear')

########################################################################################################

clear()
n=len(sys.argv)
if((n<=2) or (n>=5)):
      sys.exit("run by using command :\npython cryptanalyse.py  <n:NGRAMME> <./path/texte.txt> <language :EN or FR>\n")

########################################################################################################

cle_de_cryptage="WQAZSXCDERFVTYGHBNUJIKPLOM"
NBITERGLOB= 3000
NBITERSTATIC = 1500

DATA_PATH="./DATA"
text_path="./text"
path_statsEN = DATA_PATH+"/Dict_ngramm/stats_EN/"
path_statsFR = DATA_PATH+"/Dict_ngramm/stats_FR/"
score = 0

################################################################################################

def cryptanalyse(text,n,cle_depart,fitness,compare,Language):
    #(text : string )
    #(n : int )
    #(cle_depart : string ) length=26
    #(fitness : fun)
    #(compare : fun)
    #apply the Hill Climbing algorithm to the string(text) 
    #by using the function fitness to mesure the score of the text 
    #and using the function (compare) to compare the scores 
    #starting with the key (cle_depart) 
    if(Language=="EN"):
        path_stats=path_statsEN
    else :
        path_stats=path_statsFR
    

    dictionnaire=cipher.ngram(n,path_stats)
    dic1=cipher.ngram(1,path_stats)
    key=cipher.hillClimbing(fitness,text,dictionnaire,NBITERGLOB,NBITERSTATIC,cle_depart,compare)
    print("cle obtenu : "+key)
    print("\nSCORE OBTENU : " +str(fitness(cipher.decipher(text,key),dictionnaire)))
    print("corélation : " +str(cipher.fitness2(cipher.decipher(text,key),dic1)))

    return key


################################################################################################
 
text=fichier.NETTOYER_lire_fichier(sys.argv[2])
tps1 = time.time()
key=cryptanalyse(text,int(sys.argv[1]),cipher.alphabet,cipher.fitness1,cipher.comp1,sys.argv[3])
tps2 =  time.time()
print("time : "+str(tps2-tps1))
print(fichier.lire_fichier(text_path+"/textDECHIFRE.txt"))

########################################################################################################




    




