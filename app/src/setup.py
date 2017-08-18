#!usr/bin/env python3

import numpy as np
import itertools as it
from operator import itemgetter

def pairs(spectrum):
    """
    Returns a list of all index pairs in spectrum including any repeats

    Parameters:
    -----------
        spectrum: list
            user-defined spectrum
    """
    n = len(spectrum)
    return it.product(range(n), repeat=2)

def dist(spectrum, A, B):
    """
    Minimum number of steps along ring to get from one pitch to the next

    Parameters:
    -----------
        spectrum: list
            user-defined spectrum
        A: int
            first pitch
        B: int
            second pitch
    """
    length = len(spectrum)
    forward = abs(B - A) # Forward moving graph distance between pitches
    backward = abs(forward - length) # Backward moving distance... ...
    if forward <= backward:
        n = forward
    else:
        n = backward
    return n

def ordering(spectrum):
    """
    Takes input spectrum and re-orders it so that the most probable elements occur in the middle
    """
    holder = []
    keySpectrum = sorted(enumerate(spectrum), key = itemgetter(1))
    for i in range(len(keySpectrum)):
        if i%2 == 0:
            holder.insert(0, keySpectrum[-(i+1)])
        else:
            holder.append(keySpectrum[-(i+1)])
    translationList = [i[0] for i in holder]
    sortedSpectrum = [i[1] for i in holder]
    return (translationList, sortedSpectrum)

def conditional_probs(spectrum):
    """
    Defines array of conditional probabilities

    Parameters:
    -----------
        spectrum: list
            user-defined spectrum
    Returns:
    --------
        conditional_probs: np.array(shape=(n, n, n))
            first dimension - key pressed, second dimension - internal state, third dimension - output
            ie: indexing is by (k, s, r) or (MIDI input, internal state, output)
    """
    re_ordered_spectrum = ordering(spectrum)
    spectrum = re_ordered_spectrum[1]
    translationList = re_ordered_spectrum[0]
    n = len(spectrum)
    conditional_probs = np.zeros((n,n,n))
    for r in range(n):
        pair = pairs(spectrum)
        for k, s in pair:
            r = translationList[r]
            s = translationList[s]
            k = translationList[k]
            if k == s:
                if r == k:
                    conditional_probs[k, s, r] = 1
            else:
                conditional_probs[k, s, r] = np.exp(-(dist(spectrum, r, s)) ** 2 / (0.1 * dist(spectrum, s, k)))
    for i in range(n):
        for j in range(n):
            norm = sum(conditional_probs[i, j, :])
            conditional_probs[i, j, :] = conditional_probs[i, j, :] / norm
    return conditional_probs

def tune_H(root_1, root_2, atom, freq):
    """
    Returns time dependent weighted hamiltonian between two chords

    Parameters:
    -----------
        root_1: int
            root of the first chord
        root_2: int
            root of the second chord
        atom: np.array
            atomic structure for chord
        freq: float
            frequency at which hamiltonian is to be oscillating

    Returns:
    --------
        H: np.array
            hamiltonian between the two chords defined
    """
    n = len(atom)
    chord1 = np.zeros(n) #This will serve as a "Tonic" Chord in an Authentic/Half cadence
    chord2 = np.zeros(n) #This will serve as a "Dominant" Chord in an Authentic/Half cadence
    for i in enumerate(atom):
        chord1[(i[0] + root_1) % n] = i[1] #Transpose atom to root of Chord1
        chord2[(i[0] + root_2) % n] = i[1] #Transpose atom to root of Chord2
    H = freq / 2 * (np.outer(chord1, chord2) + np.outer(chord2, chord1))
    return H

