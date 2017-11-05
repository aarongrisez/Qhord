from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from src import DefaultApplication
from src import Defaults
from kivy.clock import Clock
from settingsjson import settings_json
from kivy.lang import Builder
from kivy.logger import Logger
import numpy as np

#Builder.load_file('SpectrumScreen.kv')
Builder.load_file('src/kv/HamiltonianScreen.kv')
Builder.load_file('src/kv/WelcomeScreen.kv')
Builder.load_file('src/kv/DefaultApplication.kv')
Builder.load_file('src/kv/key.kv')
Builder.load_file('src/kv/CustomizeHamiltonianScreen.kv')

class MainScreenManager(ScreenManager): 
    pass 

class WelcomeScreen(Screen): 
    pass 

class CreditsScreen(Screen):
    pass

class CustomizeHamiltonianScreen(Screen):
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

class ChordToggleButton(ToggleButton):
    pass

class Root1ToggleButton(ToggleButton):
    pass

class Root2ToggleButton(ToggleButton):
    pass

class HamiltonianScreen(Screen):
    chord = StringProperty('Major')
    frequency = NumericProperty(10.0)
    root1 = NumericProperty(0)
    root2 = NumericProperty(7)
    n = NumericProperty(2)

    def __init__(self, **kwargs):
        super(HamiltonianScreen, self).__init__()
        #STOPPED HERE!!!! Need to get class definitions for root1 and root2 buttons
        self.root1Buttons = [Root1ToggleButton() for i in range(self.n)]
        #for i in range(self.n):
        #    self.ids['main_window'].add_widget(self.keyWidgets[i])
        Logger.info('Build: Hamiltonian Screen Built')

#class DefaultApplicationScreen(Screen):
#    pass

class MainApp(App):

#    def initializeApp(self, *kwargs):
#        spectrum = self.screenManager.ids['spectrumScreen'].spectrum
#        psi_not = self.screenManager.ids['spectrumScreen'].psi_not
#        self.screenManager.ids['defaultApp'].children[0].on_start(spectrum, psi_not)
 
    def initializeApp(self, *kwargs):
        spectrum = self.spectra.defaults[self.screenManager.ids['hamiltonianScreen'].chord]
      #  frequency = float(self.screenManager.ids['hamiltonianScreen'].frequency)
    #root1 = int(self.screenManager.ids['hamiltonianScreen'].root1)
     #   root2 = int(self.screenManager.ids['hamiltonianScreen'].root2)
      #  self.screenManager.ids['defaultAppScreen'].add_widget(DefaultApplication.DefaultApplication(spectrum, spectrum, frequency, root1, root2))

    def initializeEmptyApp(self, *kwargs):
    	pass

    def build(self):
        self.colorScheme = Defaults.ColorScheme()
        self.spectra = Defaults.Spectra()
        self.winSize = (float(Window.width), float(Window.height))
        self.winClass = Defaults.WinClass().getWinClass((float(Window.width), float(Window.height)))
        Logger.info('Build: Using WindowClass ' + str(self.winClass))
        self.widgetSizes = Defaults.WidgetDefaults(self.winClass)
        self.screenManager = MainScreenManager()
        self.mainLoop = Clock.schedule_once(self.initializeEmptyApp)
        self.pitches = Defaults.PitchesSharps()
        Logger.info('Build: App build successful: ')
        return self.screenManager

    def on_pause(self):
        self.get_running_app.stop()
        self.tracker.stats.print_summary()
        Logger.info('Runtime: Pausing application')

    def app_start(self):
        self.screenManager.ids['blah'].children[0].schedule()
        Logger.info('OOGABOOGAOOGABOOGA WHY DO I NEVER RUN???')

    def app_stop(self):
        if self.screenManager.current != 'defaultApplicationScreen':
            self.mainLoop.cancel()        
        Logger.info('Runtime: Stopping application')

if __name__=="__main__":
    MainApp().run()
