import os
import sys

src_dir = os.path.dirname( __file__ )
src_dir = os.path.join( src_dir, '..','src')
sys.path.append( src_dir )
import fichier

data_path="../DATA/Dict_ngramm/creer_stats_script"

#a scrypt to creat our own ngramme stats from a text 

########################################################################################################
def next(ngram, n, c):
    if len(ngram) == n:
        return ngram[1 : n + 1] + c
    else:
        return ngram + c
########################################################################################################
def update_table(table, i, l):
    if i in table:
        table[i] += 1
    elif len(i) == l:
        table[i] = 1
########################################################################################################
def print_dico(D, fic):
    f = open(fic, "w")
    for i in D:
        print(i + " " + str(D[i]), file=f)
    f.close()
########################################################################################################
Monogram = {}
Bigram = {}
Trigram = {}
Tetragram = {}
Pentagram = {}
current_bigram = ""
current_trigram = ""
current_tetragram = ""
current_pentagram = ""
if len(sys.argv) == 2:
    fichier = sys.argv[1]
    f = open(fichier, "r")
else:
    f = sys.stdin
for ligne in f:
    for c in ligne:
        if c != "\n" and c.isalpha()==True:
            update_table(Monogram, c, 1)
            current_bigram = next(current_bigram, 2, c)
            update_table(Bigram, current_bigram, 2)
            current_trigram = next(current_trigram, 3, c)
            update_table(Trigram, current_trigram, 3)
            current_tetragram = next(current_tetragram, 4, c)
            update_table(Tetragram, current_tetragram, 4)
            current_pentagram = next(current_pentagram, 5, c)
            update_table(Pentagram, current_pentagram, 5)
if len(sys.argv) == 2:
    f.close()
print_dico(Monogram, data_path+"/nb_monograms_brut")
print_dico(Bigram, data_path+"/nb_bigrams_brut")
print_dico(Trigram, data_path+"/nb_trigrams_brut")
print_dico(Tetragram, data_path+"/nb_tetragrams_brut")
print_dico(Pentagram, data_path+"/nb_pentagrams_brut")