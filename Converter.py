#!/bin/python3
#
# version:  v1.3
# date:     2019-01-20
# author:   MrJollyOlliMan

#import Tkinter
#from Tkinter import *

from tkinter import Button, Checkbutton, Frame, Label, LabelFrame, Tk, StringVar, LEFT, RIGHT, BOTTOM, TOP, NW, NE, W, E, CENTER, BOTH, X, messagebox, filedialog#, PhotoImage

from PIL import Image, ImageTk
import os
import platform

#-------------- global variables

IntGloVerticalSpace = 5
IntGloHorizontalSpace = 5
initial_album_dir = '\\192.168.2.11\audio_dsic\''
#initial_album_dir = 'F:\\aktuell\\Python\\Python Album-Cover-Converter'
#initial_album_dir = 'C:\\Benutzer\\oscheum\\Eigene Dokumente\\PureSync\\41_Elektronik\\05_python\\projects\\Album-Cover-Converter'
StrFileAbsPath = ""
StrFilePath = ""
StrFileName = ""

#-------------- global functions

def SelectOutFolderSame():
    CbuOutFolderSubCD1.deselect()
    CbuOutFolderSubCD2.deselect()
    CbuOutFolderSubCD3.deselect()
    CbuOutFolderSubCD4.deselect()
    CbuOutFolderSubCD5.deselect()
    CbuOutFolderSubCD6.deselect()

def SelectOutFolderSub():
    CbuOutFolderSame.deselect()

def MakePreviewImage(ThisFile, px=160):
    if ThisFile == None:
        ThisImg = Image.new('RGB', (px, px), (240, 240, 240))
    else:
        ThisImg = Image.open(ThisFile)
        global SquareBox
        SquareBox = fctBoxForSquareSize(ThisImg.size)
        ThisImg = ThisImg.resize((px, px), Image.ANTIALIAS, SquareBox)
    ThisImg = ImageTk.PhotoImage(ThisImg)
    return ThisImg

#    function check is size tuple is wider than 110% height -> make cropBox  
def fctBoxForSquareSize(thisSize):          # as Tuple (width, height)
    if thisSize[0] > thisSize[1]*1.1:
        newX = thisSize[0]-thisSize[1]
        thisBox = (newX, 0, thisSize[0], thisSize[1])
    else:
        thisBox = None
    print('set crop box to',thisBox)
    return thisBox      # as Tuple (left, lower, right, upper) or None

def OpenFile():
    this_file = filedialog.askopenfile(filetypes=[('JPEG (File Interchange Format)','.jpg')], initialdir = initial_album_dir)
    abs_path = os.path.abspath(this_file.name)
    #print(abs_path)
    global StrFileAbsPath
    StrFileAbsPath = abs_path
    #print(StrSubDirectory.get())
    path_parts = abs_path.split( StrSubDirectory.get() )
    global StrFileName
    StrFileName = path_parts[len(path_parts) - 1]
    print('file: '+StrFileName)
    StrSelectedFile.set(StrFileName)
    IntNoOfLeftLetters = len(path_parts[len(path_parts) - 1])
    global StrFilePath
    StrFilePath = abs_path[:-IntNoOfLeftLetters]
    print('path: '+StrFilePath)
    
    global imgPreview
    imgPreview = MakePreviewImage(abs_path)           # update the selected image in LblPreviewImage
    LblPreviewImage.configure(image=imgPreview)
    LblPreviewImage.image = imgPreview

def Converting():
    global StrFilePath
    global StrFileName
    if StrFilePath == "":
        messagebox.showinfo("No file selected!", "You must select a jpg file, before converting this!")
        #OpenFile()
    else:
        if StrOutFolderSame.get() == "":
            ConvertImage(StrFilePath, StrFileName)
        if StrOutFolderSubCD1.get() == "CD 1":
            #print(StrFilePath + StrOutFolderSubCD1.get() + StrSubDirectory.get())
            ConvertImage(StrFilePath, StrFileName, StrOutFolderSubCD1.get() + StrSubDirectory.get())
        if StrOutFolderSubCD2.get() == "CD 2":
            ConvertImage(StrFilePath, StrFileName, StrOutFolderSubCD2.get() + StrSubDirectory.get())
        if StrOutFolderSubCD3.get() == "CD 3":
           ConvertImage(StrFilePath, StrFileName, StrOutFolderSubCD3.get() + StrSubDirectory.get())
        if StrOutFolderSubCD4.get() == "CD 4":
           ConvertImage(StrFilePath, StrFileName, StrOutFolderSubCD4.get() + StrSubDirectory.get())
        if StrOutFolderSubCD5.get() == "CD 5":
           ConvertImage(StrFilePath, StrFileName, StrOutFolderSubCD5.get() + StrSubDirectory.get())
        if StrOutFolderSubCD6.get() == "CD 6":
           ConvertImage(StrFilePath, StrFileName, StrOutFolderSubCD6.get() + StrSubDirectory.get())

