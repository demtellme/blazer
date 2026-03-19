import pygame
import os
import json

BASEDIR =  os.path.dirname(__file__)
CONF = os.path.join(BASEDIR, 'config.json')


pygame.init()

screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Blazer")
clock = pygame.time.Clock()

with open(CONF, "r") as f:
    config = json.load(f)

user = config['USER']

COLOURS = tuple(config['colourschemes'][user['colourscheme']])
LIGHT = COLOURS[2]
MID = COLOURS[1]
DARK = COLOURS[0]

BG = tuple(config['background'][user['background']])
FONT = pygame.font.SysFont(config['font'][user['font']], user['fontsize'])



def square(x, y, width, height, colour, border_radius):
    pygame.draw.rect(screen, colour, (x, y, width, height), border_radius=border_radius)

def text(font,text,colour):
    return font.render(text, True, colour)




# def configureconfig():
#     pass
def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG)

        screen.blit(text(FONT, "Blazer", DARK), (50,25))

        square(50, 100, 20, 20, DARK, 5)
        square(80, 100, 20, 20, MID, 5)
        square(110, 100, 20, 20, LIGHT, 5)



        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
