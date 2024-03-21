import pygame as p

def load_sounds():

    sounds = {
        "move": p.mixer.Sound("assets/sounds/move.mp3"),
        "capture": p.mixer.Sound("assets/sounds/capture.mp3"),
        "check": p.mixer.Sound("assets/sounds/check.mp3"),
        "mate": p.mixer.Sound("assets/sounds/mat.mp3"),
    }
    return sounds