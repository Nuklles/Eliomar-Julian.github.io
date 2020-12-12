# necessario a biblioteca pygame (pip install pygame)
import pygame
import os

pygame.init()
pygame.mixer_music.load(
    './audio/tribodaperiferia-conspiracao-ft-marilia-mendonca-01356338.mp3'
)
pygame.mixer_music.play(1, 0.0)
os.system("pause")