def checkDirectory(ThisDirectory):
    if os.path.isdir(ThisDirectory):
        return True
    else:
        messagebox.showwarning("Directory doesn't exist!", "The selected directory: \n\n"+ThisDirectory+"\n\ndoesn't exist.")
        return False
    
def checkOutputFile(ThisFile):
    if os.path.isfile(ThisFile):
        if messagebox.askyesno("File already exist!", "There exists already a file: \n\n"+ThisFile+"\n\nin the output directory. Do you want to replace this file?"):
            return False
        else:
            return True
    else:
        return False

def ConvertImage(ThisFilePath, ThisFileName, ThisOutputExtention = ""):
    img = Image.open(ThisFilePath + ThisFileName)
    #print(ThisFilePath)
    #print(ThisFileName)
    if checkDirectory(ThisFilePath + ThisOutputExtention):
        print('creating the thumbnails:')
        if not (StrOutFileName1.get() == ""):
            outputFile = ThisFilePath + ThisOutputExtention + StrOutFileName1.get()
            if not checkOutputFile(outputFile):
                print(outputFile)
                out1 = img.resize((200, 200), Image.ANTIALIAS, SquareBox)
                out1.save(outputFile, "JPEG", quality = 90)
        if not (StrOutFileName2.get() == ""):
            outputFile = ThisFilePath + ThisOutputExtention + StrOutFileName2.get()
            if not checkOutputFile(outputFile):
                print(outputFile)
                out2 = img.resize((75, 75), Image.ANTIALIAS, SquareBox)
                out2.save(outputFile, "JPEG", quality = 85)
    print('done!')
    print('')


#-------------- def. main window
main = Tk(className = "album cover converter")

#-------------- def. widgets
FrameCheckbuttons = Frame ( main )
FrameRightColumn = Frame( FrameCheckbuttons )
FrameLeftColumn = Frame( FrameCheckbuttons )
FrameCheckbuttonsSubDirectory = LabelFrame (FrameLeftColumn, text = "operating OS" )
FrameCheckbuttons1 = LabelFrame ( FrameRightColumn, text = "output files" )
FrameCheckbuttons2 = LabelFrame ( FrameLeftColumn, text = "output directory", pady = IntGloHorizontalSpace )
FrameMiddleColumn = Frame ( FrameCheckbuttons, width = 2*IntGloHorizontalSpace )

LblTitle = Label(FrameLeftColumn, text = "album cover\nconverter", height=3, fg="dark blue", font="Verdana 12 bold italic")

StrSubDirectory = StringVar()
CbuSubDirectory = Checkbutton ( FrameCheckbuttonsSubDirectory, text = "Windows", variable = StrSubDirectory, onvalue = "\\", offvalue = "/", padx = IntGloHorizontalSpace )
CbuSubDirectory2 = Checkbutton ( FrameCheckbuttonsSubDirectory, text = "Linux", variable = StrSubDirectory, onvalue = "/", offvalue = "\\", padx = IntGloHorizontalSpace )

StrOutFileName1 = StringVar()
StrOutFileName2 = StringVar()
CbuFolder = Checkbutton ( FrameCheckbuttons1, text = "Folder.jpg [200x200 px]", variable = StrOutFileName1, onvalue = "Folder.jpg", offvalue = "", padx = IntGloHorizontalSpace)
CbuAlbumArtSmall = Checkbutton ( FrameCheckbuttons1, text = "AlbumArtSmall.jpg [75x75 px]", variable = StrOutFileName2, onvalue = "AlbumArtSmall.jpg", offvalue = "", padx = IntGloHorizontalSpace)

