from . import Qsys
from . import OutputPitchWidget
from . import Defaults
import numpy as np
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
import copy

class Key(Button):
    alpha = NumericProperty(0.0)
    pitch_class = NumericProperty()

    def update_alpha(self):
        self.alpha = float(np.power((self.parent.parent.parent.system.get_probs()[self.pitch_class]), 1/1.2))

class DefaultApplication(Widget):
    """
    """
    outputLabels = ListProperty()
    keys = ListProperty()
    winHeight = NumericProperty()
    winWidth = NumericProperty()
    outputs = ListProperty()
    presses = ListProperty()
    measured = BooleanProperty()
    buttonPositions = ListProperty()

    def __init__(self, argSpectrum=[0], argPsi_not=[0], argFrequency=0., argRoot1=0, argRoot2=0, **kwargs):
        super(DefaultApplication, self).__init__()
        self.SOUND_PATH = 'src/assets/sounds/piano/'
        self.SOUND_EXT = '.wav'
        self.pitches_from_num = Defaults.PitchesSharps().numbers
        self.first = True
        self.playbackLoop = Clock.schedule_once(self.emptyFunct)
        self.spectrum = argSpectrum
        self.n = len(self.spectrum)
        self.psi_not = argPsi_not
        self.frequency = argFrequency
        self.playFunction = self.playSinglePitch
        self.root1 = argRoot1
        self.root2 = argRoot2
        self.holder1 = np.zeros(len(self.spectrum))
        self.holder2 = np.zeros(len(self.spectrum))
        self.outputLabels = [None for i in range(self.n)]
        self.keyslist = [None for i in range(self.n)]
        for i in range(self.n):
            self.keyslist[i] = SoundLoader.load(self.SOUND_PATH + str(i) + self.SOUND_EXT)
            Logger.info('SoundLoader: Loaded ' + self.SOUND_PATH + str(i) + self.SOUND_EXT)
        self.keys = self.keyslist
        for i in enumerate(argPsi_not): #This for loop overrides the given Psi_not and transposes the bare spectrum up to the first root
            self.holder1[(i[0] + self.root1) % self.n] = i[1] #Transpose atom to root of Chord1
            self.holder2[(i[0] + self.root2) % self.n] = i[1] #Transpose atom to root of Chord1
        self.system = Qsys.Qsys(12, self.holder1, 0.01, self.frequency,self.spectrum, self.holder1, self.holder2, self.root1, self.root2)
        self.winHeight = Window.size[1]
        self.winWidth = Window.size[0]
        self.outputs = []
        self.presses = []
        self.measured = False
        self.buttonPositions = self.setButtonPositions()
        self.keyWidgets = [Key(pitch_class=i, x=int(self.buttonPositions[0][i]), y=int(self.buttonPositions[1][i]), text=str(self.pitches_from_num[str(i)])) for i in range(self.n)]
        for i in range(self.n):
            self.ids['main_window'].add_widget(self.keyWidgets[i])
        Logger.info('DefaultApp: Default App Initialized with ' + str(self.n) + ' keys')
        self.schedule()

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

    def addOutputWidget(self):
        outputPitchWidget = OutputPitchWidget.OutputPitchWidget()
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
            self.addOutputWidget()
            self.measured = False
    
    def schedule(self):
        self.playbackLoop.cancel()
        self.main_loop = Clock.schedule_interval(self.application_loop, 1 / 30.)

