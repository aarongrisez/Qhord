from .. import Qsys
from ..components import OutputPitchWidget
from .. import Defaults
import numpy as np
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
import copy

class Walkthrough1(Popup):
    pass

class Walkthrough2(Popup):
    pass

class Walkthrough3(Popup):
    pass

class Walkthrough4(Popup):
    pass

class Key(Button):
    alpha = NumericProperty(0.0)
    pitch_class = NumericProperty()
    systemRef = '' #So that each key has a reference to the system (NOT a copy of the system)
    
    def __init__(self, inPC, inSys, x, y, text):
        """Initializes the key
        """
        super(Key,self).__init__(x=x,y=y,text=text)
        self.pitch_class = inPC
        self.systemRef = inSys

    def update_alpha(self):
        self.alpha = float(np.power((self.systemRef.get_probs()[self.pitch_class]), 1/1.2))


class KeyboardScreen(Screen):
    outputLabels = ListProperty()
    keys = ListProperty()
    winHeight = NumericProperty()
    winWidth = NumericProperty()
    outputs = ListProperty()
    presses = ListProperty()
    measured = BooleanProperty()
    buttonPositions = ListProperty()
    main_loop = ''
    

    def __init__(self, **kwargs):
        """Initializes this Screen by doing everything that only needs to happen once.
        """
        super(KeyboardScreen, self).__init__()
        self.SOUND_PATH = 'src/assets/sounds/piano/'
        self.SOUND_EXT = '.wav'
        #self.pitches_from_num = Defaults.PitchesSharps().numbers
        ##CHANGED to pentatonic mode
        self.pitches_from_num = Defaults.PitchesSharps().numbers5
        self.pitchClasses = Defaults.PitchesSharps().pitchClasses['C_pentatonic']
        self.playFunction = self.playSinglePitch
        self.winHeight = Window.size[1]
        self.winWidth = Window.size[0]
        self.outputs = []
        self.presses = []
        self.measured = False
        
    def startSimulation(self, argSpectrum=[0], argPsi_not=[0], argFrequency=0., argRoot1=0, argRoot2=0):
        """Runs every time the simulation starts, 
           initializing everything user-choice dependent.
        """
        self.spectrum = argSpectrum
        self.n = len(self.spectrum)
        self.psi_not = argPsi_not
        self.frequency = argFrequency
        self.root1 = argRoot1
        self.root2 = argRoot2
        self.holder1 = np.zeros(len(self.spectrum))
        self.first = True
        self.holder2 = np.zeros(len(self.spectrum))
        self.outputLabels = [None for i in range(self.n)]
        self.keyslist = [None for i in range(self.n)]
        for i in range(self.n):
            self.keyslist[i] = SoundLoader.load(self.SOUND_PATH + str(self.pitches_from_num[str(i)]) + self.SOUND_EXT)
            Logger.info('SoundLoader: Loaded ' + self.SOUND_PATH + str(self.pitches_from_num[str(i)]) + self.SOUND_EXT)
        self.keys = self.keyslist
        for i in enumerate(argPsi_not): #This for loop overrides the given Psi_not and transposes the bare spectrum up to the first root
            self.holder1[(i[0] + self.root1) % self.n] = i[1] #Transpose atom to root of Chord1
            self.holder2[(i[0] + self.root2) % self.n] = i[1] #Transpose atom to root of Chord1
        self.system = Qsys.Qsys(self.n, self.holder1, 0.01, self.frequency,self.spectrum, self.holder1, self.holder2, self.root1, self.root2)
        self.buttonPositions = self.setButtonPositions()
        self.keyWidgets = [Key(i, self.system, int(self.buttonPositions[0][i]), int(self.buttonPositions[1][i]), str(self.pitches_from_num[str(i)])) for i in range(self.n)]
        for i in range(self.n):
            self.ids['main_window'].add_widget(self.keyWidgets[i])
        self.main_loop = Clock.schedule_interval(self.application_loop, 1 / 30.)
        Logger.info('DefaultApp: Default App Initialized with ' + str(self.n) + ' keys')
        
    def stopSimulation(self):
        """Stops the simulation, deleting all simulation-specific data that's big enough to matter or shows up on the screen 
           and killing the Qsys to free up memory and CPU time.
        """
        Clock.unschedule(self.application_loop)
        self.system = ''
        keyWidgets = []
        outputs = []
        presses = []
        for outputWidget in self.ids['output_window'].children:
            self.ids['output_window'].remove_widget(outputWidget)
        for keyWidget in self.keyWidgets:
            self.ids['main_window'].remove_widget(keyWidget)
        for i in range(self.n):
            self.keyslist[i].unload() 
            Logger.info('SoundLoader: Unloaded ' + self.SOUND_PATH + str(i) + self.SOUND_EXT)
 

    def emptyFunct(self, args):
        pass

    def on_start(self, argSpectrum, argPsi_not, argFrequency, argRoot1, argRoot2):
        pass

    def on_stop(self):
        pass

    def setButtonPositions(self):
        boundingFunction = lambda x: .5 - 1 / (self.winHeight * 4 * (x - 0.501) ** 2)
        xoffset = .1 * self.winWidth
        xstep = self.winWidth * .8 / self.n
        x_rel_pos = np.array([.1 * self.winWidth + i * xstep for i in range(self.n)]) / self.winWidth
        y_rel_pos = boundingFunction(x_rel_pos)
        xpos = x_rel_pos * self.winWidth
        ypos = y_rel_pos * self.winHeight
        return [xpos, ypos] 

    def solve_ode(self, *args):
        self.system.run()

    def measure_system(self, key):
        """
        Currently, you will hear only the outcome of the measurement
        """
        self.system.measure(key)
        self.outputLabels = [self.system.lastKey, self.system.lastOutput]
        self.playFunction() 
        self.measured = True

    def playSinglePitch(self):
        if self.keys[self.outputLabels[1]].state == 'play':
            self.keys[self.outputLabels[1]].stop()
        self.keys[self.outputLabels[1]].play()

    def addOutputWidget(self,output,key):
        outputPitchWidget = OutputPitchWidget.OutputPitchWidget(self.pitchClasses[output],self.pitchClasses[key])
        self.ids['output_window'].add_widget(outputPitchWidget)
        outputPitchWidget.start()

    def application_loop(self, *args):
        if self.first:
            self.first = False
        self.solve_ode()
        for i in range(self.n):
            self.keyWidgets[i].update_alpha()
        if self.measured == False:
            self.outputs.append(None)
            self.presses.append(None)
        elif self.measured == True:
            self.outputs.append(self.system.lastOutput)
            self.presses.append(self.system.lastKey)
            self.addOutputWidget(self.system.lastOutput,self.system.lastKey)
            self.measured = False

