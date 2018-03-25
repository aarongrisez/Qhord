from kivy.app import App
from kivy.base import ExceptionHandler
from kivy.base import ExceptionManager
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from src.screens import KeyboardScreen
from src.screens import TutorialScreen
#from src.screens import EmailScreen
from src import Defaults
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
import kivy.resources
import numpy as np
#import plyer

#Builder.load_file('SpectrumScreen.kv')
Builder.load_file('src/kv/HamiltonianScreen.kv')
Logger.info("Import Hamiltonian Screen")
Builder.load_file('src/kv/TutorialScreen.kv')
Logger.info("Import Tutorial Screen")
Builder.load_file('src/kv/WelcomeScreen.kv')
Logger.info("Import Welcome Screen")
Builder.load_file('src/kv/KeyboardScreen.kv')
Logger.info("Import Keyboard Screen")
Builder.load_file('src/kv/key.kv')
Logger.info("Import Key")
Builder.load_file('src/kv/tutorialkey.kv')
Logger.info("Import TutorialKey")
#Builder.load_file('src/kv/EmailScreen.kv')
#Logger.info("Import Email Screen")

class MainScreenManager(ScreenManager): 
    pass 

class WelcomeScreen(Screen): 
    pass 

class CreditsScreen(Screen):
    pass

class ChordToggleButton(ToggleButton):
    pass

class Root1ToggleButton(ToggleButton):
    pass

class Root2ToggleButton(ToggleButton):
    pass

class HamiltonianScreen(Screen):
    chord = StringProperty('1-5')
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


class MainApp(App):
    def initializeEmptyApp(self, *kwargs):
    	pass

    def build(self):
#        try:
        self.colorScheme = Defaults.ColorScheme()
        self.spectra = Defaults.Spectra()
        self.winSize = (float(Window.width), float(Window.height))
        self.winClass = Defaults.WinClass().getWinClass((float(Window.width), float(Window.height)))
        Logger.info('Build: Using WindowClass ' + str(self.winClass))
        self.widgetSizes = Defaults.WidgetDefaults(self.winClass)
        Logger.info('Widget Defaults Loaded')
        self.screenManager = MainScreenManager()
        Logger.info("Screen Manager Initialized")
        self.mainLoop = Clock.schedule_once(self.initializeEmptyApp)
        self.pitches = Defaults.PitchesSharps()
        Logger.info('Build: App build successful: ')
        return self.screenManager
#        except:
#            Logger.info('Something big messed up')

    def on_pause(self):
        self.get_running_app.stop()
        self.tracker.stats.print_summary()
        Logger.info('Runtime: Pausing application')

    def app_stop(self):
        if self.screenManager.current != 'keyboardScreen':
            self.mainLoop.cancel()        
        Logger.info('Runtime: Stopping application')

class E(ExceptionHandler):
    def handle_exception(self, inst):
        Logger.exception('Exception catched by ExceptionHandler')
        return ExceptionManager.PASS

if __name__=="__main__":
#    ExceptionManager.add_handler(E())
    MainApp().run()
