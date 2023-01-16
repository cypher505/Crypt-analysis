import os
import sys

src_dir = os.path.dirname( __file__ )
src_dir = os.path.join( src_dir, '..','src')
sys.path.append( src_dir )

import fichier
import cipher 
import time
########################################################################################################
cle_de_cryptage="WQAZSXCDERFVTYGHBNUJIKPLOM"
NBITERGLOB= 3000
NBITERSTATIC = 1500

DATA_PATH="../DATA"
text_path="../text"
path_stats = DATA_PATH+"/Dict_ngramm/stats_EN/"

score = 0
################################################################################################
def breakcrypt(text,n,cle_depart,fitness,compare):
    dictionnaire=cipher.ngram(n,path_stats)
    dic1=cipher.ngram(1,path_stats)
    key=cipher.hillClimbing(fitness,text,dictionnaire,NBITERGLOB,NBITERSTATIC,cle_depart,compare)
    print("  Clé  cryptage : "+cle_de_cryptage)
    print("\n  Lettres correctes : "+str(cipher.compare_cle(cle_de_cryptage,key))+"/26")
    print("SCORE OBTENU : " +str(fitness(cipher.decipher(text,key),dictionnaire)))
    print("\n  Score maximal : "+str(fitness(fichier.NETTOYER_lire_fichier(text_path+"/EN/txtCLAIRE_1500_EN.txt"),dictionnaire))+"\n")
    print("corélation : " +str(cipher.fitness2(cipher.decipher(text,key),dic1)))

    return key


################################################################################################

dictionnaire=cipher.ngram(1,path_stats)
text=fichier.NETTOYER_lire_fichier(text_path+"/EN/txtCLAIRE_1500_EN.txt")
text=cipher.encipher(text,cle_de_cryptage)

tps1 = time.time()
key=breakcrypt(text,5,cipher.alphabet,cipher.fitness1,cipher.comp1)
#print("corélation : " +str(cipher.fitness2(cipher.decipher(text,"ZAERQSFDWXCVHGBYTNUJPMILOK"),dictionnaire)))
#print("fit2: " +str(cipher.fitness2(cipher.decipher(text,key),dictionnaire)))
tps2 =  time.time()





    




