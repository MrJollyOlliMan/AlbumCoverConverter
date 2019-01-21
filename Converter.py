#!/bin/python3
#
##########################################
#
# version:  v1.4
# date:     2019-01-21
# author:   MrJollyOlliMan
#
##########################################

from tkinter import Button, Checkbutton, Frame, IntVar, Label, LabelFrame, Radiobutton, StringVar, Tk, LEFT, RIGHT, TOP, W, X, messagebox, filedialog
from PIL import Image, ImageTk
import os

from fctModul import fctCheckDirectory, fctCheckOutputFile


#---    global variables

DEBUG = True
intX, intY = 5, 5
strFileAbsPath, strFileName, strFilePath = "", "", ""

initial_album_dir = '\\192.168.2.11\audio_dsic\''
#initial_album_dir = 'F:\\aktuell\\Python\\Python Album-Cover-Converter'
#initial_album_dir = 'C:\\Benutzer\\oscheum\\Eigene Dokumente\\PureSync\\41_Elektronik\\05_python\\projects\\Album-Cover-Converter'

SquareBox = None
imgPreview = None


#---    global functions

def fctBoxForSquareSize(thisSize):          # thisSize as Tuple (width, height)
    if intRBtnCropBoxButtons.get() == 1:
        newX = thisSize[0]-thisSize[1]
        thisBox = (newX, 0, thisSize[0], thisSize[1])
    else:
        thisBox = None
    if DEBUG:
        print('set crop box to',thisBox)
    return thisBox      # as Tuple (left, lower, right, upper) or None

def fctConvertImage(ThisFilePath, ThisFileName, ThisOutputExtention = ""):
    img = Image.open(ThisFilePath + ThisFileName)
    #print(ThisFilePath)
    #print(ThisFileName)
    if fctCheckDirectory(ThisFilePath + ThisOutputExtention):
        print('creating the thumbnails:')
        if not (CBtnOutputFileVal[0][2].get() == ""):
            outputFile = ThisFilePath + ThisOutputExtention + CBtnOutputFileVal[0][2].get()
            if not fctCheckOutputFile(outputFile):
                print(outputFile)
                out1 = img.resize((200, 200), Image.ANTIALIAS, SquareBox)
                out1.save(outputFile, "JPEG", quality = 90)
        if not (CBtnOutputFileVal[1][2].get() == ""):
            outputFile = ThisFilePath + ThisOutputExtention + CBtnOutputFileVal[1][2].get()
            if not fctCheckOutputFile(outputFile):
                print(outputFile)
                out2 = img.resize((75, 75), Image.ANTIALIAS, SquareBox)
                out2.save(outputFile, "JPEG", quality = 85)
    print('done!\n')

def fctMakePreviewImage(ThisFile, px=180):
    if ThisFile == None:
        ThisImg = Image.new('RGB', (px, px), (240, 240, 240))
    else:
        ThisImg = Image.open(ThisFile)
        SquareBox = fctBoxForSquareSize(ThisImg.size)
        ThisImg = ThisImg.resize((px, px), Image.ANTIALIAS, SquareBox)
    ThisImg = ImageTk.PhotoImage(ThisImg)
    return ThisImg

def fctUpdatePreviewImage():
    global imgPreview
    if strFileAbsPath == "":
        imgPreview = fctMakePreviewImage(None)
    else:
        imgPreview = fctMakePreviewImage(strFileAbsPath)
    lblPreviewImage.configure(image=imgPreview)
    lblPreviewImage.image = imgPreview
    return 0


#---    callbacks
    
def callConverting():
    global strFileName, strFilePath
    
    if strFilePath == "":
        messagebox.showinfo("No file selected!", "You must select a jpg file, before converting this!")
    else:
        for i in range(0, 7):
            if CBtnOutputDirectoryVal[i][2].get() == CBtnOutputDirectoryVal[i][1]:
                if i != 0:
                    fctConvertImage(strFilePath, strFileName, CBtnOutputDirectoryVal[i][2].get() + strDirectorySeparator.get() )
                else:
                    fctConvertImage(strFilePath, strFileName)

def callOpenFileDialog():
    global strFileAbsPath, strFileName, strFilePath
    
    this_file = filedialog.askopenfile(filetypes=[('JPEG (File Interchange Format)','.jpg')], initialdir = initial_album_dir)
    strFileAbsPath = os.path.abspath(this_file.name)
    
    path_parts = strFileAbsPath.split( strDirectorySeparator.get() ) 
    strFileName = path_parts[len(path_parts) - 1]
    strSelectedFile.set(strFileName)
    
    IntNoOfLeftLetters = len(path_parts[len(path_parts) - 1])
    strFilePath = strFileAbsPath[:-IntNoOfLeftLetters]
    if DEBUG:
#        print('strFileAbsPath:', strFileAbsPath)
        print(strDirectorySeparator.get())
        print('strFileName:', strFileName)
        print('strFilePath:', strFilePath)
    
    fctUpdatePreviewImage()

def callSelectOutFolderSame():
    for i in range(1, 7):
        CBtnOutputDirectory[i].deselect()

def callSelectOutFolderSub():
    CBtnOutputDirectory[0].deselect()


#---    def. main window + frames

main = Tk(className = "album cover converter")

frmMain = Frame ( main )
frmLeftColumn = Frame( frmMain, padx = intX, pady = intY/2 )
frmRightColumn = Frame( frmMain, padx = intX, pady = intY/2 )

