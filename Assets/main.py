'''
This is The Quest game
for the final project of
Bootcamp Zero of KeepCoding.
'''


import pygame
import sys
from Scripts.controller import Controller


if __name__ == '__main__':
    run = Controller()
    run.launch_manager()
    pygame.quit()
    sys.exit()
