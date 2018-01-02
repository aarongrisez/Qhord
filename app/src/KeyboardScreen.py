from . import Qsys
from . import OutputPitchWidget
from . import Defaults
from .Key import Key
import numpy as np
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
import copy


class KeyboardScreen(Screen):
    outputLabels = ListProperty()
    pitches = ListProperty()
    winHeight = NumericProperty()
    winWidth = NumericProperty()
    outputs = ListProperty()
    presses = ListProperty()
    measured = BooleanProperty()
    buttonPositions = ListProperty()
    lastOutput = StringProperty()
    lastKey = StringProperty()
    main_loop = ''
    

    def __init__(self, **kwargs):
        """Initializes this Screen by doing everything that only needs to happen once.
        """
        super(KeyboardScreen, self).__init__()
        self.SOUND_PATH = 'src/assets/sounds/piano/'
        self.SOUND_EXT = '.wav'
        self.pitches_from_num = Defaults.PitchesSharps().numbers
        self.winHeight = Window.size[1]
        self.winWidth = Window.size[0]
        self.outputs = []
        self.presses = []
        self.measured = False
        self.lastOutput
        
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
        self.holder2 = np.zeros(len(self.spectrum))
        self.outputLabels = [None for i in range(self.n)]
        self.pitches = [None for i in range(self.n)]
        for i in range(self.n):
            self.pitches[i] = SoundLoader.load(self.SOUND_PATH + str(i) + self.SOUND_EXT)
            Logger.info('SoundLoader: Loaded ' + self.SOUND_PATH + str(i) + self.SOUND_EXT)
        for i in enumerate(argPsi_not): #This for loop overrides the given Psi_not and transposes the bare spectrum up to the first root
            self.holder1[(i[0] + self.root1) % self.n] = i[1] #Transpose atom to root of Chord1
            self.holder2[(i[0] + self.root2) % self.n] = i[1] #Transpose atom to root of Chord1
        self.system = Qsys.Qsys(12, self.holder1, 0.01, self.frequency,self.spectrum, self.holder1, self.holder2, self.root1, self.root2)
        self.buttonPositions = self.setButtonPositions()
        self.keyWidgets = [Key(i, self.pitches, self.system, int(self.buttonPositions[0][i]), int(self.buttonPositions[1][i]), str(self.pitches_from_num[str(i)])) for i in range(self.n)]
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
        self.outputs = []
        self.presses = []
        for outputWidget in self.ids['output_window'].children:
            self.ids['output_window'].remove_widget(outputWidget)
        for keyWidget in self.keyWidgets:
            self.ids['main_window'].remove_widget(keyWidget)
        self.keyWidgets = []

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
    
    def addOutputWidget(self,output,key):
        outputPitchWidget = OutputPitchWidget.OutputPitchWidget(output,key)
        self.ids['output_window'].add_widget(outputPitchWidget)
        outputPitchWidget.start()

    def application_loop(self, *args):
        self.system.run()
        for i in range(self.n):
            curKey = self.keyWidgets[i]
            curKey.update_alpha(self.system.get_probs())
            if curKey.measured:
                self.measured = True
                curKey.measured = False
                self.lastKey = str(curKey.pitch_class)
                self.lastOutput = str(curKey.output)
        if self.measured == False:
            self.outputs.append(None)
            self.presses.append(None)
        else:
            self.outputs.append(self.lastOutput)
            self.presses.append(self.lastKey)
            self.addOutputWidget(self.lastOutput,self.lastKey)
            self.measured = False

