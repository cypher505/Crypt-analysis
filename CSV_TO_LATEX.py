import csv

def CSV2LATEX(FILENAME,size):
    cmpglob=0
    with open ("./LATEX/table.txt",'w+') as tex:
        tex.write("\\begin{table}[]\n\\begin{tabular}{|l|l|l|l|l|}\n\hline\n")
        tex.write("Iteration GLOBALE & Iteration LOCAL  & Cle  & SCORE & TIME \\\ \hline\n")
        with open(FILENAME, 'r') as csvfile:
            file_reader = csv.reader(csvfile,delimiter=',')
            for row in  file_reader:
                cmp=0
                for e in row:
                    if(cmp!=size):
                        tex.write("\\textit{"+str(e)+"} & ")
                    else :
                        tex.write("\\textit{"+str(e)+"} \\\ \hline\n")
                    cmp+=1
                cmpglob+=1
                if(cmpglob>100):
                    tex.write("\end{tabular}\n\end{table}")
                    tex.write("\\begin{table}[]\n\\begin{tabular}{|l|l|l|l|l|}\n\hline\n")
                    tex.write("Iteration GLOBALE & Iteration LOCAL  & Cle  & SCORE & TIME \\\ \hline\n")
                    cmpglob=0

                    

                
        tex.write("\end{tabular}\n\end{table}")

CSV2LATEX("./stats_optimales/iterations_optimales_BIGRAMS.csv",4)            


        
