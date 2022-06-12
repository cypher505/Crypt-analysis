import fichier
import cipher 
########################################################################################################
cle_de_cryptage="AZERQSDFWXCVTGBYHNUJPMILOK"
NBITERGLOB= 3000
NBITERSTATIC = 1300
path_stats = "./stats_GERMINAL/"
################################################################################################
def cryptanalyse(text,n,cle_depart):
    dictionaire=cipher.ngram(n,path_stats)
    key=cipher.hillClimbing(cipher.fitness1,text,dictionaire,NBITERGLOB,NBITERSTATIC,cle_depart)
    print("  Clé  cryptage : "+cle_de_cryptage)
    print("\n  Lettres correctes : "+str(cipher.compare_cle(cle_de_cryptage,key))+"/26")
    print("\n  Score maximal : "+str(cipher.fitness1(fichier.NETTOYER_lire_fichier("./text/textCLAIRE.txt"),dictionaire))+"\n")
    return key
################################################################################################
cle="ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
text=fichier.NETTOYER_lire_fichier("./text/textCLAIRE.txt")
text=cipher.encipher(text,cle_de_cryptage)
cryptanalyse(text,3,"")

