import argparse
import os

import pygame
import pygame.gfxdraw

from shape import Shape
import numpy as np
import cv2
import PIL


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

    height, width = image.shape[:2]
    screen = pygame.display.set_mode([width, height])

    surface = Painting(200, width, height).draw()
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    fitness(image, surface)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


def fitness(image, surface):
    surface_array = pygame.surfarray.array3d(surface).transpose([1, 0, 2])
    surface_img = cv2.cvtColor(surface_array, cv2.COLOR_RGB2BGR)
    img_diff = cv2.subtract(image, surface_img)
    b, g, r = cv2.split(img_diff)
    return np.sum([b, g, r])


def rgb_from_int(color_value):
    blue = color_value & 255
    green = (color_value >> 8) & 255
    red = (color_value >> 16) & 255
    return np.array([red, green, blue])


def read_image():
    def file_type(file_path):
        if not os.path.exists(file_path):
            raise argparse.ArgumentTypeError('File does not exist')
        return file_path

    parser = argparse.ArgumentParser('Process image')
    parser.add_argument('-f', dest="file_path", required=True, type=file_type,
                        help="input image file path")

    image_path = parser.parse_args().file_path
    img = cv2.imread(image_path)
    return img


if __name__ == "__main__":
    main()
