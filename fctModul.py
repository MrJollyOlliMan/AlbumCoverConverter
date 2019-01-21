#!/bin/python3
#
##########################################
#
# version:  v1.4
# date:     2019-01-21
# author:   MrJollyOlliMan
#
##########################################

import os

from tkinter import messagebox

#---    functions file & directory

def fctCheckDirectory(ThisDirectory):
    if os.path.isdir(ThisDirectory):
        return True
    else:
        messagebox.showwarning("Directory doesn't exist!", "The selected directory: \n\n"+ThisDirectory+"\n\ndoesn't exist!")
        return False
    
def fctCheckOutputFile(ThisFile):
    if os.path.isfile(ThisFile):
        if messagebox.askyesno("File already exist!", "There exists already a file: \n\n"+ThisFile+"\n\nin the output directory. Do you want to replace this file?"):
            return False
        else:
            return True
    else:
        return False