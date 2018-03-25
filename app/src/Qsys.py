#!usr/bin/env python2

import numpy as np
from . import setup

class Qsys:
    """
    Base Class for Quantum System simulation

    Constructor Parameters:
    -----------------------
    dim (int)
    psi_naught (list)
    delta_t (float)
    omega (float)

    Attributes:
    -----------
        dim: integer
            dimension of the system
        current_state: list_like
            current wavefunction for the system
        time: float
            current time for system's evolution
        spectrum: list_like ###STILL NEED TO REIMPLEMENT###
            relative weights for pitches
        chord1: list_like
            first chord in oscillation
        chord2: list_like
            second chord in oscillation
        omega: float
            frequency for oscillation
        hamiltonian: array_like
            matrix representation of hamiltonian operator; optional kwarg to override spectrum generation of hamiltonian
    """
    def __init__(self, argDim, argPsi_naught, argDelta_t, argOmega, argBareSpectrum, argStableSpectrum, argUnstableSpectrum, argRoot1, argRoot2, argHamiltonian = None):
        self.bareSpectrum = argBareSpectrum
        self.dim = argDim
        self.current_state = argPsi_naught
        self.current_probs = self.probabilities()
        self.time = 0.
        self.delta_t = argDelta_t
        self.spectrum = np.array(argStableSpectrum)
        self.unstable = np.array(argUnstableSpectrum)
        #Normalize spectrum if it isn't normalized
        self.spectrum = self.spectrum / np.sum(self.spectrum)
#        self.atom = setup.atom(self.spectrum)
        self.recombinedSpectrum = self.spectrum + self.unstable
        self.recombinedSpectrum = self.recombinedSpectrum / np.sum(self.recombinedSpectrum)
        self.omega = argOmega
        self.root1 = argRoot1
        self.root2 = argRoot2
        self.lastOutput = 0
        self.lastKey = 0
        self.conditionalProbs = setup.conditional_probs(self.recombinedSpectrum)
        self.POVMs = setup.POVMs(self.spectrum, self.conditionalProbs)
        if argHamiltonian == None:
            self.hamiltonian = setup.tune_H(self.root1, self.root2, self.bareSpectrum, self.omega)
        else:
            self.hamiltonian = argHamiltonian
        self.conditional_probabilities = setup.conditional_probs(self.spectrum)
        self.POVMs = setup.POVMs(self.spectrum, self.conditional_probabilities)

    def normalize(self, state):
        """
        Takes current state and normalizes

        Parameters:
        -----------
            state: complex vector
                state to normalize
        """
        norm = np.linalg.norm(state)
        return state / norm

    def schrodinger(self, psi, t):
        """
        Schrodinger Equation

        Parameters:
        -----------
            psi: vector
                initial wavefunction to evolve
            t: scalar, np.float
                time for evaluation

        Returns:
        --------
            vector
                differential time step for wavefunction evolution
        """
        return 1 / (1j) * np.dot(self.hamiltonian, psi)

    def rk4_step(self, u, t, du, delta_t):
        """
        Implementation of the Runge-Kutta 4th order approximation for solving a system of coupled ODEs

        Parameters:
        -----------
            u: array-like
                initial values
            delta_t: float
                time step size
            t: float
                current time
            du: lambda
                vector-valued function for differential equation
        Returns:
        --------
            tuple of floats
                vector of values for the function at the next time step
        """
        K1 = delta_t * du(u, t)
        K2 = delta_t * du(u + K1 / 2, t + delta_t / 2)
        K3 = delta_t * du(u + K2 / 2, t + delta_t / 2)
        K4 = delta_t * du(u + K3, t + delta_t)# 4 intermediate approximations
        return u + (K1 + 2 * K2 + 2 * K3 + K4) / 6

    def probabilities(self):
        """
        Returns mod^2 of the current state. This function normalizes probabilities
        """
        probs = np.absolute(self.current_state)
        norm = np.sum(probs) # Calculates the norm of the current wavefunction
        return probs / norm

    def get_probs(self):
        return self.current_probs

    def measure(self, key):
        """
        Measures current state and initiates collapse
        """
        #Randomly Sample to find "internal state"
        wf_probability = self.probabilities()
        internal_state = self.sample(wf_probability) #This is a hidden state--The User never sees or knows this
        conditional_probability = self.conditional_probabilities[key, internal_state, :]
        self.lastOutput = self.sample(conditional_probability)
        self.lastKey = key
        #Now, need to collapse state and output pitch
        self.collapse()
        return self.output()

    def collapse(self):
        POVM = self.POVMs[self.lastOutput][self.lastKey]        
        new_state = np.dot(np.sqrt(POVM), self.current_state) / np.dot(self.current_state, np.dot(POVM, self.current_state))
        self.current_state = new_state

    def sample(self, probabilities):
        """
        Randomly sample over a set of probabilities using a threshold calculation. Returns the location of the sampled state in ordered pitch space
        """
        thresholds = np.array([np.sum(probabilities[:i]) for i in range(1, self.dim+1)])
        r = np.random.rand()
        max_threshold = thresholds[thresholds > r][0]
        thresholds = list(thresholds)
        loc = thresholds.index(max_threshold)
        return loc

    def output(self):
        """
        Triggers output for the given output pitch
        """
        return (self.lastKey, self.lastOutput)

    def run(self):
        new_state = self.rk4_step(self.current_state, self.time, self.schrodinger, self.delta_t)
        self.current_state = self.normalize(new_state)
        self.time += self.delta_t
        self.current_probs = self.probabilities()
