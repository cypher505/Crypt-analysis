import os
import sys

src_dir = os.path.dirname( __file__ )
src_dir = os.path.join( src_dir, '..','src')
sys.path.append( src_dir )


import fichier 
import cipher 
import csv
import timeit
DATA_PATH="../DATA"
path_stats = DATA_PATH+"/Dict_ngramm/stats_EN/"

#A scrypt to creat files of type .csv with the stats of the algorithm Hill Climbing produced by
#varying the variables NBITERGLOB and NBITERSTATIC 

########################################################################################################

def clear():
    #clear the screan
     os.system('cls' if os.name == 'nt' else 'clear')


    
########################################################################################################

def creer_stats_ngram(text,n,cle_depart,fileNAME):
    #(text : string )
    #(n : int )
    #(cle_depart : string ) length = 26
    #(fileNAME : string )
    #Creat stats by varying the variables NBITERGLOB and NBITERSTATIC in the algorithm Hill Climbing 
    #and writes them in a file of type .csv


    clear()
    key=""
    global_BORN_inf=2000
    global_BORN_sup=2200
    static_BORN_inf=1000
    static_BORN_sup=1200
    fichier.print_progress_bar(0,global_BORN_sup, "creer_stats_"+str(n)+"gram")
    with open(fileNAME, 'w+') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dictionaire=cipher.ngram(n,path_stats)
        dic1=cipher.ngram(1,path_stats)
        static=static_BORN_inf
        glob=global_BORN_inf
        while glob<=global_BORN_sup:
            static=static_BORN_inf
            while static<=static_BORN_sup and static < glob:
                moyennelettres=0
                moyennescore=0
                nb_iter=20
                start = timeit.default_timer()
                for i in range (0,nb_iter) :
                    key=cipher.hillClimbing(cipher.fitness1,text,dictionaire,glob,static,cle_depart,cipher.comp1)
                    moyennelettres+=cipher.compare_cle(cle_de_cryptage,key)
                    moyennescore+=cipher.fitness1(cipher.decipher(text,key),dictionaire)
                stop = timeit.default_timer()
                corr=str(cipher.fitness2(cipher.decipher(text,key),dic1))
                filewriter.writerow([str(glob),str(static),str(moyennelettres/nb_iter)+"/26",str('{:.3f}'.format(moyennescore/nb_iter)),str('{:.3f}'.format((stop - start)/nb_iter)),corr])
                static+=250
            fichier.print_progress_bar(glob-global_BORN_inf, global_BORN_sup,"creer_stats_"+str(n)+"gram")
            glob+=500 
    clear()
    return key

########################################################################################################

cle_de_cryptage="QASZDEFRGTHYJUKILOMPWXCVBN"
text=fichier.NETTOYER_lire_fichier("../text/EN/txtCLAIRE_1500_EN.txt")
text=cipher.encipher(text,cle_de_cryptage)
creer_stats_ngram(text,2,cipher.alphabet,DATA_PATH+"/stats_ngramm/stats_optimales_EN/iterations_optimales_BIGRAMS.csv")
creer_stats_ngram(text,3,cipher.alphabet,DATA_PATH+"/stats_ngramm/stats_optimales_EN/iterations_optimales_TRIGRAMMES.csv")
creer_stats_ngram(text,4,cipher.alphabet,DATA_PATH+"/stats_ngramm/stats_optimales_EN/iterations_optimales_TETRAGRAMMES.csv")
creer_stats_ngram(text,5,cipher.alphabet,DATA_PATH+"/stats_ngramm/stats_optimales_EN/iterations_optimales_PENTAGRAMMES.csv")

