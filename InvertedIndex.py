from sys import version_info
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import os


FolderPath = ''
InWord = ''



def BuSaveData():
    global FolderPath
    global InWord
    InWord = EntryWord.get()
    FolderPath = main_win.path
    main_win.destroy()

def chooseDir():
    main_win.path = filedialog.askdirectory(parent=main_win, initialdir= "/", title='Please select a directory')


class TreeNode:
    def __init__(self,v):
        self.val=v
        self.children={}
        self.endhere=False


class Trie:
    def __init__(self):
        self.root=TreeNode(None)
    def insert(self,word):
        s = ['.', ',', ':', '?', '/', '"', '<', '>', ';', '(', ')']
        parent=self.root
        for i , char in enumerate(word):
            if i in s :
                continue
            else:

                if char not in parent.children:
                    parent.children[char]=TreeNode(char)
                parent=parent.children[char]
                if i ==len(word)-1:
                    parent.endhere=True

    def search(self, word):
        parent = self.root
        for char in word:
            if char not in parent.children:
                return False
            parent = parent.children[char]
        return True


main_win = tkinter.Tk()
main_win.title("")
main_win.geometry("300x300")
main_win.path = ''
EntryWord = tkinter.Entry(main_win, width=15, font=('Arial', 16))
EntryWord.pack()
tkinter.Label(main_win, text="Enter Word to search").pack()
b_chooseDir = tkinter.Button(main_win, text="Chose Folder", command=chooseDir).pack()
buSubmit = tkinter.Button(main_win, text="Submit")
buSubmit.pack()
buSubmit.config(command=BuSaveData)

main_win.mainloop()


os.chdir(FolderPath)
ListOfFilePaths=[]
ListOfFileNames=[]
with os.scandir(FolderPath) as it:
    for entry in it:
         if entry.name.endswith(".txt") and entry.is_file():
             with open(entry.name, encoding='utf8')as fp:
                 Line = fp.read()
                 # Line=clean(Line)
                 l = Line.split()
                 Tree = Trie()
                 for word in l:
                     word = word.lower()
                     Tree.insert(word)
                 if Tree.search(InWord) == True:
                    ListOfFilePaths.append(FolderPath+"/"+entry.name)
                    ListOfFileNames.append(entry.name)
                    #print(ListOfFileNames)
                    #print(ListOfFilePaths)
             continue
         else:
             continue


root = Tk()
root.title(str(len(ListOfFilePaths))+" Files Containing " + InWord)
root.geometry("300x300")


def read(file):
    import webbrowser
    webbrowser.open(file)

class Example(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        text = tkinter.Text(self, wrap="none")
        vsb = tkinter.Scrollbar(orient="vertical", command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        text.pack(fill="both", expand=True)

        for i in range(len(ListOfFilePaths)):
            b = tkinter.Button(self, text=ListOfFileNames[i],  command = partial(read, ListOfFilePaths[i]))
            text.window_create("end", window=b)
            text.insert("end", "\n")

        text.configure(state="disabled")

Example(root).pack(fill = 'both', expand=True)




#for i in range(len(ListOfFilePaths)) :
 #   tkinter.Button(root, text=ListOfFileNames[i],  command = partial(read, ListOfFilePaths[i])).pack()



root.mainloop()






