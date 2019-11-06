import argparse
import os

import cv2
import numpy as np
import pygame

from painting import Painting
from random import randint, choices
POPULATION_SIZE = 10
SHAPES_NUMBER = 50


def main():
    image = read_image()
    height, width = image.shape[:2]
    screen = pygame.display.set_mode([width, height])

    population = generate_initial_population(width, height, image)
    screen.blit(population[0][1], (0, 0))
    pygame.display.flip()

    running = True
    while running:
        population = generate_new_population(population)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


def generate_new_population(previous_population):
    def mutate_random_shapes(_painting):
        for _ in range(randint(3, 10)):
            selected_shape = _painting[2].shapes[randint(1, SHAPES_NUMBER-1)]
            selected_shape.rand_color()
            selected_shape.mutate_vertices()
        return _painting[2]

    new_population = []
    new_population.extend(crossover(previous_population[0][2], previous_population[1][2]))
    for painting in previous_population[2:POPULATION_SIZE]:
        new_population.append(mutate_random_shapes(painting))
    return new_population
    # fitness(image, child.draw()) !!!!!!!!!!!!!!!


def crossover(parent1, parent2):
    child1 = Painting(SHAPES_NUMBER, parent1.width, parent1.height)
    child2 = Painting(SHAPES_NUMBER, parent1.width, parent1.height)
    child1.shapes = parent1.shapes[:49] + parent2.shapes[50:99]
    child2.shapes = parent1.shapes[50:99] + parent2.shapes[:49]
    return child1, child2


def mutation(painting):
    pass


def generate_initial_population(width, height, image):
    paintings = []
    for _ in range(POPULATION_SIZE):
        painting = Painting(SHAPES_NUMBER, width, height)
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
