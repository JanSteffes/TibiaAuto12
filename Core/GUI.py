import pyautogui
import tkinter as tk
from tkinter import SUNKEN, RAISED, Label, Grid
from PIL import Image, ImageTk
from Core.Defaults import rgb

class GUI:
    def __init__(self, windowID, name):
        self.windowID = windowID
        self.name = name

    def enableResize(self, windowToAutoResize):
        maxRow = 0
        maxColumn = 0
        for child in windowToAutoResize.winfo_children():
            childInfo = child.grid_info()
            childRow = childInfo["row"]
            maxRow = max(maxRow, childRow)
            childColumn = childInfo["column"]
            maxColumn = max(maxColumn, childColumn)
        for rowIndex in range(maxRow+1):
            Grid.rowconfigure(windowToAutoResize, rowIndex, weight = 1)
        for columnIndex in range(maxColumn+1):
            Grid.columnconfigure(windowToAutoResize, columnIndex, weight = 1)

    
    def EnableStageRecursive(self, Stage, enable = True):
        if enable:
            stateToSet = 'enable'
        else:
            stateToSet = 'disable'
        for child in Stage.winfo_children():    
            childChildren = child.winfo_children()
            if childChildren and len(childChildren) > 0:
                self.EnableStageRecursive(child)
            else:
                try:
                    child.configure(state=stateToSet)
                except Exception:
                    return


    def MainWindow(self: (object, 'self'), 
        BackgroundImage: (str, 'path to image to use, can be left empty'), 
        #sizes: (object, 'size of window, simple array ont 2 int (more won\'t be used), [0] is width and [1] is height'), 
        positions: (object, 'idk, some positions for who knows what')):
        """Open the main window using given sizes and positions
        """
        self.windowID = tk.Tk()
        # w = sizes[0]
        # h = sizes[1]
        # sw = self.windowID.winfo_screenwidth()
        # sh = self.windowID.winfo_screenheight()
        # x = (sw - w) / positions[0]
        # y = (sh - h) / positions[1]
        # self.windowID.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.windowID.title(self.name)
        self.windowID.resizable(width=True, height=True)
        self.windowID.configure(background='#000', takefocus=True)
        self.windowID.iconbitmap('images/icone2.ico')
        if BackgroundImage:      
            image = Image.open('images/Modules/' + BackgroundImage + '.png')
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(self.windowID, image=photo, bg='#000')
            label.image = photo
            label.place(x=0, y=0, relwidth=1, relheight=1)        

    def DefaultWindow(self, BackgroundImage, sizes, positions):
        self.windowID = tk.Toplevel()
        self.windowID.focus_force()
        #self.windowID.grab_set()
        # w = sizes[0]
        # h = sizes[1]
        # sw = self.windowID.winfo_screenwidth()
        # sh = self.windowID.winfo_screenheight()
        # x = (sw - w) / positions[0]
        # y = (sh - h) / positions[1]
        # self.windowID.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.windowID.title(self.name)
        self.windowID.resizable(width=True, height=True)
        self.windowID.configure(background='#000', takefocus=True)
        self.windowID.iconbitmap('images/icone2.ico')
        # image = Image.open('images/Modules/' + BackgroundImage + '.png')
        # photo = ImageTk.PhotoImage(image)
        # label = tk.Label(self.windowID, image=photo, bg='#000')
        # label.image = photo
        # label.pack()

    def InvisibleWindow(self, BackgroundImage):
        self.windowID = tk.Toplevel()
        self.windowID.focus_force()
        self.windowID.grab_set()
        self.windowID.resizable(width=False, height=False)
        self.windowID.geometry('130x130')
        self.windowID.image = tk.PhotoImage(file='images/BackgroundImages/' + BackgroundImage + '.png')
        label = tk.Label(self.windowID, image=self.windowID.image, bg='black')
        label.place(x=0, y=0)
        self.windowID.overrideredirect(True)
        self.windowID.wm_attributes("-topmost", True)
        self.windowID.attributes("-transparentcolor", "black")

    def loop(self):
        self.windowID.mainloop()

    def Protocol(self, Function):
        return self.windowID.protocol("WM_DELETE_WINDOW", Function)

    def UpdateWindow(self, X, Y):
        self.windowID.geometry('130x130+%d+%d' % (X - 65, Y - 65))
        self.windowID.update()

    def destroyWindow(self):
        self.windowID.destroy()

    def PositionOfWindow(self, value):
        if value == 'X':
            return self.windowID.winfo_x()
        elif value == 'Y':
            return self.windowID.winfo_y()

    def createFrame(self, masterToAssignTo = None, background = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        frameID = tk.Frame(masterToAssignTo, background = background)
        return frameID

    def addFrameGrid(self, rowIndex, columnIndex, masterToAssignTo = None, background = None):
        print('created frame at ' + str(rowIndex) + '|' + str(columnIndex) + ' to master ' + str(masterToAssignTo))        
        frameID = self.createFrame(masterToAssignTo, background = background)  
        frameID.grid(row = rowIndex, column = columnIndex, sticky = 'nsew')
        return frameID

    def addButton(self, textOfButton, command, sizes, positions):
        buttonID = self.createButton(textOfButton, command)
        buttonID.place(w=sizes[0], h=sizes[1], x=positions[0], y=positions[1])
        return buttonID

    def addButtonGrid(self, textOfButton, command, rowIndex, columnIndex, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        buttonID = self.createButton(textOfButton, command, masterToAssignTo)
        buttonID.grid(row= rowIndex, column = columnIndex, sticky = 'nsew')
        return buttonID

    def createButton(self, textOfButton, command, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        buttonID = tk.Button(masterToAssignTo,
                             text=textOfButton,
                             font=('Microsoft Sans Serif', 10),
                             bg=rgb((114, 0, 0)),
                             fg='white',
                             command=command,
                             cursor="hand2",
                             activebackground=rgb((103, 13, 5)))
        return buttonID



    def addCheck(self, variable, position, selected, textOfButton="", image=None):        
        buttonID = self.createCheck(variable, selected, textOfButton, image)
        buttonID.place(x=position[0], y=position[1])
        return buttonID

    def addCheckGrid(self, variable, rowIndex, columnIndex, selected, textOfButton="", image=None, masterToAssignTo = None):
        buttonID = self.createCheck(variable, selected, textOfButton, image, masterToAssignTo)
        buttonID.grid(row = rowIndex, column = columnIndex, sticky = 'nsew')
        return buttonID

    def createCheck(self, variable, selected, textOfButton, image = None, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID        
        buttonID = tk.Checkbutton(masterToAssignTo,
                                  bg=rgb((114, 0, 3)),
                                  activebackground=rgb((114, 0, 3)),
                                  activeforeground='white',
                                  text=textOfButton,
                                  variable=variable,
                                  fg='white',
                                  selectcolor=rgb((114, 0, 3)),
                                  cursor="hand2",
                                  onvalue=True,
                                  offvalue=False,
                                  image=image)
        if selected:
            buttonID.select()
        else:
            buttonID.deselect()
        return buttonID



    def addLabel(self, textOfLabel, position):
        labelID = self.createLabel(textOfLabel)
        labelID.place(x=position[0], y=position[1])
        return labelID

    def addLabelGrid(self, textOfLabel, rowIndex, columnIndex, masterToAssignTo = None):
        labelID = self.createLabel(textOfLabel, masterToAssignTo)
        labelID.grid(row=rowIndex, column = columnIndex, sticky = 'nsew')
        return labelID

    def createLabel(self, textOfLabel, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        labelID = Label(master = masterToAssignTo,
                           text=textOfLabel,
                           bg=rgb((114, 0, 0)),
                           fg='white')
        return labelID

    def addMinimalLabel(self, textOfLabel, position, h=16):     
        labelID = self.createMinimalLabel(textOfLabel)
        labelID.place(x=position[0], y=position[1], h=h)
        return labelID

    def addMinimalLabelGrid(self, textOfLabel, rowIndex, columnIndex, masterToAssignTo = None):
        return self.addLabelGrid(textOfLabel, rowIndex, columnIndex, masterToAssignTo)
    

    def createMinimalLabel(self, textOfLabel, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        labelID = tk.Label(masterToAssignTo,
                           text=textOfLabel,
                           bg=rgb((114, 0, 0)),
                           fg='white')
        return labelID

    def addImage(self, image, position):
        imageID = self.createImage(image)
        imageID.place(x=position[0], y=position[1])
        return imageID

    def addImageGrid(self, image, rowIndex, columnIndex, masterToAssignTo = None):
        imageID = self.createImage(image)
        imageID.grid(row= rowIndex, column = columnIndex, sticky = 'nsew')
        return imageID

    def createImage(self, image, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        imageID = tk.Label(masterToAssignTo,
                           image=image,
                           bg=rgb((114, 0, 0)),
                           fg='white')
        return imageID

    def addEntry(self, position, var, width=12):        
        entryID = self.createEntry(var, width)     
        entryID.place(x=position[0], y=position[1])
        return entryID

    def addEntryGrid(self, rowIndex, columnIndex, var, width=12, masterToAssignTo = None):  
        entryID = self.createEntry(var, width, masterToAssignTo)     
        entryID.grid(row = rowIndex, column = columnIndex, sticky = 'nsew')
        return entryID

    def createEntry(self, var, width = 12, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        entryID = tk.Entry(masterToAssignTo,
                           width=width,
                           textvariable=var,
                           bg=rgb((114, 0, 0)),
                           borderwidth=2,
                           foreground=rgb((81, 216, 0))
                           )
        return entryID

    def addOption(self, variable, options, position, width=4):
        optionID = self.createOption(variable, options, width)
        optionID.place(x=position[0], y=position[1])
        return optionID
    
    def addOptionGrid(self, variable, options, rowIndex, columnIndex, width = 4, masterToAssignTo = None):
        optionID = self.createOption(variable, options, width, masterToAssignTo)
        optionID.grid(row = rowIndex, column = columnIndex, sticky = 'nsew')
        return optionID

    def createOption(self, variable, options, width = 4, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        optionID = tk.OptionMenu(masterToAssignTo, variable, *options)
        optionID['bg'] = rgb((114, 0, 0))
        optionID['fg'] = 'white'
        optionID['activebackground'] = rgb((103, 13, 5))
        optionID["highlightthickness"] = 0
        optionID['width'] = width
        optionID['cursor'] = "hand2"
        return optionID

    def addRadio(self, text, variable, value, position, command=None):
        RadioID = self.createRadio(text, variable, value, command)
        RadioID.place(x=position[0], y=position[1])
        return RadioID

    def addRadioGrid(self, text, variable, value, rowIndex, columnIndex, command = None, masterToAssignTo = None):
        RadioID = self.createRadio(text, variable, value, command, masterToAssignTo)
        RadioID.grid(row = rowIndex, column = columnIndex, sticky = 'nsew')
        return RadioID
    

    def createRadio(self, text, variable, value, command = None, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        RadioID = tk.Radiobutton(masterToAssignTo,
                                 text=text,
                                 variable=variable,
                                 value=value,
                                 fg='white',
                                 selectcolor=rgb((114, 0, 3)),
                                 cursor="hand2",
                                 bg=rgb((114, 0, 3)),
                                 command=command)
        RadioID['activebackground'] = rgb((114, 0, 3)),
        RadioID['activeforeground'] = 'white',
        return RadioID

    def addRadioImage(self, text, variable, value, position, command=None, image=None):
        RadioID = self.createRadioImage(text, variable, value, command, image)
        RadioID.place(x=position[0], y=position[1])
        return RadioID

    def addRadioImageGrid(self, text, variable, value, rowIndex, columnIndex, command = None, image = None, masterToAssignTo = None):
        RadioID = self.createRadioImage(text, variable, value, command, image, masterToAssignTo)
        RadioID.grid(row = rowIndex, column = columnIndex, sticky = 'nsew')
        return RadioID

    def createRadioImage(self, text, variable, value, position, command = None, image = None, masterToAssignTo = None):
        if not masterToAssignTo:
            masterToAssignTo = self.windowID
        RadioID = tk.Radiobutton(masterToAssignTo,
                                 text=text,
                                 variable=variable,
                                 value=value,
                                 fg='white',
                                 selectcolor=rgb((114, 0, 3)),
                                 cursor="hand2",
                                 bg=rgb((114, 0, 3)),
                                 command=command,
                                 image=image)
        RadioID['activebackground'] = rgb((114, 0, 3)),
        RadioID['activeforeground'] = 'white',
        return RadioID


    def After(self, Time, Function):
        return self.windowID.after(Time, Function)

    @staticmethod
    def openImage(image, size):
        ImageID = Image.open(image)
        ImageID = ImageID.resize((size[0], size[1]), Image.ANTIALIAS)
        ImageID = ImageTk.PhotoImage(ImageID)
        return ImageID

import abc

class LayoutWidget:    
    __metaclass__ = abc.ABCMeta

    def __init__(self, gui: (GUI, "GUI to create with to"), masterToAssignTo = None, background = None):
        if not masterToAssignTo:
            masterToAssignTo = gui.windowID
        self.Gui = gui
        self.Frame = gui.createFrame(masterToAssignTo, background)
        self.Widgets = []

    def appendWidget(self, widget):
        self.Widgets.append(widget)

    def prependWidget(self, widget):
        self.Widgets.insert(0, widget)

    @abc.abstractmethod
    def layoutWidgets(self):
        """" layout widget """
        return

class Column(LayoutWidget):  

    def layoutWidgets(self):
        count = 0
        for widget in self.Widgets:
            widget.grid(row = count, column = 0, sticky = 'nsew')
            count += 1
        self.Gui.enableResize(self.Frame)

class Row(LayoutWidget): 

    def layoutWidgets(self):
        count = 0
        for widget in self.Widgets:
            widget.grid(row = 0, column = count, sticky = 'nsew')
            count += 1
        self.Gui.enableResize(self.Frame)
