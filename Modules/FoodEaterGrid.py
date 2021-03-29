import time

from Conf.Hotkeys import Hotkey

from Core.GUI import *
from Core.GUIManager import *
from Core.ThreadManager import ThreadManager
from Core.GUISetter import GUISetter

from Engine.ScanStarving import ScanStarving

EnabledFoodEater = False
ThreadStarted = False

class FoodEater:
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

        self.FoodEater.addButtonGrid('Ok', self.FoodEater.destroyWindow, 0,0)
        LabelHotkey = self.FoodEater.addLabelGrid('Hotkey Food: ', 2, 0)
        HotkeyFood = self.FoodEater.addOptionGrid(VarHotkeyFood, self.SendToClient.Hotkeys, 3, 0, 8)
        
        global EnabledFoodEater
        if not EnabledFoodEater:
            ButtonEnabled = self.FoodEater.addButtonGrid('FoodEater: OFF', SetFoodEater, 1, 0)
        else:
            ButtonEnabled = self.FoodEater.addButtonGrid('FoodEater: ON', SetFoodEater, 1, 0)

        def CheckingButtons():
            if EnabledFoodEater:
                Disable(LabelHotkey)
                Disable(HotkeyFood)
            else:
                Enable(LabelHotkey)
                Enable(HotkeyFood)
            ExecGUITrigger()

        CheckingButtons()

        self.FoodEater.loop()

