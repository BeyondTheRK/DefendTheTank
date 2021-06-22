import pygame
import sys
import os

pygame.mixer.init()

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
"""
bullet_boop = resource_path("laser1.wav")
alien_boop = resource_path("explosion.wav")
back_boop = resource_path("background.mp3")
"""

bullet_sound = pygame.mixer.Sound("laser1.wav")
alien_sound = pygame.mixer.Sound("explosion.wav")
background_sound = pygame.mixer.Sound("background.wav")
