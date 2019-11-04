import argparse
import os

import cv2
import numpy as np
import pygame

from painting import Painting

POPULATION_SIZE = 10


def main():
    image = read_image()
    height, width = image.shape[:2]
    screen = pygame.display.set_mode([width, height])

    new_generation = generate_initial_population(width, height, image)
    screen.blit(new_generation[0][1], (0, 0))
    pygame.display.flip()

    # ------------------
    child = crossover(new_generation[0][2], new_generation[1][2])
    fitness(image, child.draw())
    # -------------------
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


def generate_new_population():
    pass


def crossover(parent1, parent2):
    child = Painting(100, parent1.width, parent2.height)
    child.shapes = parent1.shapes[:49] + parent2.shapes[50:99]
    return child


def mutation():
    pass


def generate_initial_population(width, height, image):
    paintings = []
    for _ in range(POPULATION_SIZE):
        painting = Painting(100, width, height)
        painting.create_init_shapes()
        paintings.append(painting)

    images_with_fitneses = [(*fitness(image, painting.draw()), painting) for painting in paintings]
    return sorted(images_with_fitneses, key=lambda k: k[0])


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
