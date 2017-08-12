from . import Qsys
from . import OutputPitchWidget
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
import copy

class Key(Button):
    alpha = NumericProperty(0.0)
    pitch_class = NumericProperty()

    def update_alpha(self):
        self.alpha = float(np.power((self.parent.parent.parent.system.get_probs()[self.pitch_class]), 1/1.2))

class DefaultApplication(Widget):
    playFunction = None 
    winHeight = NumericProperty()
    winWidth = NumericProperty()
    buttonPositions = ListProperty()
    outputLabels = ListProperty([None for i in range(12)])
    SOUND_PATH = 'src/assets/sounds/piano/'
    SOUND_EXT = '.wav'
    keyslist = [None for i in range(12)]
    for i in range(12):
        keyslist[i] = SoundLoader.load(SOUND_PATH + str(i) + SOUND_EXT)
    keys = ListProperty(keyslist)
    outputs = ListProperty([])
    presses = ListProperty([])
    measured = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(DefaultApplication, self).__init__()

    def emptyFunct(self, args):
        pass

    def on_start(self, argSpectrum, argPsi_not, argFrequency, argRoot1, argRoot2):
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
        for i in enumerate(argPsi_not): #This for loop overrides the given Psi_not and transposes the bare spectrum up to the first root
            self.holder1[(i[0] + self.root1) % self.n] = i[1] #Transpose atom to root of Chord1
            self.holder2[(i[0] + self.root2) % self.n] = i[1] #Transpose atom to root of Chord1
        self.system = Qsys.Qsys(12, self.holder1, 0.01, self.frequency,self.spectrum, self.holder1, self.holder2, self.root1, self.root2)

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
        for i in range(12):
            self.ids[str(i)].update_alpha()
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

