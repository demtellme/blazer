import pygame
import os
import json
import calendar
import datetime
import tkinter as tk
from tkinter import filedialog

CONF = os.path.join(os.path.dirname(__file__), 'config.json')
COMMITSFOLDER = os.path.join(os.path.dirname(__file__), '.commits')
COMMITSJSON = os.path.join(os.path.dirname(__file__), '.commits.json')

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

class Commit:
    def __init__(self, message, files, timestamp, directory):
        self.message = message
        self.files = files
        self.timestamp = timestamp
        self.directory = directory

    def makedictionary(self):
        return {
            'message': self.message,
            'files': self.files,
            'timestamp': self.timestamp
        }

    def savecommit(self):
        with open(COMMITSJSON, 'r') as f:
                    commits = json.load(f)
        commits.append(self.makedictionary())
        with open(COMMITSJSON, 'w') as f:
            json.dump(commits, f, indent=2)

def setup():
    if not os.path.exists(COMMITSJSON):
        with open(COMMITSJSON, 'w') as f:
            json.dump([], f)
    if not os.path.exists(COMMITSFOLDER):
        os.mkdir(COMMITSFOLDER)

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
    with open(COMMITSJSON) as f:
        pass

def addfile():
    filepath = filedialog.askopenfilename(
        parent=tkroot,
        title="Open File",
        initialdir=os.path.expanduser("~")
    )
    return filepath


def dipslayhomescreen():
    screen.blit(text(BIGFONT, "Blazer", MID), (50, 20))
    square(50, 90, 20, 20, DARKEST, 5)
    square(80, 90, 20, 20, DARK, 5)
    square(110, 90, 20, 20, MID, 5)
    square(140, 90, 20, 20, LIGHT, 5)
    square(170, 90, 20, 20, LIGHTEST, 5)

    screen.blit(text(SMALLFONT, year, MID), (500,30))
    screen.blit(text(SMALLFONT, f"{day}-{month}", MID), (500,55))

    square(WIDTH*0.1,HEIGHT*0.2, WIDTH * 0.8, HEIGHT*0.6, BGSECONDARY, 5)

    square(50,550,200,50,DARK,5)
    screen.blit(text(SMALLFONT, "Add new commit", MID), (54, 560))

    displaypastdays(daysincurrentmonth)

def displaycommitscreen(files):
    square(40, 30, 200, 40, BGSECONDARY, 5)
    square(40, 90, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Message:", MID), (50, 27))

    square(40, 230, 175, 40, BGSECONDARY, 5)
    square(40, 290, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Files:", MID), (50, 228))

    square(232, 500, 175, 45, DARK, 5)
    screen.blit(text(FONT, "COMMIT", MID), (240, 500))

    if len(files) > 0:
        for file in files:
            index = files.index(file)
            ycord = 300 + index * 20
            screen.blit(text(SMALLFONT, file, MID), (50,ycord))


def main():
    setup()
    running = True
    state = 'home'
    files = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == 'home':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(50, 550, 200, 50).collidepoint(event.pos):
                        state = 'commitscreen'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    state='commitscreen'

            if state == 'commitscreen':
                if event.type == pygame.DROPFILE:
                    files.append(addfile())

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(232,500,175,45).collidepoint(event.pos):
                        print('commited')
                        state = 'home'
                        files = []
                    elif pygame.Rect(40, 290, 560, 120).collidepoint(event.pos):
                        files.append(addfile())
                    elif pygame.Rect(40, 90, 560, 120).collidepoint(event.pos):
                        pass

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        files.append(addfile())

                    if event.key == pygame.K_j:
                        pass

        screen.fill(BGPRIMARY)

        if state == 'home':
            dipslayhomescreen()
        elif state == 'commitscreen':
            displaycommitscreen(files)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
