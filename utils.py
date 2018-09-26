import os
from pathlib import Path

import numpy as np


def saveNames(csvPath, names):
    createCsv(csvPath)
    saved_names = np.array(names)
    np.savetxt(csvPath, saved_names, delimiter=",", fmt="%s")


def loadNames(csvPath):
    if not os.path.exists(csvPath):
        return []
    names = np.genfromtxt(csvPath, delimiter=",", dtype=str).tolist()
    if type(names) == str:
        names = [names]
    return names


def saveEncodings(csvPath, encodings):
    createCsv(csvPath)
    saved_encodings = np.array(list(encodings))
    np.savetxt(csvPath, saved_encodings, delimiter=",")


def loadEncodings(csvPath):
    if not os.path.exists(csvPath):
        return []
    enc = np.loadtxt(csvPath, delimiter=",")
    if type(enc) == str:
        enc = [enc]
    return enc


def createCsv(csvPath):
    if not os.path.exists(csvPath):
        Path(csvPath).touch()
