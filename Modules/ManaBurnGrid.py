import time

from Conf.Hotkeys import Hotkey
from Conf.Constants import ManaColor, ManaColorFull, Percentage

from Core.GUI import *
from Core.GUIManager import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import ThreadManager

from Engine.ScanStages import ScanStages

EnabledManaBurn = False
ThreadStarted = False

GUIChanges = []


class ManaBurnGrid:
    def __init__(self, ManaLocation, MOUSE_OPTION):
        self.ManaBurn = GUI('ManaBurn', 'Module: Mana Burn')
        self.ManaBurn.DefaultWindow('ManaBurn', [306, 272], [1.2, 2.29])
        self.Setter = GUISetter("ManaBurn")
        self.SendToClient = Hotkey(MOUSE_OPTION)
        self.Scan = ScanStages('ManaBurn')
        self.ThreadManager = ThreadManager("ThreadManaBurn")

        def SetManaBurn():
            global EnabledManaBurn
            if not EnabledManaBurn:
                ButtonEnabled.configure(text='ManaBurn: ON', relief=SUNKEN, bg=rgb((158, 46, 34)))
                print("ManaBurn: ON")
                EnabledManaBurn = True
                CheckingButtons()
                if not ThreadStarted:
                    self.ThreadManager.NewThread(ScanManaBurn)
                else:
                    self.ThreadManager.UnPauseThread()
            else:
                print("ManaBurn: OFF")
                EnabledManaBurn = False
                CheckingButtons()
                ButtonEnabled.configure(text='ManaBurn: OFF', relief=RAISED, bg=rgb((127, 17, 8)))
                self.ThreadManager.PauseThread()

        def ScanManaBurn():
            while EnabledManaBurn:
                Mana = self.Scan.ScanStages(ManaLocation, ManaColor, ManaColorFull)

                if Mana is None:
                    Mana = 0

                manaPercentage = ManaBurnPercentage.get()
                if Mana > manaPercentage or manaPercentage == Mana:
                    self.SendToClient.Press(ManaBurnHotkey.get())              
                time.sleep(1)

        ManaBurnPercentage, InitiatedManaBurnPercentage = self.Setter.Variables.Int('ManaBurnPercentage')
        ManaBurnHotkey, InitiatedManaBurnHotkey = self.Setter.Variables.Str('ManaBurnHotkey')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            CheckingGUI(InitiatedManaBurnPercentage, ManaBurnPercentage.get(), 'ManaBurnPercentage')
            CheckingGUI(InitiatedManaBurnHotkey, ManaBurnHotkey.get(), 'ManaBurnHotkey')

            if len(GUIChanges) != 0:
                for EachChange in range(len(GUIChanges)):
                    self.Setter.SetVariables.SetVar(GUIChanges[EachChange][0], GUIChanges[EachChange][1])

            self.ManaBurn.destroyWindow()

        self.ManaBurn.createButton('Ok', Destroy)

        ''' button enable '''

        ExitButton = self.ManaBurn.createButton('Ok', Destroy)

        global EnabledManaBurn
        if not EnabledManaBurn:
            ButtonEnabled = self.ManaBurn.createButton('ManaBurn: OFF', SetManaBurn)
        else:
            ButtonEnabled = self.ManaBurn.createButton('ManaBurn: ON', SetManaBurn)
            ButtonEnabled.configure(relief=SUNKEN, bg=rgb((158, 46, 34)))

        FrameConfig = self.ManaBurn.createFrame()
        LabelPercentage = self.ManaBurn.createLabel('% Percentage', masterToAssignTo=FrameConfig)
        OptionPercentage = self.ManaBurn.createOption(ManaBurnPercentage, Percentage, masterToAssignTo=FrameConfig)

        LabelHotkey = self.ManaBurn.createLabel('HotKey', masterToAssignTo=FrameConfig)
        OptionHotkey = self.ManaBurn.createOption(ManaBurnHotkey, self.SendToClient.Hotkeys, masterToAssignTo=FrameConfig)

        
        # layout stuff
        rowIndex = 0
        ExitButton.grid(row = rowIndex, column = 0, columnspan = 2, sticky = 'nsew')
        rowIndex += 1

        ButtonEnabled.grid(row = rowIndex, column = 0, columnspan = 2, sticky='nsew')
        rowIndex += 1

        FrameConfig.grid(row = rowIndex, column = 0, sticky = 'nsew')
        rowIndex += 1
        LabelPercentage.grid(row = 0, column = 0, sticky = 'nsew')
        OptionPercentage.grid(row = 0, column = 1, sticky = 'nsew')

        LabelHotkey.grid(row = 1, column = 0, sticky = 'nsew')
        OptionHotkey.grid(row = 1, column = 1, sticky = 'nsew')


        def CheckingButtons():            
            self.ManaBurn.EnableStageRecursive(FrameConfig, EnabledManaBurn)
            ExecGUITrigger()

        CheckingButtons()

        self.ManaBurn.Protocol(Destroy)
        self.ManaBurn.loop()
