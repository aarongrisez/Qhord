#!/usr/bin/env python3

import numpy as np
import pandas as pd
import sys
import setup
import pygame
from pygame import midi

class system():

    ##### CONSTRUCTORS
    def __init__(self, state, spectrum, roots, freq, delta_t = 0.001, voice = 0):
        self.spectrum = spectrum
        self.n = len(self.spectrum)
        self.pairs = setup.pairs(self.spectrum)
        self.conditional_probs = setup.conditional_probs(self.spectrum)
        self.POVMs = setup.POVM_normalize(self.spectrum, self.conditional_probs, self.pairs)
        self.atom = setup.atom(spectrum)
        self.initial_state = state
        self.current_state = self.initial_state
        self.frequency = freq
        self.hamiltonian = setup.tune_H(roots[0], roots[1], self.atom, self.frequency)
        self.voice = voice
        self.time = 0
        self.delta_t = delta_t
        self.MIDI_notes = [60, 62, 64, 65, 67, 69, 71]

    ##### CLASS METHODS
    def clock():
        """
        Clock for continuous time transformation
        """
        #return ping every time step to trigger runtime_loop, needs to be class method for synchronization between all instances?
        pass


    ##### METHODS
    def rk4_step(self, u, t, du, delta_t):
        """
        Implementation of the Runge-Kutta 4th order approximation for solving a system of coupled ODEs

        Parameters:
        -----------
            u: array-like
                vector of initial conditions
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

    def schrodinger(self, psi, t):
        """
        Schrodinger Equation

        Parameters:
        -----------
            psi: vector
                initial wavefunction to evolve
            t: scalar, np.float
                time for evaluation
            H: np.array
                hamiltonian for evolution

        Returns:
        --------
            vector
                differential evolution step for wavefunction
        """
        return 1 / (1j) * np.dot(self.hamiltonian, psi)

    def propogator(self, t):
        return np.exp(-1j * t * self.hamiltonian)

    def MIDI_listener():
        """
        Detects MIDI input
        """
        pass

    def write_record():
        """
        Records 4 melodies to file
        """
        # Record Random Sample
        # Record User Choice
        # Record Most Likely
        # Record Average
        pass

    def update_state(self):
        """
        Updates state with a single rk4 step
        """
        self.current_state = rk4_step(self.current_state, self.time, self.schrodinger(), self.delta_t)

    def probabilities(self):
        """
        Returns mod^2 of current state
        """
        probs = np.absolute(self.current_state)
        norm = sum(probs)
        return probs / norm

    def norm(self, state):
        """
        Returns mod^2 of any given state
        """
        return np.absolute(state)

    def collapse(self, key):
        """
        Collapses current state and initiates creation of a new object
        """
        #Randomly Sample to find "internal state"
        probs_wf = self.probabilities()
        thresholds = np.array([sum(probs_wf[:i]) for i in range(1, self.n+1)])
        r1 = np.random.rand()
        max_threshold = thresholds[thresholds > r1][0]
        thresholds = list(thresholds)
        loc = thresholds.index(max_threshold)
        #Randomly Sample to find Output given internal state
        r2 = np.random.rand()
        flattened = []
        probs = self.conditional_probs[key, loc, :]
        thresholds = np.array([sum(probs[:i]) for i in range(1, self.n+1)])
        max_threshold = thresholds[thresholds > r2][0]
        thresholds = list(thresholds)
        output = thresholds.index(max_threshold)
        self.output(output)
        #Need to get POVM based on readout, not on key pressed
        POVM = self.POVMs[key, :, :]
        print(POVM)
        expectation = sum(np.dot(probs_wf, POVM))
        new_state_un_normalized = np.dot(self.current_state,np.sqrt(POVM)) / np.sqrt(expectation)
        norm = sum(self.norm(new_state_un_normalized))
        new_state = new_state_un_normalized / norm
        return (new_state, output)

    def output(self, output):
        """
        Outputs selected MIDI pitch
        """
        pass

def main(spectrum, initial_condition, roots, freq, MIDI=True):
    """
    Main Function

    Parameters:
    -----------
        spectrum: list
            user-defined spectrum
        initial_condition: list
            initial state for the system
        roots: tuple
            pair of roots for Hamiltonian oscillations
        freq: float
            frequency of oscillation for Hamiltonian
    """
    pygame.init()
    pygame.font.init()
    pygame.midi.init()
    player = pygame.midi.Output(4)
    MIDI_in = pygame.midi.Input(3)
    screen_height = 500
    screen_width = 800
    font = pygame.font.SysFont("Comic Sans MS", 30)
    screen = pygame.display.set_mode((screen_width,screen_height), 0, 32)
    screen.fill((255,255,255))
    pygame.display.update()
    qsystem = system(initial_condition, spectrum, roots, freq)
    c_surf = pygame.image.load('./img/c_green.png')
    d_surf = pygame.image.load('./img/d_green.png')
    e_surf = pygame.image.load('./img/e_green.png')
    f_surf = pygame.image.load('./img/f_green.png')
    g_surf = pygame.image.load('./img/g_green.png')
    a_surf = pygame.image.load('./img/a_green.png')
    b_surf = pygame.image.load('./img/b_green.png')
    text1 = font.render("No Collapse yet", False, (0,0,0))
    text2 = font.render("No Keys pressed yet", False, (0,0,0))
    t = 0
    pitches_on = {}
    clock = pygame.time.Clock()
    times = []
    while True:
        times.append(clock.get_time())
        screen.fill((255,255,255))
        ev = pygame.event.poll()
        if MIDI_in.poll():
            notes = MIDI_in.read(100)
            MIDI_1 = notes[0]
            vel = MIDI_1[0][2]
            key = MIDI_1[0][1]
            if MIDI_1[0][0] == 144:
                msg_1 = "Current State is " + str(qsystem.current_state)
                logging.info(msg_1)
                collapse = qsystem.collapse(qsystem.MIDI_notes.index(key))
                new_state = collapse[0]
                output = collapse[1]
                MIDI_pitch = qsystem.MIDI_notes[output]
                msg_2 = "Output is " + str(output)
                msg_3 = "New state is " + str(new_state)
                logging.info(msg_2)
                logging.info(msg_3)
                text1 = font.render('Output was ' + str(output), False, (0,0,0))
                text2 = font.render('Key pressed ' + str(key), False, (0,0,0))
                player.note_on(MIDI_pitch, vel, 1)
                counter = 0
                qsystem = system(new_state, spectrum, (0, 3), 100)
                pitches_on[key] = MIDI_pitch
            else:
                MIDI_pitch = pitches_on[key]
                player.note_off(MIDI_pitch, vel, 1)
        state = qsystem.current_state
        #Implementation of rk4 step in schrodinger equation
        qsystem.current_state = qsystem.rk4_step(state, t, qsystem.schrodinger, qsystem.delta_t)
        #Implementation of propogator applied to state - This doesn't work
        #qsystem.set_current_state(np.dot(qsystem.propogator(t), state))
        t += qsystem.delta_t
        heights = qsystem.probabilities() * 300
        screen.blit(c_surf,(30,400 - heights[0]))
        screen.blit(d_surf,(90,400 - heights[1]))
        screen.blit(e_surf,(150,400 - heights[2]))
        screen.blit(f_surf,(210,400 - heights[3]))
        screen.blit(g_surf,(270,400 - heights[4]))
        screen.blit(a_surf,(330,400 - heights[5]))
        screen.blit(b_surf,(400,400 - heights[6]))
        screen.blit(text1, (470, 200))
        screen.blit(text2, (470, 300))
        pygame.display.update()
        if ev.type == pygame.QUIT:
            logging.info(times)
            MIDI_in.close()
            player.close()
            pygame.quit()
            sys.exit()
        clock.tick()

#####TESTS

def test_collapse():
    pass

#####EXCEPTIONS

class Error(Exception):
    """
    Base Class for exceptions
    """
    pass

class InputError(Error):
    pass

#####COMMAND LINE

if __name__ == "__main__":
    import sys
    import logging
    import argparse
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--spectrum', nargs='+', help="List type, List of relative weights for each pitch to use, must have dimensionality n (7 for v0.1)", type=float)
    parser.add_argument('-b', '--initial_condition', nargs='+', help="List type, Initial state of the system, must have dimensionality n (7 for v0.1)", type=float)
    parser.add_argument('-c', '--roots', nargs='+', help="List type, Roots of the chords for oscillation", type=int)
    parser.add_argument('-d', '--freq', help="Float type, Frequency of oscillation for the Hamiltonian", type=float)
    try:
        args = vars(parser.parse_args())
        spectrum = np.array(args['spectrum'])
        norm = np.sum(spectrum)
        spectrum = spectrum / norm
        initial_condition = np.array(args['initial_condition'])
        norm = np.sum(initial_condition)
        initial_condition = initial_condition / norm
        roots = args['roots']
        freq = args['freq']
    except (ValueError, TypeError):
        print("Invalid Input")
        sys.exit()
    main(list(spectrum), list(initial_condition), roots, freq)
