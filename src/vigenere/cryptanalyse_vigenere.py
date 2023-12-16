# Sorbonne Université 3I024 2021-2022
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : Zein SAKKOUR
# Etudiant.e 2 : Philemon WEHBE

import sys, getopt, string, math

# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

##############################################################################################################################

# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    """Lit un fichier et renvoie une chaîne de caractères."""
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)
##############################################################################################################################


# Chiffrement César
def chiffre_cesar(txt, key):
    """Parametre:
    (txt:str, key:int) -> str
    Chiffre une chaîne de caractères en utilisant la méthode de chiffrement de César avec une clé entière donnée.
    Il prend en entrée la chaîne de caractères à chiffrer et la clé de chiffrement et renvoie la chaîne de caractères chiffrée."""

    characters = string.ascii_uppercase
    if key < 0: key=26-(abs(key)%26)
    n = len(characters)
    #characters[key:]+characters[:key] gives us the new alphabet alphabet and maketrans translate the text
    new_alph = str.maketrans(characters, characters[key:]+characters[:key])
    translated_text = txt.translate(new_alph)    
    return translated_text

# Déchiffrement César
def dechiffre_cesar(txt, key):
    """Paramétre:
    (txt:str, key:int) -> str
    Déchiffre une chaîne de caractères chiffrée avec la méthode de chiffrement de César en utilisant une clé entière
    donnée. Il prend en entrée la chaîne de caractères à déchiffrer et la clé de déchiffrement
    et renvoie la chaîne de caractères déchiffrée."""
    characters = string.ascii_uppercase
    if key < 0: key=26-(abs(key)%26)
    n = len(characters)
    key = n - key # déchifré revient a chifré avec la clé inverse donc n - key
    new_alph = str.maketrans(characters, characters[key:]+characters[:key])
    translated_text = txt.translate(new_alph)    
    return translated_text


# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
    """Parametre :(txt:str, key:str) -> str
    Chiffre une chaîne de caractères en utilisant la méthode de chiffrement de Vigenère avec une clé donnée. 
    Il prend en entrée la chaîne de caractères à chiffrer et la clé de chiffrement 
    et renvoie la chaîne de caractères chiffrée."""
    n = 0
    chiffre=""
    for c in txt:
        k = key[n%len(key)]
        chiffre += chiffre_cesar(c,k)        
        n+=1
    return chiffre

# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
    """Parametre:
    (txt:str, key:str) -> str
    Déchiffre une chaîne de caractères chiffrée avec la méthode de chiffrement de Vigenère en utilisant une clé donnée. 
    Il prend en entrée la chaîne de caractères à déchiffrer et la clé de déchiffrement 
    et renvoie la chaîne de caractères déchiffrée."""
    n = 0
    dechiffre=""
    for c in txt:
        k = key[n%len(key)]
        dechiffre += dechiffre_cesar(c,k)        
        n+=1
    return dechiffre

# Analyse de fréquences
def freq(txt):
    """Parametre:(txt:str) -> List[float]
    Analyse la fréquence d'apparition des lettres dans une chaîne de caractères 
    et renvoie une liste des fréquences des lettres.
    """
    hist=[0.0]*len(alphabet)
    for c in txt:
        hist[ord(c)-ord('A')]+=1.0   
    return hist

##############################################################################################################################
# Fréquence moyenne des lettres en français
freq_FR = freq(read("germinal_nettoye")) #Fréquence du text germinal_nettoye
##############################################################################################################################


# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """Parametre:
    (txt:str) -> int
    Renvoie l'indice dans l'alphabet de la lettre la plus fréquente d'un texte donné."""
    hist=freq(txt)
    imax=0
    vmax=0.0
    for c in range(0,len(hist)):
        if(hist[c]>vmax):
            vmax=hist[c]
            imax=c
    return imax

# indice de coïncidence
def indice_coincidence(hist):
    """Parametre:
    (hist:List[float]) -> float
    Calcule l'indice de coïncidence pour une liste d'occurrences de lettres et renvoie sa valeur.

    """
    assert(hist!=[] and hist != [0.0 for i in range(26)])
    ic=0.0
    n=math.fsum(hist)
    if n==1:
        return 0.0
    for c in hist:
        ic+=((c)*(c-1))
    return ic/(n*(n-1))

# Recherche la longueur de la clé
def longueur_clef(cipher): 
    """Parametre:
    (cipher:str) -> int
    Recherche la longueur de la clé utilisée pour le chiffrement de Vigenère. 
    Il prend en entrée la chaîne de caractères chiffrée et renvoie la longueur de la clé si elle est trouvée, 
    sinon il renvoie -1."""
    max_key_length=20
    for key_length in range(1, max_key_length + 1):
        substrings = [cipher[i::key_length] for i in range(key_length)]
        ics = [indice_coincidence(freq(substring)) for substring in substrings]
        moy_ic = sum(ics) / len(ics)
        if moy_ic > 0.06:
            return key_length
    return -1 
#ABCDEF
    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher,key_length):
    """Parametre:
    (cipher:str, key_length:int) -> List[int]
    Renvoie le tableau des décalages probables étant donné la longueur de la clé 
    en utilisant la lettre la plus fréquente de chaque colonne."""
    substrings = [cipher[i::key_length] for i in range(key_length)]
    decalages=[]
    for substring in substrings:
        lettreFRmax=lettre_freq_max(substring)
        decalages.append((lettreFRmax-4)%26)  #4 = ord('E') -ord('A')
    return decalages

# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """Parametre:
    (cipher:str) -> str
    Renvoie le text déchifré en devinant la clé de chiffrement de Vigenere selon les methode 
    longueur_clef() et clef_par_decalages() """
    key_length=longueur_clef(cipher)
    key=clef_par_decalages(cipher,key_length)
    dechiffreTXT=dechiffre_vigenere(cipher,key)
    return dechiffreTXT

#On a réussi a déchiffrer 18 textes avec succès et le reste a échoué car on n'a pas bien deviné la longueur 
#de la clé 
# car la method de calcul du décalage avec la frequence max correspondant à E n'est pas optimale sur les petits textes ou le textes qui contien pas beaucoup de 0
################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1,h2,d):
    """
    Parametre:
        h1 (list[float]): Tableau de fréquence de lettres pour le premier texte.
        h2 (list[float]): Tableau de fréquence de lettres pour le deuxième texte.
        d (int): Décalage entre les lettres des deux tableaux.
    Calcule l'indice de coïncidence mutuelle (ICM) entre deux tableaux de fréquence de lettres.
    Returns:
        float: L'indice de coïncidence mutuelle entre les deux tableaux.
    Raises:
        AssertionError: Si les tableaux `h1` ou `h2` sont vides ou ne contiennent que des zéros.

    """

    assert(h1!=[] and h1 != [0.0 for i in range(26)])
    assert(h2!=[] and h2 != [0.0 for i in range(26)])
    icm=0.0
    n1=math.fsum(h1)
    n2=math.fsum(h2)
    for i in range(26):
        icm+=h1[i]*h2[(i+d)%26]
    return icm/(n1*n2)


def tableau_decalages_ICM(cipher, key_length):
    """
    Parametre:
        cipher (str): Texte chiffré.
        key_length (int): Longueur de la clé.
    Renvoie le tableau des décalages probables étant donné la longueur de la clé 
    en comparant l'indice de décalage mutuel par rapport à la première colonne
    Returns:
        list[int]: Tableau des décalages correspondants pour chaque position dans la clé.

    """
    decalages=[0]
    substrings = [cipher[i::key_length] for i in range(key_length)]
    for i in range(1, key_length):
        maxICM=0.0
        maxD=0
        for d in range(0,26):
            currICM=indice_coincidence_mutuelle(freq(substrings[0]),freq(substrings[i]),d)
            if currICM>maxICM:
                maxICM=currICM
                maxD=d
        decalages.append(maxD)
    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Parametre:
        cipher (str): Texte chiffré.

    Détermine la clé utilisée pour chiffrer un texte à l'aide de l'algorithme de Vigenère, puis déchiffre
    le texte chiffré à l'aide de la clé trouvée et renvoie le texte déchiffré.

    Returns:
        str: Texte déchiffré.

    """
    key_length = longueur_clef(cipher)
    decalages = tableau_decalages_ICM(cipher, key_length)
    cesar=dechiffre_vigenere(cipher,decalages)
    lettreFRmax=lettre_freq_max(cesar)
    return dechiffre_cesar(cesar,(lettreFRmax-4)%26)

################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(X,Y):
    """
    Calcule le coefficient de corrélation entre deux séries de données.

    Parametre:
        X (list): La première série de données.
        Y (list): La deuxième série de données.

    Returns:
        float: Le coefficient de corrélation entre les deux séries de données.

    """
    mX = math.fsum(X) / len(X)
    mY = math.fsum(Y) / len(Y)
    num = 0
    denX = 0
    denY = 0
    for i in range(len(X)):
        num += (X[i] - mX) * (Y[i] - mY)
        denX += (X[i] - mX) * (X[i] - mX)
        denY += (Y[i] - mY) * (Y[i] - mY)
    return num / math.sqrt(denX * denY)

# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """Parametre :
        (cipher: str, key_length: int) -> Tuple[float, List[int]]
        Calcule la clé de déchiffrement potentielle pour un texte chiffré avec une clé de longueur fixe donnée.
        
        Returns:
            Un tuple contenant :
            - score (float): le score moyen .
            - key (List[int]): une liste d'entiers représentant la clé de déchiffrement.
    """
    if key_length==0:
        return (0,0)
    key=[0 for i in range(key_length)]
    score=0.0
    substrings = [cipher[i::key_length] for i in range(key_length)]
    for i in range(0, key_length):
        maxCORR=0.0
        maxD=0
        for d in range(0,26):
            currCORR=correlation(freq_FR,freq(dechiffre_cesar(substrings[i],d)))
            if currCORR>maxCORR:
                maxCORR=currCORR
                maxD=d
        key[i]=maxD
        score += maxCORR
    score/=key_length
    return (score, key)

# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """(cipher: str) -> str:
    
    Déchiffre un texte chiffré avec un chiffrement de Vigenère en utilisant une attaque par analyse de fréquences.

    Parametre:
        cipher (str): le texte chiffré.

    Returns:
        Le texte déchiffré avec la clé de déchiffrement potentielle qui a le score de corrélation moyen le plus élevé parmi toutes les clés de longueur de 0 à 20.
    
    """
    decalage_max=(0.0,[])
    for d in range(21):
        decalage_curr=clef_correlations(cipher,d)
        if(decalage_curr[0]>decalage_max[0]):
            decalage_max=decalage_curr
    return dechiffre_vigenere(cipher,decalage_max[1])
    

################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TESTS D'EVALUATION
################################################################

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])
