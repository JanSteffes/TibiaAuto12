import time

from Conf.Hotkeys import Hotkey
from Conf.Constants import ManaColor, ManaColorFull, Percentage

from Core.GUI import *
from Core.GUIManager import *
from Core.GUISetter import GUISetter
from Core.ThreadManager import ThreadManager

from Engine.ScanStages import ScanStages

EnabledAutoMana = False
ThreadStarted = False

GUIChanges = []

'''
Use potion if mana is below specific percentage value
'''
class AutoManaGrid:
    def __init__(self, ManaLocation, MOUSE_OPTION):
        self.AutoMana = GUI('AutoMana', 'Module: Auto Mana')     
        self.AutoMana.DefaultWindow('AutoMana', [306, 272], [1.2, 2.29])
        self.Setter = GUISetter("ManaLoader")
        self.SendToClient = Hotkey(MOUSE_OPTION)
        self.Scan = ScanStages('Mana')
        self.ThreadManager = ThreadManager("ThreadAutoMana")
        self.AutoMana.enableResize(self.AutoMana.windowID)

        def SetAutoMana():
            global EnabledAutoMana
            if not EnabledAutoMana:
                EnabledAutoMana = True
                CheckingButtons()
                if not ThreadStarted:
                    self.ThreadManager.NewThread(ScanAutoMana)
                else:
                    self.ThreadManager.UnPauseThread()
            else:
                print("AutoMana: OFF")
                EnabledAutoMana = False
                CheckingButtons()
                self.ThreadManager.PauseThread()

        def ScanAutoMana():
            while EnabledAutoMana:
                Mana = self.Scan.ScanStages(ManaLocation, ManaColor, ManaColorFull)
                #print('automana is ', Mana)
                if Mana is None:
                    Mana = 0

                if ManaCheckStageTwo.get():
                    stage_two = ManaPercentageStageTwo.get()
                    #print('stage two is ', stage_two)
                    if Mana > stage_two or stage_two == Mana:
                        self.SendToClient.Press(ManaHotkeyStageTwo.get())
                        #print("Pressed ", ManaHotkeyStageTwo.get())
                elif ManaCheckStageOne.get():
                    stage_one = ManaPercentageStageOne.get()
                    #print('stage one is ', stage_one)
                    if Mana > stage_one or stage_one == Mana:
                        self.SendToClient.Press(ManaHotkeyStageOne.get())
                        #print("Pressed ", ManaHotkeyStageOne.get())
                else:
                    print("Modulo Not Configured")
                time.sleep(5)
            

        VarCheckPrint, InitiatedCheckPrint = self.Setter.Variables.Bool('CheckPrint')
        VarCheckBuff, InitiatedCheckBuff = self.Setter.Variables.Bool('CheckBuff')

        ManaCheckStageOne, InitiatedManaCheckStageOne = self.Setter.Variables.Bool('ManaCheckStageOne')
        ManaCheckStageTwo, InitiatedManaCheckStageTwo = self.Setter.Variables.Bool('ManaCheckStageTwo')

        ManaPercentageStageOne, InitiatedManaPercentageStageOne = self.Setter.Variables.Int('ManaPercentageStageOne')
        ManaHotkeyStageOne, InitiatedManaHotkeyStageOne = self.Setter.Variables.Str('ManaHotkeyStageOne')

        ManaPercentageStageTwo, InitiatedManaPercentageStageTwo = self.Setter.Variables.Int('ManaPercentageStageTwo')
        ManaHotkeyStageTwo, InitiatedManaHotkeyStageTwo = self.Setter.Variables.Str('ManaHotkeyStageTwo')

        def CheckingGUI(Init, Get, Name):
            if Get != Init:
                GUIChanges.append((Name, Get))

        def Destroy():
            CheckingGUI(InitiatedCheckPrint, VarCheckPrint.get(), 'CheckPrint')
            CheckingGUI(InitiatedCheckBuff, VarCheckBuff.get(), 'CheckBuff')
            CheckingGUI(InitiatedManaCheckStageOne, ManaCheckStageOne.get(), 'ManaCheckStageOne')
            CheckingGUI(InitiatedManaCheckStageTwo, ManaCheckStageTwo.get(), 'ManaCheckStageTwo')
            CheckingGUI(InitiatedManaPercentageStageOne, ManaPercentageStageOne.get(), 'ManaPercentageStageOne')
            CheckingGUI(InitiatedManaHotkeyStageOne, ManaHotkeyStageOne.get(), 'ManaHotkeyStageOne')
            CheckingGUI(InitiatedManaPercentageStageTwo, ManaPercentageStageTwo.get(), 'ManaPercentageStageTwo')
            CheckingGUI(InitiatedManaHotkeyStageTwo, ManaHotkeyStageTwo.get(), 'ManaHotkeyStageTwo')

            if len(GUIChanges) != 0:
                for EachChange in range(len(GUIChanges)):
                    self.Setter.SetVariables.SetVar(GUIChanges[EachChange][0], GUIChanges[EachChange][1])

            self.AutoMana.destroyWindow()

        # create ui elements

        # frame for controls
        def createControlsFrame():
            AutoManaControlsFrame = self.AutoMana.createFrame(background="Green")
            # self.AutoMana.addButton('Ok', Destroy, [73, 21], [115, 240])
            okButton = self.AutoMana.createButton('Ok', Destroy, masterToAssignTo = AutoManaControlsFrame)
            
            ''' button enable AutoMana '''

            global EnabledAutoMana
            if not EnabledAutoMana:
                # ButtonEnabled = self.AutoMana.addButton('AutoMana: OFF', SetAutoMana, [287, 23], [11, 211])
                ButtonEnabled = self.AutoMana.createButton('AutoMana: OFF', SetAutoMana, masterToAssignTo=AutoManaControlsFrame)
            else:
                # ButtonEnabled = self.AutoMana.addButton('AutoMana: ON', SetAutoMana, [287, 23], [11, 211])
                ButtonEnabled = self.AutoMana.createButton('AutoMana: ON', SetAutoMana,  masterToAssignTo=AutoManaControlsFrame)
                ButtonEnabled.configure(relief=SUNKEN, bg=rgb((158, 46, 34)))


            ''' checks for print in client stuff '''     
            CheckPrint = self.AutoMana.createCheck(VarCheckPrint, InitiatedCheckPrint, "Print on Tibia's screen", masterToAssignTo=AutoManaControlsFrame)
            CheckPrint.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))
            CheckBuff = self.AutoMana.createCheck(VarCheckBuff, InitiatedCheckBuff, "Don't Buff", masterToAssignTo=AutoManaControlsFrame)
            CheckBuff.configure(bg=rgb((114, 94, 48)), activebackground=rgb((114, 94, 48)), selectcolor=rgb((114, 94, 48)))

            #layout
            AutoManaControlsFrame.grid(row = 0, column = 0, sticky = 'nsew')
            okButton.grid(row = 0, column = 0, sticky = 'nsew')
            ButtonEnabled.grid(row = 1, column = 0, sticky = 'nsew')
            CheckPrint.grid(row = 2, column = 0, sticky = 'nsew')
            CheckBuff.grid(row = 3, column = 0, sticky = 'nsew')

            # autoresize controls in frame
            self.AutoMana.enableResize(AutoManaControlsFrame)      

            return AutoManaControlsFrame
            
        
        def createConfigFrame():
            # frame for configurations (e.g. stages)
            AutoManaConfigureFrame = self.AutoMana.createFrame(background="Yellow")       

            def CreateStage(index, InitiatedManaCheck, ManaCheckVar, ManaPercentage, HotkeyVar, background):
                AutoManaConfigureStateFrame = self.AutoMana.createFrame( masterToAssignTo=AutoManaConfigureFrame, background = background)

                # create controls
                ManaCheck = self.AutoMana.createCheck(ManaCheckVar, InitiatedManaCheck, "Enable Stage " + str(index), masterToAssignTo=AutoManaConfigureStateFrame)
                PercLabel = self.AutoMana.createLabel('% Percentage', masterToAssignTo=AutoManaConfigureStateFrame)
                PercOption = self.AutoMana.createOption(ManaPercentage, Percentage, masterToAssignTo=AutoManaConfigureStateFrame)
                HotKeylabel = self.AutoMana.createLabel('HotKey', masterToAssignTo=AutoManaConfigureStateFrame)
                HotKeyOption = self.AutoMana.createOption(HotkeyVar, self.SendToClient.Hotkeys, masterToAssignTo=AutoManaConfigureStateFrame)

                # layout
                ManaCheck.grid(row=0, column = 0,columnspan = 2, sticky = 'nsew')
                PercLabel.grid(row=1, column = 0, sticky = 'nsew')
                PercOption.grid(row=1, column = 1, sticky = 'nsew')
                HotKeylabel.grid(row=2, column = 0, sticky = 'nsew')
                HotKeyOption.grid(row=2, column = 1, sticky = 'nsew')

                #autresize controls in frame                   
                self.AutoMana.enableResize(AutoManaConfigureStateFrame)

                return AutoManaConfigureStateFrame

            StageOne = CreateStage(1, InitiatedManaCheckStageOne, ManaCheckStageOne, ManaPercentageStageOne, ManaHotkeyStageOne, "Red")
            StageTwo = CreateStage(2, InitiatedManaCheckStageTwo, ManaCheckStageTwo, ManaPercentageStageTwo, ManaHotkeyStageTwo, "Orange")

            # layout config in frame
            StageOne.grid(row = 0, column = 0, sticky = 'nsew')
            StageTwo.grid(row = 1, column = 0, sticky = 'nsew')

            #autresize controls in frame                   
            self.AutoMana.enableResize(AutoManaConfigureFrame)

            return AutoManaConfigureFrame


        # create controls and config frames
        ControlsFrame = createControlsFrame()
        ConfigFrame = createConfigFrame()

        # layout frames
        ControlsFrame.grid(row = 0, column = 0, sticky = 'nsew')
        ConfigFrame.grid(row = 1, column = 0, sticky = 'nsew')
        
        def EnableStageRecursive(Stage, enable = True):
            if enable:
                stateToSet = 'enable'
            else:
                stateToSet = 'disable'
            for child in Stage.winfo_children():    
                childChildren = child.winfo_children()
                if childChildren and len(childChildren) > 0:
                    EnableStageRecursive(child)
                else:
                    try:
                        child.configure(state=stateToSet)
                    except Exception:
                        print('exception while configurting child')

        def CheckingButtons():
            EnableStageRecursive(ConfigFrame, EnabledAutoMana)        
            ExecGUITrigger()

        # CheckingButtons()

        self.AutoMana.Protocol(Destroy)
        self.AutoMana.loop()
