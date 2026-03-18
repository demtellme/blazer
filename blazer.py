import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Blazer")
clock = pygame.time.Clock()
running = True

FONT = pygame.font.SysFont("hack", 48)

DARKGREEN = (50, 100, 50)
GREEN = (0,255,0)
LIGHTGREEN = (150,255,150)

def square(x, y, width, height, colour, border_radius):
    pygame.draw.rect(screen, colour, (x, y, width, height), border_radius=border_radius)

def text(text,colour):
    return FONT.render(text, True, colour)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((23, 23, 23))

    screen.blit(text("Blazer", (255,100,50)), (50,25))

    square(50, 100, 20, 20, DARKGREEN, 5)
    square(80, 100, 20, 20, GREEN, 5)
    square(110, 100, 20, 20, LIGHTGREEN, 5)

    print(pygame.mouse.get_pos())
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
