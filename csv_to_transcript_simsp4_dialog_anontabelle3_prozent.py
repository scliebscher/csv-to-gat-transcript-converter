# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 17:27:09 2018

@author: GERD
"""
import io
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import chardet
import os

root = tk.Tk()
root.withdraw()
cwd = os.getcwd()

def get_enc(file):
    rawdata = open(file, 'rb').read()
    result = chardet.detect(rawdata)
    charenc = result['encoding']
    return charenc
    
    

def dress_line(text,off=0,opos=0):
    #wenn der feldtrenner im text vorkommt, werden zeichenkettentrenner eingesetzt
    text = text.replace('"','')
    
    #wenn feldtrenner im text vorkommt, pech gehabt!!!
    line = text.split("%")
    if len(line) == 1:
        line = text.split(",")

    #get rid of unnecessary line breaks and spaces at the end of the line
    if line[3][-1:] =="\n":
        line[3] = line[3][:-1]
    if line[3][-1:] ==" ":
        line[3] = line[3][:-1]
    
    #sprechermarkierungen und namen ersetzen
    for sp in sps:
        line[2]=re.sub(r"\b%s\b" % sp[0],sp[1],line[2])
    
    for anon in anons:
        line[3]=re.sub(r"\b%s\b" % anon[0],anon[1],line[3])
    
    line[3]=" "*opos+line[3]
    if line[0]=="":
        line[0] = timelen*" "
    else:
        line[0] = ("{" + line[0] + "}").ljust(timelen)
    line[1] = (str(i+startn+off).zfill(nlen-3)).ljust(nlen)
    if line[2]=="":
        line[2] = (splen)*" "
    else:
        line[2] = (line[2]+":").ljust(splen)
            
    return line
    
def rest_line(text):
    line = text.split("%")
    line[0] = timelen*" "
    line[1] = nlen*" "
    line[2] = (splen)*" "
    return line

#mypath="//dfs\OMNIBUS\gruppen\AG-Meseth\Arbeitsordner\Blista Wiss Begl\Daten\Transkriptionen\in Arbeit"
messagebox.showinfo("Transkript auswählen","Wählen Sie ein Transkript im .csv-Format zum Konvertieren aus.")
file_path = filedialog.askopenfilename(initialdir = cwd,title = "Transkript auswählen")
if file_path[-4:]!=".csv":
    messagebox.showerror("Error", "Die ausgewählte Datei muss eine Tabelle im .csv-Format sein.")
else:
    file_enc = get_enc(file_path)
    print(file_enc)    
    #anonymisierungstabelle laden    
    messagebox.showinfo("Anonymisierungstabelle auswählen","Wählen Sie die Anonymisierungstabelle aus, mit der die Namen ersetzt werden sollen.")
    anon_path = filedialog.askopenfilename()
    
    anons=list(())
    if anon_path!='':    
        anon_enc=get_enc(anon_path)
        print(anon_enc)
        with io.open(anon_path,encoding=anon_enc) as fa:
            anon_lines=fa.readlines()
            for line in anon_lines:
                anon = line.split("%")
                if anon[1][-1:] =="\n":
                    anon[1] = anon[1][:-1]
                anons.insert(0,[anon[0],anon[1]])
    
    messagebox.showinfo("Sprechertabelle auswählen","Wählen Sie die Sprechertabelle aus, mit der die Sprechermarkierungen ersetzt werden sollen.")
    sp_path = filedialog.askopenfilename()
    
    sps=list(())
    if sp_path != "":
        sp_enc = get_enc(sp_path)    
        print(sp_enc)
        with io.open(sp_path,encoding=sp_enc) as fs:
            sp_lines=fs.readlines()
            for line in sp_lines:
                sp = line.split("%")
                if sp[1][-1:] =="\n":
                    sp[1] = sp[1][:-1]
                sps.insert(0,[sp[0],sp[1]])
    
    qu=list(())
    
    path=file_path[:file_path.rfind("/")]
    outfile=file_path[file_path.rfind("/")+1:-4]+".txt"
    outfile_path=path+"/"+outfile
    with io.open(file_path,encoding=file_enc) as f:
        lines=f.readlines()
        nlines=len(lines)
    print(nlines)
    timelen=len("{00:00:01}   ")
    if nlines<1000:    
        nlen=len("001   ")
    else:
        nlen=len("0001   ")
    splen=len("F(m):    ")
    prelen=timelen+nlen+splen
    print(prelen)
    linelen=66-prelen
    #messagebox.showinfo("",linelen)
    startn=1
    skipnext=0
    spmar=0
    with io.open(outfile_path,'w',encoding="utf-8") as fo:
        with io.open(file_path,encoding=file_enc) as f:
            lines=f.readlines()
            i=0
            opos=0
            while (i<len(lines) and i<20000) or len(qu)>0:
                if len(qu)==0:
                    qu.insert(0,dress_line(lines[i]))
                    i=i+1
                    #print(i)
                else:
                    if len(qu[0][3])<=linelen:
                        print(qu[0][0]+qu[0][1]+qu[0][2]+qu[0][3][:],file=fo)
                        qu.pop(0)
                    else:
                        spacepos=qu[0][3][:linelen+1].rfind(" ")+1
                        opos=qu[0][3][:].find("[")
                        cpos=qu[0][3][:].find("]")
                        if opos!=-1 and cpos!=-1 and (cpos-opos+1)>linelen:
                            print("ERROR: [] zu lang in Zeile "+str(i))
                            messagebox.showerror("Error", "Die Übersprechung [...] in Zeile "+str(i)+" ist zu lang für eine Zeile und muss daher aufgetrennt werden.")
                            i=9999
                            qu.pop(0)
                        else:
                            opos=qu[0][3][:spacepos].find("[")
                            cpos=qu[0][3][:spacepos].find("]")
                            if opos!= -1 and cpos == -1:
                                print("Übersprechung in neue Zeile verschoben in Segment "+str(i))
                                spacepos=opos
                            
                            print(qu[0][0]+qu[0][1]+qu[0][2]+qu[0][3][:spacepos], file=fo)
                            qu.insert(0,rest_line("%%%"+qu[0][3][spacepos:]))
                            qu.pop(1)
                            if 0 and opos!= -1 and cpos != -1:
                                qu.insert(0,dress_line(lines[i],opos=opos))
                                i=i+1
    if i!=9999:
        messagebox.showinfo("Ordner","Das Transkript wurde als Textdatei gespeichert in '"+path+"' unter dem Namen '"+outfile+"'.")                