import pygame
import pygame.gfxdraw
from random import randint

width = 800
height = 800
screen = pygame.display.set_mode([width, height])

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
ORANGE_RED = (255, 69, 0)
SNAKE_GREEN = (127, 255, 0)


def main():
    running = True
    screen = pygame.display.set_mode([width, height])
    screen.set_alpha(128)
    for i in range(100):
        pygame.gfxdraw.filled_polygon(screen,
                                      [(randint(1, width), randint(1, height)), (randint(1, width), randint(1, height)),
                                       (randint(1, width), randint(1, height))], rand_color())

    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


def rand_color():
    return randint(1, 255), randint(1, 255), randint(1, 255), 128


if __name__ == "__main__":
    main()
