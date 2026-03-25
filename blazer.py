import pygame
import os
import json
import calendar
import datetime
import tkinter as tk
from tkinter import filedialog

CONF = os.path.join(os.path.dirname(__file__), 'config.json')
CCOMMITS = os.path.join(os.path.dirname(__file__), '.commits.txt')

HEIGHT = 640
WIDTH = 640

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blazer")
clock = pygame.time.Clock()

with open(CONF, "r") as f:
    config = json.load(f)

userconfig = config['USER']

COLOURS = tuple(config['colourschemes'][userconfig['colourscheme']])

LIGHTEST = COLOURS[4]
LIGHT = COLOURS[3]
MID = COLOURS[2]
DARK = COLOURS[1]
DARKEST = COLOURS[0]

BGCOLOURS = tuple(config['background'][userconfig['background']])
BGPRIMARY = BGCOLOURS[0]
BGSECONDARY = BGCOLOURS[1]


SMALLFONT = pygame.font.SysFont(config['font'][userconfig['font']], userconfig['fontsize'] - 20)
FONT = pygame.font.SysFont(config['font'][userconfig['font']], userconfig['fontsize'])
BIGFONT = pygame.font.SysFont(config['font'][userconfig['font']], userconfig['fontsize'] + 20)


timeframeinmonths = 1

date = str(datetime.date.today()).split("-")
year = date[0]
month = date[1]
day = date[2]

daysincurrentmonth = int(calendar.monthrange(int(year),int(month))[1])


tkroot = tk.Tk()
tkroot.withdraw()

def square(x, y, width, height, colour, border_radius):
    pygame.draw.rect(screen, colour, (x, y, width, height), border_radius=border_radius)

def text(font, text, colour):
    return font.render(text, True, colour)

def displaypastdays(days):
    gap = 10
    step = 40 + gap
    startx = WIDTH * 0.12
    starty = HEIGHT * 0.3
    squaresperrow = int((WIDTH * 0.8) // step)

    for i in range(days):
        row = i // squaresperrow
        col = i % squaresperrow
        x = startx + col * step
        y = starty + row * step
        square(x, y, 40, 40, DARKEST, 5)


def loadcommits():
    commits = open(CONF, 'r').readlines()

def makenewcommit():
    filepath = filedialog.askopenfilename(
        parent=tkroot,
        title="Open File",
        initialdir=os.path.expanduser("~")
    )
    return filepath


def dipslayhomescreen():
    screen.blit(text(BIGFONT, "Blazer", MID), (50, 20))
    square(50, 100, 20, 20, DARKEST, 5)
    square(80, 100, 20, 20, DARK, 5)
    square(110, 100, 20, 20, MID, 5)
    square(140, 100, 20, 20, LIGHT, 5)
    square(170, 100, 20, 20, LIGHTEST, 5)

    screen.blit(text(SMALLFONT, year, MID), (500,30))
    screen.blit(text(SMALLFONT, f"{day}-{month}", MID), (500,55))

    square(WIDTH*0.1,HEIGHT*0.2, WIDTH * 0.8, HEIGHT*0.6, BGSECONDARY, 5)

    square(50,550,200,50,DARK,5)
    screen.blit(text(SMALLFONT, "Add new commit", MID), (54, 560))

    displaypastdays(daysincurrentmonth)

def displaycommitscreen():
    square(40, 30, 200, 40, BGSECONDARY, 5)
    square(40, 90, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Message:", MID), (50, 27))

    square(40, 230, 175, 40, BGSECONDARY, 5)
    square(40, 290, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Files:", MID), (50, 228))

    square(232, 500, 175, 45, DARK, 5)
    screen.blit(text(FONT, "COMMIT", MID), (240, 500))



def main():
    running = True
    state = 'home'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == 'home' and pygame.Rect(50, 550, 200, 50).collidepoint(event.pos):
                    state = 'commitscreen'

        screen.fill(BGPRIMARY)

        if state == 'home':
            dipslayhomescreen()
        elif state == 'commitscreen':
            displaycommitscreen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
