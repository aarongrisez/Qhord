from .. components import OutputPitchWidget
from .. import Defaults
import json
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.app import App
import copy
import numpy as np

class TutorialKey(Button):
    alpha = NumericProperty(0.0)
    pitch_class = NumericProperty()
    
    def __init__(self, inPC, x, y, text, *kwargs):
        """Initializes the key
        """
        Logger.info("Init TutorialKey")
        super(TutorialKey,self).__init__(x=x,y=y,text=text)
        self.pitch_class = inPC

    def set_alpha(self, value):
        self.alpha = value 

class TutorialScreen(Screen):
    currentStepNumber = NumericProperty(0)
    outputLabels = ListProperty()
    keys = ListProperty()
    winHeight = NumericProperty()
    winWidth = NumericProperty()
    outputs = ListProperty()
    presses = ListProperty()
    measured = BooleanProperty()
    buttonPositions = ListProperty()
    keyWidgets = ListProperty()
    text = Label()
 
    def __init__(self, **kwargs):
        super(Screen, self).__init__() 
        Logger.info("Init Tutorial Screen")
        self.text.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.add_widget(self.text)
        self.n = 5
        self.currentStepNumber = 0
        self.SOUND_PATH = 'src/assets/sounds/piano/'
        self.SOUND_EXT = '.wav'
        #self.pitches_from_num = Defaults.PitchesSharps().numbers
        ##CHANGED to pentatonic mode
        self.pitches_from_num = Defaults.PitchesSharps().numbers5
        self.pitchClasses = Defaults.PitchesSharps().pitchClasses['C_pentatonic']
        self.winHeight = Window.size[1]
        self.winWidth = Window.size[0]
        self.currentTutorial = "tutorial1"
        with open('src/screens/json/Tutorial1.json') as file:
            self.data = json.load(file)
        Logger.info('Tutorial Screen: Loaded tutorial json')

    def on_enter(self):
        Logger.info("Entered Tutorial Screen")
        self.currentStepNumber = 0
        self.keyslist = [None for i in range(self.n)]
        for i in range(self.n):
            self.keyslist[i] = SoundLoader.load(self.SOUND_PATH + str(self.pitches_from_num[str(i)]) + self.SOUND_EXT)
            Logger.info('SoundLoader: Loaded ' + self.SOUND_PATH + str(self.pitches_from_num[str(i)]) + self.SOUND_EXT)
        self.keys = self.keyslist
        self.buttonPositions = self.setButtonPositions()
        self.keyWidgets = [TutorialKey(i, int(self.buttonPositions[0][i]), int(self.buttonPositions[1][i]), str(self.pitches_from_num[str(i)])) for i in range(self.n)]
        for i in range(self.n):
            self.ids['main_window'].add_widget(self.keyWidgets[i])
        Logger.info('TutorialApp: Tutorial App Initialized with ' + str(self.n) + ' keys')
        self.start_tutorial()

    def start_tutorial(self):
        Logger.info('TutorialApp: Tutorial started')
        self.currentStep = self.data[self.currentTutorial]["steps"][self.currentStepNumber]
        self.text.text = self.currentStep["text"]
        self.set_action_trigger(self.currentStep["trigger"])
        for (i,j) in enumerate(self.keyWidgets):
            j.set_alpha(self.currentStep["alpha"][i])
            j.canvas.ask_update()

    def set_action_trigger(self, trigger_key, *kwargs):
        Logger.info('Setting new action trigger to ' + str(trigger_key))
        self.keyWidgets[trigger_key].bind(on_press=self.next_step)

    def unbindAction(self, trigger_key, *kwargs):
        self.keyWidgets[trigger_key].funbind('on_press', self.next_step)

    def end_tutorial(self, *kwargs):
        App.screenManager.current = 'welcomeScreen'

    def playSinglePitch(self):
        if self.keys[self.outputLabels[1]].state == 'play':
            self.keys[self.outputLabels[1]].stop()
        self.keys[self.outputLabels[1]].play()

    def addOutputWidget(self,output,key):
        outputPitchWidget = OutputPitchWidget.OutputPitchWidget(self.pitchClasses[output],self.pitchClasses[key])
        self.ids['output_window'].add_widget(outputPitchWidget)
        outputPitchWidget.start()

    def next_step(self, *kwargs):
        #Advances tutorial to the next step
        self.currentStep["completed"] = True
        if self.currentStepNumber < len(self.data[self.currentTutorial]["steps"]) - 1:
            Logger.info('Tutorial Screen: On step ' + str(self.currentStepNumber))
            self.outputLabels = [self.currentStep["trigger"], self.currentStep["heard"]]
            self.addOutputWidget(self.currentStep["trigger"], self.currentStep["heard"])
            self.playSinglePitch()
            self.unbindAction(self.currentStep["trigger"])
            self.currentStepNumber += 1
            self.currentStep = self.data[self.currentTutorial]["steps"][self.currentStepNumber]
            self.text.text = self.currentStep["text"]
            for (i,j) in enumerate(self.keyWidgets):
                j.set_alpha(self.currentStep["alpha"][i])
                j.canvas.ask_update()
                Logger.info(str(j.alpha))
            self.set_action_trigger(self.currentStep["trigger"])
            Logger.info(self.currentStep["text"])
        elif self.currentStepNumber == len(self.data[self.currentTutorial]["steps"]) - 1:
            more_button = Button(on_press=self.walkthrough)
            self.add_widget(more_button)
        else:
            Logger.info('Tutorial complete!')
    
    def walkthrough(self):
        pass
        
    def addOutputWidget(self,output,key):
        outputPitchWidget = OutputPitchWidget.OutputPitchWidget(self.pitchClasses[output],self.pitchClasses[key])
        self.ids['output_window'].add_widget(outputPitchWidget)
        outputPitchWidget.start()
        
    def setButtonPositions(self):
        Logger.info("Set Button Positions, Tutorial Screen")
        boundingFunction = lambda x: .5 - 1 / (self.winHeight * 4 * (x - 0.501) ** 2)
        xoffset = .1 * self.winWidth
        xstep = self.winWidth * .8 / self.n
        x_rel_pos = np.array([.1 * self.winWidth + i * xstep for i in range(self.n)]) / self.winWidth
        y_rel_pos = boundingFunction(x_rel_pos)
        xpos = x_rel_pos * self.winWidth
        ypos = y_rel_pos * self.winHeight
        return [xpos, ypos] 
