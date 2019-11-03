import argparse
import os

import cv2
import numpy as np
import pygame
import pygame.gfxdraw

from shape import Shape

population_size = 10


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

    paintings = [Painting(100, width, height).draw() for _ in range(population_size)]
    images_with_fitneses = [fitness(image, painting) for painting in paintings]
    best_painting = sorted(images_with_fitneses, key=lambda k: k[0])[0]

    screen.blit(best_painting[1], (0, 0))
    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


def fitness(image, painting_surface) -> tuple:
    # transpose from (width, height) to (height, width) and change from RGB to BGR
    painting_array = pygame.surfarray.array3d(painting_surface).transpose([1, 0, 2])
    paiting_image = cv2.cvtColor(painting_array, cv2.COLOR_RGB2BGR)
    diff = cv2.absdiff(paiting_image, image).sum()
    return diff, painting_surface


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
