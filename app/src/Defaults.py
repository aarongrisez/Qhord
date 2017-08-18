class WinClass():
    """
    Contains information about the window size/aspect ratio, etc
    """
    def getWinClass(self,size):
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
 
