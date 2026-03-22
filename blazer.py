import pygame
import os
import json
import calendar
import datetime
import tkinter as tk
from tkinter import filedialog

CONF = os.path.join(os.path.dirname(__file__), 'config.json')

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
BGSECONDAY = BGCOLOURS[1]


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

    for day in range(days):
        row = day // squaresperrow
        col = day % squaresperrow
        x = startx + col * step
        y = starty + row * step
        square(x, y, 40, 40, DARKEST, 5)

def main():
    filepath = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    filepath = filedialog.askopenfilename(
                        parent=tkroot,
                        title="Open File",
                        initialdir=os.path.expanduser("~")
                    )
                    print(filepath)

        screen.fill(BGPRIMARY)
        screen.blit(text(BIGFONT, "Blazer", MID), (50, 20))

        square(50, 100, 20, 20, DARKEST, 5)
        square(80, 100, 20, 20, DARK, 5)
        square(110, 100, 20, 20, MID, 5)
        square(140, 100, 20, 20, LIGHT, 5)
        square(170, 100, 20, 20, LIGHTEST, 5)

        screen.blit(text(SMALLFONT, year, MID), (500,30))
        screen.blit(text(SMALLFONT, month, MID), (500,55))

        square(WIDTH*0.1,HEIGHT*0.2, WIDTH * 0.8, HEIGHT*0.6, BGSECONDAY, 5)

        displaypastdays(daysincurrentmonth)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