def atom(spectrum, argThreshold = 0.8):
    """
    Extract an abstracted atomic structure chord from the given spectrum. This is just one of several possible extractions that could be musically sensible. This function can be broken if given input like this: np.array([.15,.5,.15,.2]) with threshold .8. Here the algorithm will correctly select the 1st and 3rd elements (zero indexed). Then it will admit the 0th element and terminate. However, this is somewhat erroneous as the 2nd element has the same value as the 0th. The atomic structure the algorithm gives, however, implies that somehow the 0th element is more important. What I propose to fix this is an adaptive approach to setting the threshold. That is, include some way for the algorithm to detect if it stops on an element with multiplicity != 1, and then adjust the given threshold either up or down (whichever is appropriate) to extract the atomic structure.
    """
    spectrum = np.array(spectrum) #Sanitize input so that it is a numpy array
    threshold = argThreshold #Set cutoff threshold for total weight to include from the spectrum
    total_weight = 0
    if np.sum(spectrum) != 1.0: #Check to see that spectrum is normalized, normalize if not
        spectrum = spectrum / np.sum(spectrum)
    for i in range(1, spectrum.size):
        if total_weight < threshold: #Check that the total weight of selected indeces is less than the threshold
            ind = np.argpartition(spectrum, -i)[-i:] #Select the indeces of i largest values in spectrum
            total_weight = np.sum(spectrum[ind]) #Find the sum of all elements in spectrum that were selected
        else:
            break
    atom = np.zeros(spectrum.size)
    atom[ind] += spectrum[ind]
    return atom / np.sum(atom)

def POVM_key(spectrum, r, key, conditional_probs):
    """
    Creates POVM matrix for a given readout

    Parameters:
    -----------
        spectrum: list
            user-defined spectrum
        r: np.int
            readout of measurement
        key: np.int
            input MIDI key
        conditional_probs: np.array
            conditional probabilities from spectrum

    Returns:
    --------
        np.array
            POVM matrix
    """
    n = len(spectrum)
    probs = np.zeros(n)
    for i in range(n):
        probs[i] = conditional_probs[key, i, r] #THIS IS A VERY SKETCHY STEP! I think it's ok, since k and s are independent params and switching the ordering of them should make no difference, but I should check to make sure this is okay
    POVM = np.identity(n) * probs #There should be an easier/more efficient way of doing this
    return POVM

def POVMs(spectrum, conditional_probs):
    n = len(spectrum)
    POVMs = np.zeros((n,n,n,n))
    for output in range(n):
        for key in range(n):
            POVMs[output][key] = POVM_key(spectrum, output, key, conditional_probs)
    return POVMs

##### TESTS

def test_pairs():
    test = list(pairs([0.7,0.3]))
    case = [(0,0), (0,1), (1,0), (1,1)]
    print(test, case)
    assert test == case

def test_dist():
    spectrum = [0.7, 0.3]
    test = dist(spectrum, 0, 1)
    case = 1.0
    print(test, case)
    assert np.allclose(test,case)

def test_atom():
    test = atom(np.array([.1,.3,.2,.15,.05,.2]))
    case = np.array([0,0.35294118, 0.23529412, 0.17647059, 0, 0.23529412])
    #print(test, case)
    assert np.allclose(test, case)

def test_conditional_probability():
    spectrum = [0.7, 0.3]
    test = conditional_probs(spectrum)
    case = np.array([[np.array([1,0]),np.array([0.26894142,0.73105858])],[np.array([0.73105858,0.26894142]), np.array([0,1])]])
    print(test, case)
    assert np.allclose(test[0], case[0]) and np.allclose(test[1], case[1])

def test_POVM_key():#Need to finish this test, for now it is okay
    spectrum = [.4,.1,.3,.2]
    conditional_probabilities = conditional_probs(spectrum)
    test = POVM_key(spectrum, 0, 0, conditional_probabilities)
    case = np.array([[1,0,0,0],[0,0.53444665,0,0],[0,0,0.47536689,0],[0,0,0,0.53444665]])
    assert np.allclose(test, case)

def test_POVMs():
    spectrum = [.4,.1,.3,.2]
    conditional_probabilities = conditional_probs(spectrum)
    test = POVMs(spectrum, conditional_probabilities)
    print(test)
    assert False

def test_atom():
    test = atom([.5, 0, .01, .1, .2])
    case = np.array([0.714285, 0, 0, 0, 0.285714])
    print(test, case)
    assert np.allclose(test,case)

def test_H():#This test works
    test = tune_H(3, 4, [0.5,0,0.3,0,0.2,0,0], 4)
    print(test)
    assert True

def main():
    pass

if __name__ == "__main__":
    main()
