import time

from Conf.Hotkeys import Hotkey

from tkinter import Grid

from Core.GUI import GUI, Column, Row
from Core.GUIManager import *
from Core.ThreadManager import ThreadManager
from Core.GUISetter import GUISetter

from Engine.ScanStarving import ScanStarving

EnabledFoodEater = False
ThreadStarted = False

class FoodEaterGrid:
    def __init__(self, root, StatsPositions, MOUSE_OPTION):
        self.FoodEater = GUI('FoodEater', 'Module: Food Eater')
        self.FoodEater.DefaultWindow('DefaultWindow', None, None)
        self.ThreadManager = ThreadManager("ThreadFoodEater")
        self.Setter = GUISetter("FoodEater")
        self.SendToClient = Hotkey(MOUSE_OPTION)

        def SetFoodEater():
            global EnabledFoodEater
            if not EnabledFoodEater:
                EnabledFoodEater = True
                ButtonEnabled.configure(text='FoodEater: ON')
                print("FoodEater: ON")                
                CheckingButtons()
                if not ThreadStarted:
                    self.ThreadManager.NewThread(ScanFoodEater)
                else:
                    self.ThreadManager.UnPauseThread()
            else:
                EnabledFoodEater = False
                ButtonEnabled.configure(text='FoodEater: OFF')
                print("FoodEater: OFF")                
                CheckingButtons()
                self.ThreadManager.PauseThread()

        def ScanFoodEater():
            while EnabledFoodEater:
                try:
                    IsStarving = ScanStarving(StatsPositions)
                except Exception:
                    IsStarving = False
                    pass
                if IsStarving:
                    self.SendToClient.Press(VarHotkeyFood.get())
                time.sleep(5)

        
        VarHotkeyFood, _ = self.Setter.Variables.Str('HotkeyFood')            
  
        
        MainColumn = Column(self.FoodEater, background="Green")
        MainColumn.Frame.grid(row = 0, column = 0, sticky = 'nsew')

        # close button
        OkButton = self.FoodEater.createButton('Ok', self.FoodEater.destroyWindow, MainColumn.Frame)  
        
        # enable button 
        global EnabledFoodEater
        if not EnabledFoodEater:
            ButtonEnabled = self.FoodEater.createButton('FoodEater: OFF', SetFoodEater, MainColumn.Frame)
        else:
            ButtonEnabled = self.FoodEater.createButton('FoodEater: ON', SetFoodEater, MainColumn.Frame)
 

        #build HotkeyRow    
        HotkeyRow = Row(self.FoodEater, MainColumn.Frame)
        LabelHotkey = self.FoodEater.createLabel('Hotkey Food: ', HotkeyRow.Frame)
        HotkeyFood = self.FoodEater.createOption(VarHotkeyFood, self.SendToClient.Hotkeys, masterToAssignTo=HotkeyRow.Frame)
        HotkeyRow.appendWidget(LabelHotkey)
        HotkeyRow.appendWidget(HotkeyFood)
        HotkeyRow.layoutWidgets()

        MainColumn.appendWidget(OkButton)
        MainColumn.appendWidget(ButtonEnabled)
        MainColumn.appendWidget(HotkeyRow.Frame)
        MainColumn.layoutWidgets()

        self.FoodEater.enableResize(self.FoodEater.windowID)

        def CheckingButtons():
            self.FoodEater.EnableStageRecursive(HotkeyRow.Frame, EnabledFoodEater)
            ExecGUITrigger()

        CheckingButtons()

        self.FoodEater.loop()