StrOutFolderSame = StringVar()
StrOutFolderSubCD1 = StringVar()
StrOutFolderSubCD2 = StringVar()
StrOutFolderSubCD3 = StringVar()
StrOutFolderSubCD4 = StringVar()
StrOutFolderSubCD5 = StringVar()
StrOutFolderSubCD6 = StringVar()
CbuOutFolderSame = Checkbutton ( FrameCheckbuttons2, text = "same folder", variable = StrOutFolderSame, onvalue = "", offvalue = " ", command = SelectOutFolderSame, padx = IntGloHorizontalSpace)
CbuOutFolderSubCD1 =  Checkbutton ( FrameCheckbuttons2, text = "sub folder 'CD 1'", variable = StrOutFolderSubCD1, onvalue = "CD 1", offvalue = "", command = SelectOutFolderSub, padx = IntGloHorizontalSpace)
CbuOutFolderSubCD2 =  Checkbutton ( FrameCheckbuttons2, text = "sub folder 'CD 2'", variable = StrOutFolderSubCD2, onvalue = "CD 2", offvalue = "", command = SelectOutFolderSub, padx = IntGloHorizontalSpace)
CbuOutFolderSubCD3 =  Checkbutton ( FrameCheckbuttons2, text = "sub folder 'CD 3'", variable = StrOutFolderSubCD3, onvalue = "CD 3", offvalue = "", command = SelectOutFolderSub, padx = IntGloHorizontalSpace)
CbuOutFolderSubCD4 =  Checkbutton ( FrameCheckbuttons2, text = "sub folder 'CD 4'", variable = StrOutFolderSubCD4, onvalue = "CD 4", offvalue = "", command = SelectOutFolderSub, padx = IntGloHorizontalSpace)
CbuOutFolderSubCD5 =  Checkbutton ( FrameCheckbuttons2, text = "sub folder 'CD 5'", variable = StrOutFolderSubCD5, onvalue = "CD 5", offvalue = "", command = SelectOutFolderSub, padx = IntGloHorizontalSpace)
CbuOutFolderSubCD6 =  Checkbutton ( FrameCheckbuttons2, text = "sub folder 'CD 6'", variable = StrOutFolderSubCD6, onvalue = "CD 6", offvalue = "", command = SelectOutFolderSub, padx = IntGloHorizontalSpace)


FrameButtons1 = Frame( FrameRightColumn )
FrameButtonsVerticalSpace1 = Frame ( FrameButtons1, height = IntGloVerticalSpace)
FrameButtonsVerticalSpace2 = Frame ( FrameButtons1, height = IntGloVerticalSpace)
FrameFilePreview = LabelFrame ( FrameButtons1, text = "selected file" )
FrameButtonsVerticalSpace3 = Frame ( FrameFilePreview, height = 2*IntGloVerticalSpace)
StrSelectedFile = StringVar()
LblSelectedFile = Label ( FrameFilePreview, textvariable = StrSelectedFile, height=2, wraplength = 180 )
StrSelectedFile.set("- no file -")
imgPreview = MakePreviewImage(None,160)
#imgPreview = MakePreviewImage("C:\\users\\oscheum\\documents\\PureSync\\41_Elektronik\\05_python\\projects\\Album-Cover-Thumbnail-Converter\\Inv\\Paul.jpg")
LblPreviewImage = Label ( FrameFilePreview, height=160, width=160, image=imgPreview )
ButSelectFile = Button ( FrameButtons1, text = "open file", command = OpenFile, width = "12")
ButConvertFiles = Button ( FrameButtons1, text = "convert", command = Converting, width = "12")


#-------------- set default values
if platform.platform()[:7] == "Windows":
    CbuSubDirectory.select()
    CbuSubDirectory2.deselect()
else:
    CbuSubDirectory.deselect()
    CbuSubDirectory2.select()

CbuFolder.select()
CbuAlbumArtSmall.select()
CbuOutFolderSame.select()
CbuOutFolderSubCD1.deselect()
CbuOutFolderSubCD2.deselect()
CbuOutFolderSubCD3.deselect()
CbuOutFolderSubCD4.deselect()
CbuOutFolderSubCD5.deselect()
CbuOutFolderSubCD6.deselect()

#-------------- set widgets
FrameCheckbuttons.pack( expand="yes" )
FrameLeftColumn.pack( side = LEFT )
LblTitle.pack()
FrameCheckbuttonsSubDirectory.pack ( side = TOP, fill = X )
FrameCheckbuttons2.pack(side = TOP )
FrameMiddleColumn.pack( side = LEFT )
FrameRightColumn.pack( side = RIGHT )
FrameCheckbuttons1.pack()
FrameButtons1.pack( fill = X )

CbuSubDirectory.pack(anchor = W)
CbuSubDirectory2.pack(anchor = W)   

CbuFolder.pack(anchor = W)
CbuAlbumArtSmall.pack(anchor = W)

CbuOutFolderSame.pack(anchor = W)
CbuOutFolderSubCD1.pack(anchor = W)
CbuOutFolderSubCD2.pack(anchor = W)
CbuOutFolderSubCD3.pack(anchor = W)
CbuOutFolderSubCD4.pack(anchor = W)
CbuOutFolderSubCD5.pack(anchor = W)
CbuOutFolderSubCD6.pack(anchor = W)

FrameButtonsVerticalSpace1.pack()
FrameFilePreview.pack( fill = X )
LblSelectedFile.pack()
LblPreviewImage.pack()
FrameButtonsVerticalSpace3.pack()
FrameButtonsVerticalSpace2.pack()
ButSelectFile.pack(side = LEFT)
ButConvertFiles.pack(side = RIGHT)

#-------------- def & set main window
#            widthxheight
main.geometry("370x350")
main.mainloop()
