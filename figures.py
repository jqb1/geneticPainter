import argparse
import os

import pygame
import pygame.gfxdraw

from shape import Shape


class Painting:
    def __init__(self, shapes_number: int, width: int, height: int):
        self.shapes_number = shapes_number
        self.width = width
        self.height = height

    def draw(self):
        surface = pygame.Surface((self.width, self.height))
        for i in range(self.shapes_number):
            shape = Shape(self.width, self.height)
            shape.set_init_vertices()
            pygame.gfxdraw.filled_polygon(surface, shape.vertices, shape.color)

        return surface


def main():
    image = read_image()

    width, height = image.get_width(), image.get_height()
    screen = pygame.display.set_mode([width, height])
    print(pygame.display.get_surface().get_view())

    surface = Painting(200, width, height).draw()
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


def fitness():
    pass


def read_image():
    def file_type(file_path):
        if not os.path.exists(file_path):
            raise argparse.ArgumentTypeError('File does not exist')
        return file_path

    parser = argparse.ArgumentParser('Process image')
    parser.add_argument('-f', dest="file_path", required=True, type=file_type,
                        help="input image file path")

    image_path = parser.parse_args().file_path
    img = pygame.image.load(image_path)
    return img


if __name__ == "__main__":
    main()
