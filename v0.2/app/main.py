from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from src import DefaultApplication
from kivy.clock import Clock
from settingsjson import settings_json
from kivy.lang import Builder
from kivy.logger import Logger
import numpy as np

#Builder.load_file('SpectrumScreen.kv')
Builder.load_file('src/kv/HamiltonianScreen.kv')
Builder.load_file('src/kv/WelcomeScreen.kv')
Builder.load_file('src/kv/key.kv')

def WinClass(size):
    """
    This class contains information about the window created for the app
    """
    aspectRatio = size[0] / size[1]
    if aspectRatio == 4./3:
        return '4:3' 

class ColorScheme():
    """
    Setup color scheme for the application
    """
    Background = 0.05, 0.39, 0.48, 1
    ButtonFill = 1, 1, 1 
    ButtonEdge = 0.031, 0.329, 0.412, 1
    name = "default"

class WidgetDefaults(object):
    """
    Setup default sizes for widgets (this is mostly to help debugging the UI)
    """

    def __init__(self, winClass):
        
        if winClass == '4:3':
            self.KEY_WIDTH = '50dp'
            self.KEY_HEIGHT = '50dp'
        else:
            self.KEY_WIDTH = '30dp'
            self.KEY_HEIGHT = '30dp'

class Spectra():
    defaults = {
    'Major': [.45, 0, 0, 0, .35, 0, 0, .2, 0, 0, 0, 0],
    'Minor':  [.45, 0, 0, .35, 0, 0, 0, .2, 0, 0, 0, 0],
    'Augmented': [.45, 0, 0, 0, .35, 0, 0, 0, .2, 0, 0, 0], 
    'Diminished': [.45, 0, 0, .35, 0, 0, .2, 0, 0, 0, 0, 0],
    'Tritone': [.5, 0, 0, 0, 0, 0, .5, 0, 0, 0, 0, 0]
    }

class PitchesSharps():
    letters = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    numbers = {'0': 'C', '1': 'C#', '2': 'D', '3': 'D#', '4': 'E', '5': 'F', '6': 'F#', '7': 'G', '8': 'G#', '9': 'A', '10': 'A#', '11': 'B'}
    
class MainScreenManager(ScreenManager): 
    pass 

class WelcomeScreen(Screen): 
    pass 

class CreditsScreen(Screen):
    pass

class SpectrumScreen(Screen): 
    spectrum = np.zeros(11) 
    psi_not = np.zeros(11)
    
    def update_spectrum(self): 
        for i in range(11): self.spectrum[i] = self.ids[str(i)].value
        norm = sum(self.spectrum)
        if norm != 0:
            self.spectrum = self.spectrum / norm #Normalizes the spectrum immediately
        self.ids['spectrumLabel'].text = str(np.around(self.spectrum, decimals=2))

    def update_psi_not(self):
        for i in range(11):
           self.psi_not[i] = self.ids[str(i + 12)].value
        norm = sum(self.psi_not)
        if norm != 0:
            self.psi_not = self.psi_not / norm #Normalizes the initial condition immediately
        self.ids['psi_notLabel'].text = str(np.around(self.psi_not, decimals=2))

class HamiltonianScreen(Screen):
    chord = StringProperty('Major')
    frequency = NumericProperty(10.0)
    root1 = NumericProperty(0)
    root2 = NumericProperty(7)

class DefaultApplicationScreen(Screen):
    pass

class MainApp(App):

#    def initializeApp(self, *kwargs):
#        spectrum = self.screenManager.ids['spectrumScreen'].spectrum
#        psi_not = self.screenManager.ids['spectrumScreen'].psi_not
#        self.screenManager.ids['defaultApp'].children[0].on_start(spectrum, psi_not)
 
    def initializeApp(self, *kwargs):
        spectrum = self.spectra.defaults[self.screenManager.ids['hamiltonianScreen'].chord]
        frequency = float(self.screenManager.ids['hamiltonianScreen'].frequency)
        root1 = int(self.screenManager.ids['hamiltonianScreen'].root1)
        root2 = int(self.screenManager.ids['hamiltonianScreen'].root2)
        self.screenManager.ids['defaultApp'].children[0].on_start(spectrum, spectrum, frequency, root1, root2)

    def initializeEmptyApp(self, *kwargs):
    	pass

    def build(self):
        self.colorScheme = ColorScheme()
        self.spectra = Spectra()
        self.winSize = (float(Window.width), float(Window.height))
        self.winClass = WinClass((float(Window.width), float(Window.height)))
        Logger.info('Build: Using WindowClass ' + str(self.winClass))
        self.widgetSizes = WidgetDefaults(self.winClass)
        self.screenManager = MainScreenManager()
        self.mainLoop = Clock.schedule_once(self.initializeEmptyApp)
        self.pitches = PitchesSharps()
        Logger.info('Build: App build successful')
        return self.screenManager

    def on_pause(self):
        self.get_running_app.stop()
        self.tracker.stats.print_summary()
        Logger.info('Runtime: Pausing application')

    def app_start(self):
        self.screenManager.ids['defaultApp'].children[0].schedule()
        Logger.info('Runtime: Starting application')

    def app_stop(self):
        if self.screenManager.current != 'defaultApplicationScreen':
            self.mainLoop.cancel()        
        Logger.info('Runtime: Stopping application')

if __name__=="__main__":
    MainApp().run()
