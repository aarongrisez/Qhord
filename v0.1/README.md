## Introducing Qhord

Qhord is a flexible and portable interface for musical improvisation that is governed by a quantum simulation. The simulation currently implements a 7-dimensional quantum simulation which partially collapses due to user input (or "measurements").

### Pitch Spectrum

The first parameter a user can play with is the spectrum of pitches. This is an abstract notion of importance for each pitch. The user assigns a weight to each pitch in the tonal space used (normalized, so this spectrum can be seen as a probability spectrum over the pitches). The program then extracts a representative (or "atomic) chord which contains the most prevalent intervals in the spectrum.

### Unitary Evolution

The system is subjected to unitary evolution through an oscillatory Hamiltonian. This Hamiltonian is determined by an "atomic" chord containing the most prevalent intervals in the user-provided spectrum.

## Installation

### Dependencies
This project currently uses Python3 with the following packages:
 - NumPy 1.11.1
 - Pandas 0.18.1
 - PyGame 1.9.2

It is important that the PyGame version installed is at least 1.9 as the midi module is used extensively.

### Tested Systems
This project has been tested successfully on a 

### Runtime
Once installation is complete, navigate to the directory containing qsys.py. Run the following command:

```
python -a 0 0 0 0 0 0 0 -b 0 0 0 0 0 0 0 -c 0 0 -d 0
```

## Moving Forward
This is a list of things I'd like to do still with the program:
- Clarify and formalize the relationship between game time and simulation time. Introductory research on the issue http://gafferongames.com/game-physics/fix-your-timestep/
- Allow for multiple voices (multiple quantum system objects) to interact, see if entanglement produces interesting results
- Allow for time-dependent Hamiltonians - Particularly, I'd like for oscillations between certain chords to be "turned on" or "turned off" at particular points. It would be interesting if this process could be automated, ie: the Hamiltonian switches to a new chord pair if the current state gets "close enough" to a particular configuration
- Re-implement code for pitches and spectra; create classes for pitch and spectra and overload methods to account for modularity in calculating distances
