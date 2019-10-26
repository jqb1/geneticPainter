import pygame
import pygame.gfxdraw

from shape import Shape

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])


class Painting:
    def __init__(self, shapes_number: int):
        self.shapes_number = shapes_number

    def draw(self):
        for i in range(self.shapes_number):
            shape = Shape(WIDTH, HEIGHT)
            shape.set_init_vertices()
            pygame.gfxdraw.filled_polygon(screen, shape.vertices, shape.color)


def main():
    running = True
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    print(pygame.display.get_surface().get_view())

    Painting(200).draw()
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


if __name__ == "__main__":
    main()
