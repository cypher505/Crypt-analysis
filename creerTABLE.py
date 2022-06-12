import fichier 
import cipher 
import csv
import timeit
import os
path_stats = "./stats_GERMINAL/"
########################################################################################################
def clear():
     os.system('cls' if os.name == 'nt' else 'clear')
########################################################################################################
def creer_stats_ngram(text,n,cle_depart,fileNAME):
    clear()
    key=""
    global_BORN_inf=1000
    global_BORN_sup=10000
    static_BORN_inf=500
    static_BORN_sup=4000
    fichier.print_progress_bar(0,global_BORN_sup, "creer_stats_"+str(n)+"gram")
    with open(fileNAME, 'w+') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dictionaire=cipher.ngram(n,path_stats)
        static=static_BORN_inf
        glob=global_BORN_inf
        while glob<=global_BORN_sup:
            static=static_BORN_inf
            while static<=static_BORN_sup and static < glob:
                moyennelettres=0
                moyennescore=0
                nb_iter=10
                start = timeit.default_timer()
                for i in range (0,nb_iter) :
                    key=cipher.hillClimbing(cipher.fitness1,text,dictionaire,glob,static,cle_depart)
                    moyennelettres+=cipher.compare_cle(cle_de_cryptage,key)
                    moyennescore+=cipher.fitness1(cipher.decipher(text,key),dictionaire)
                stop = timeit.default_timer()
                filewriter.writerow([str(glob),str(static),str(moyennelettres/nb_iter)+"/26",str(moyennescore/nb_iter),str((stop - start)/nb_iter)])
                static+=250
            fichier.print_progress_bar(glob-global_BORN_inf, global_BORN_sup,"creer_stats_"+str(n)+"gram")
            glob+=500 
    clear()
    return key
########################################################################################################
cle_de_cryptage="QASZDEFRGTHYJUKILOMPWXCVBN"
text=fichier.NETTOYER_lire_fichier("./text/textCLAIRE.txt")
text=cipher.encipher(text,cle_de_cryptage)
creer_stats_ngram(text,2,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","./stats_optimales/iterations_optimales_BIGRAMS.csv")
creer_stats_ngram(text,3,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","./stats_optimales/iterations_optimales_TRIGRAMMES.csv")
creer_stats_ngram(text,4,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","./stats_optimales/iterations_optimales_TETRAGRAMMES.csv")
creer_stats_ngram(text,5,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","./stats_optimales/iterations_optimales_PENTAGRAMMES.csv")