lblTitle = Label(frmLeftColumn, text = "album cover\nconverter", fg="dark blue", font="Verdana 12 bold italic")


#---    OS widgets; directory separator

frmRBtnOS = LabelFrame (frmLeftColumn, text = "operating OS", padx = intX, pady = intY/2 )

strDirectorySeparator = StringVar()
strDirectorySeparator.set("\\")
OSButtons = [  ("Windows", "\\"),
               ("Linux", "/") ]
for Text, Val in OSButtons:
    RBtnOSButtons = Radiobutton(frmRBtnOS, text = Text, variable = strDirectorySeparator, value = Val, indicatoron = 0)
    RBtnOSButtons.pack( fill = X, pady = intY/2 )


#---    output directory

FrameCheckbuttons2 = LabelFrame ( frmLeftColumn, text = "output directory", pady = intY)

CBtnOutputDirectoryVal = [ ("same folder", "", StringVar() ),
                           ("sub folder 'CD 1'", "CD 1", StringVar() ),
                           ("sub folder 'CD 2'", "CD 2", StringVar() ),
                           ("sub folder 'CD 3'", "CD 3", StringVar() ),
                           ("sub folder 'CD 4'", "CD 4", StringVar() ),
                           ("sub folder 'CD 5'", "CD 5", StringVar() ), 
                           ("sub folder 'CD 6'", "CD 6", StringVar() ) ]
i = 0
CBtnOutputDirectory = {}
for Text, OnV, Var in CBtnOutputDirectoryVal:
    if i == 0:
        CBtnOutputDirectory[i] = Checkbutton ( FrameCheckbuttons2, text = Text, variable = Var, onvalue = OnV, offvalue = " ", command = callSelectOutFolderSame, padx = intX )
    else:
        CBtnOutputDirectory[i] = Checkbutton ( FrameCheckbuttons2, text = Text, variable = Var, onvalue = OnV, offvalue = "", command = callSelectOutFolderSub, padx = intX )
    CBtnOutputDirectory[i].pack( anchor = W )
    CBtnOutputDirectory[i].select()
    i = i + 1

CBtnOutputDirectory[0].select()
callSelectOutFolderSame()


#---    BTNs 'open file' & 'convert

frmButtons = Frame( frmLeftColumn, pady = intY/2 )

btnSelectFile = Button ( frmButtons, text = "open file", command = callOpenFileDialog, width = "12", pady = intY/2 )
btnConvertFiles = Button ( frmButtons, text = "convert", command = callConverting, width = "12", pady = intY/2 )
btnSelectFile.pack( fill = X, padx = intX, pady = intY/2 )
btnConvertFiles.pack( fill = X, padx = intX, pady = intY/2 )


#---    output file widgets

frmCBtnOutputFiles = LabelFrame ( frmRightColumn, text = "output files", padx = intX)

CBtnOutputFileVal = [ ("Folder.jpg [200x200 px]", "Folder.jpg", StringVar()),
                    ("AlbumArtSmall.jpg [75x75 px]", "AlbumArtSmall.jpg", StringVar()) ]
for Text, OnV, Var in CBtnOutputFileVal:
    CBtnOutputFile = Checkbutton ( frmCBtnOutputFiles, text = Text, variable = Var, onvalue = OnV, offvalue = "")
    CBtnOutputFile.pack( anchor = W )
    CBtnOutputFile.select()


#---    crop box widgets

frmCropBox = LabelFrame ( frmRightColumn, text = "crop the image?", padx = intX, pady = intY/2 )

intRBtnCropBoxButtons = IntVar()
intRBtnCropBoxButtons.set(0)
RBtnCropBoxButtonsVal = [  ("no", 0),
                           ("flushed right squared crop box", 1) ]
for Text, Val in RBtnCropBoxButtonsVal:
    RBtnCropBoxButtons = Radiobutton(frmCropBox, text = Text, variable = intRBtnCropBoxButtons, value = Val, command = fctUpdatePreviewImage, indicatoron = 0)
    RBtnCropBoxButtons.pack( fill = X, pady = intY/2 )


#---    preview widgets

frmFilePreview = LabelFrame ( frmRightColumn, text = "selected file")
strSelectedFile = StringVar()
strSelectedFile.set("- no file -")
lblSelectedFile = Label ( frmFilePreview, textvariable = strSelectedFile, wraplength = 180)
lblSelectedFile.pack()
lblPreviewImage = Label ( frmFilePreview, height=180, width=180, image=imgPreview)
lblPreviewImage.pack( ipady = intY )
fctUpdatePreviewImage()


#---    set widgets left side

frmMain.pack( expand="yes" )
frmLeftColumn.pack( side = LEFT )
lblTitle.pack()
frmRBtnOS.pack ( side = TOP, fill = X, pady = intY/2 )
FrameCheckbuttons2.pack( side = TOP, pady = intY/2 )
frmButtons.pack( fill = X, pady = intY/2 )


#---    set widgets right side

frmRightColumn.pack( side = RIGHT )
frmCBtnOutputFiles.pack( pady = intY/2 )
frmCropBox.pack( fill = X, pady = intY/2 )
frmFilePreview.pack( fill = X, pady = intY/2 )


#---    def & set main window

main.geometry("370x440")    # width x height
main.mainloop()