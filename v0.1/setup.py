#!usr/bin/env python3

import numpy as np
import pandas as pd
import operator as op
import itertools as it
import copy

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
    n = len(spectrum)
    conditional_probs = np.zeros((n,n,n))
    for r in range(n):
        pair = pairs(spectrum)
        for k, s in pair:
            if k == s:
                if r == k:
                    conditional_probs[k, s, r] = 1
            else:
                conditional_probs[k, s, r] = np.exp(-(dist(spectrum, r, s)) ** 2 / (2 * dist(spectrum, s, k)))
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
    chord1 = np.zeros(n)
    chord2 = np.zeros(n)
    for i in enumerate(atom):
        chord1[(i[0] + root_1) % n] = i[1]
        chord2[(i[0] + root_2) % n] = i[1]
    H = freq / 2 * (np.outer(chord1, chord2) + np.outer(chord2, chord1))
    return H

def atom(spectrum):
    """
    Defines atomic chord structure as default structrue from spectrum -- need to address the case where spectrum values are equal

    Parameters:
    -----------
        spectrum: list
            user-defined spectrum

    Returns:
    --------
        np.array
            atomic structure for chord
    """
    n = len(spectrum)
    members = []
    total_weight = 0
    u_spectrum = copy.deepcopy(spectrum)
    spectrum.sort(reverse=True)
    for i in spectrum:
        if total_weight < .7:
            members.append([u_spectrum.index(i), i])
        total_weight += i
    positions = []
    norm = 0
    for i in members[:]:
        positions.append(i[0])
        norm += i[1]
    if min(positions) != 0:
        positions = [i - min(positions) for i in positions]
    abstracted = np.zeros(n)
    for i in enumerate(members):
        abstracted[positions[i[0]]] =  i[1][1] / norm
    return abstracted

def normalize_row(conditional_probs, row_idx):
    """
    Normalizes rows in the conditional probabilities (Do I still need this? I think it's embedded in the conditional_probs itself)
    """
    weights = []
    for i in row_idx:
        weights.append(conditional_probs[i])
    total_weight = sum(weights)
    for i in row_idx:
        conditional_probs[i] = conditional_probs[i] / total_weight
    return conditional_probs

def POVM_key(spectrum, r, key, conditional_probs):
    """
    Creates un-normalized POVM matrix for a given readout

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
    probs = conditional_probs[key, :, r]
    POVM = np.identity(n) * probs
    return POVM

def POVM_normalize(spectrum, conditional_probs, pairs):
    """
    Returns all normalized POVMs

    Parameters:
    -----------
        spectrum: list
            user-defined spectrum
        conditional_probs: np.array(shape=(n,n,n))
            conditional probabilities
        pairs: list
            list of all possible permutation pairs from spectrum

    Returns:
    --------
        POVMs: np.array
            POVMs for any given readout
    """
    n = len(spectrum)
    POVMs = np.zeros((n, n, n))
    for i in range(n):
        for j in range(n):
            POVMs[i] = POVM_key(spectrum, i, j, conditional_probs)
    for i in range(n):
        weight = sum(sum(POVMs[:,:,i]))
        POVMs[:,:,i] = POVMs[:,:,i] / weight
    return POVMs

##### TESTS

def test_pairs():
    test = list(pairs([0.7,0.3]))
    case = [(0,1), (1,0)]
    print(test, case)
    assert test == case

def test_max_distance():
    spectrum = [0.7, 0.3]
    test = max_distance(spectrum, pairs(spectrum))
    case = .4
    print(test, case)
    assert np.allclose(test, case)

def test_dist():
    spectrum = [0.7, 0.3]
    max_dist= max_distance(spectrum, pairs(spectrum))
    test = dist(spectrum, 0, 1, max_dist)
    case = 1.0
    print(test, case)
    assert np.allclose(test,case)

def test_conditional_probability(): #This is a placeholder test, probabilities are currently randomized
    spectrum = [0.7, 0.3]
    max_dist= max_distance(spectrum, pairs(spectrum))
    print(conditional_probs(spectrum))
    assert True

def test_POVM_key():#Need to finish this test, for now it is okay
    spectrum = [.4,.1,.3,.2]
    test = POVM_key(spectrum, 0, 0, conditional_probs(spectrum))
    print(test)
    assert True

def test_POVM_normalize():
    spectrum = [.4,.1,.3,.2]
    test = POVM_normalize(spectrum, conditional_probs(spectrum), pairs(spectrum))
    print(test)
    print(test[:,0,:])
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
