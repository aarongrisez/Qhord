#!usr/bin/env python2

import numpy as np
from . import setup

class Qsys(object):
    """
    Base Class for Quantum System simulation

    Constructor Parameters:
    -----------------------
    dim (int)
    initial_state (list)
    time_step (float)

    Attributes:
    -----------
        dim: integer
            dimension of the system
        current_state: list_like, (n,n)
            current wavefunction for the system
        current_probs: array_like, (1,n)
            current probabilities for the system
        time: float
            current time for system's evolution
        time_step: float
            time step used in propogation of system

    ATTRIBUTES SET BY SUBCLASS:
        hamiltonian: ufunc(self.time), returns (n,n) array
            function that returns matrix representation of hamiltonian operator
        trajectory: array_like, (n, self.time)
            history of the quantum system, has default max_size, dumps to npy
            file when max size is reached
        measurement_history: array_like, (measurement, outcome, self.time)
            contains tuples of what measurements occurred when and their
            outcomes

    Methods:
    --------
        normalize(self)
        schrodinger(self), returns array
    """
    def __init__(self, dim, initial_state, time_step, hamiltonian=None,
                 povms=None):
        self.dim = dim
        self.current_state = initial_state
        self.current_probs = self.probabilities()
        self.time = 0.
        self.time_step = time_step
        self.hamiltonian = hamiltonian
        self.povms = povms

    def normalize(self, state):
        """
        Takes current state and normalizes

        Parameters:
        -----------
            state: complex vector
                state to normalize
        """
        norm = np.linalg.norm(self.current_state)
        self.current_state = self.current_state / norm

    def schrodinger(self)
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
        return 1 / (1j) * np.dot(self.hamiltonian(t), self.current_state)

    def rk4_step(self):
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
        return probs

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
