import csv
import sys
import decimal 
#A scrypt that creat a LATEX TABLE of stats from multiple .csv files (passed as arguments)


file_path="../DATA/DATA4LATEX/"

def CSV2LATEX(FILENAME,size):
    #(FILENAME : string) ends with .csv
    #(size : int ) number of colums
    #Creat a LATEX TABLE of stats from  FILENAME 


    currentLINE =0
    size-=1
    cmpglob=0
    mxLINE=[]
    mxVALUE=22
    colomNAME="Iteration GLOBALE & Iteration LOCAL  & Cle  & SCORE & TIME & Person"
    Fname=FILENAME.split("/")[-1]
    print(Fname)
    with open (file_path+"/TABLE_"+Fname+".txt",'w+') as tex:
        tex.write("\\begin{table}[]\n\centering \n\caption{"+(Fname.split("_")[-1]).split(".")[0]+"}\n\\vspace{10mm}\n\\begin{tabular}{|"+("l|"*(size+1))+"}\n\hline\n")
        currentLINE+=6
        tex.write(colomNAME+" \\\ \hline\n")
        currentLINE+=1
        LINE=""
        writ=0
        with open(FILENAME, 'r') as csvfile:
            file_reader = csv.reader(csvfile,delimiter=',')
            for row in  file_reader:
                cmp=0
                
                for e in row:
                    if(cmp!=size):
                        LINE+="\\textit{"+str(e)+"} & "
                        #tex.write("\\textit{"+str(e)+"} & ")
                        if(cmp==2): 
                            if(decimal.Decimal((e.split("/"))[0])>=0):
                                writ=1
                                cmpglob+=1
                                if(decimal.Decimal((e.split("/"))[0])>=mxVALUE):
                                #mxVALUE=decimal.Decimal((e.split("/"))[0])
                                    print(str(decimal.Decimal((e.split("/"))[0]))+"\n")
                                    mxLINE.append(currentLINE)
                            else :
                                writ =0
                            
                            
                    else :
                        
                        LINE+="\\textit{"+("%.5f" % decimal.Decimal(e))+"} \\\ \hline\n"
                            
                        #tex.write("\\textit{"+str(e)+"} \\\ \hline\n")
                        if writ==1 :
                            currentLINE+=1
                        
                    cmp+=1
                
                if(writ==1):
                    tex.write(LINE)
                    writ=0
                

                LINE=""
                if(cmpglob>33):
                    tex.write("\end{tabular}\n\end{table}")
                    tex.write("\\begin{table}[]\n\\begin{tabular}{|"+("l|"*(size+1))+"}\n\hline\n")
                    tex.write(colomNAME+" \\\ \hline\n")
                    currentLINE+=5
                    cmpglob=0

    contents=""
    with open (file_path+"/TABLE_"+Fname+".txt",'r+') as tex:    
        contents = tex.readlines()
        cmp=0
        for l in mxLINE:
            contents.insert(l+cmp, "\\rowcolor{green}\n")  # new_string should end in a newline
            cmp+=1
            tex.seek(0)  # readlines consumes the iterator, so we need to start over

    with open (file_path+"/TABLE_"+Fname+".txt",'w+') as tex:
    
        tex.writelines(contents)    
        tex.write("\end{tabular}\n\end{table}")
######################################################################################################################
n=len(sys.argv)
if(n<=1):
    sys.exit("run by using command :\npython CSV2LATEX.py  <./path/file1.csv> <./path/file2.csv> <..> ...\n")
    
for i in range(1,n): 
    CSV2LATEX(sys.argv[i],6)            


        
