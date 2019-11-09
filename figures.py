import argparse
import os
from random import randint, sample

import cv2
import pygame

from painting import Painting

POPULATION_SIZE = 30
SHAPES_NUMBER = 200

import numpy as np


def main():
    reference_image = read_image()
    height, width = reference_image.shape[:2]
    screen = pygame.display.set_mode([width, height])
    population_num = 0
    changes = 0

    population = generate_initial_population(width, height, reference_image)
    best_image = population[0]
    screen.blit(population[0][1], (0, 0))
    pygame.display.flip()

    running = True
    while running:
        population = generate_new_population(population, reference_image)
        population_num += 1
        print(population_num, changes, best_image[0])

        if population[0][0] < best_image[0]:
            best_image = population[0]
            screen.blit(population[0][1], (0, 0))
            pygame.display.flip()
            changes += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


def generate_new_population(population, reference_image):
    for parent1, parent2 in list(zip(population[0::2], population[1::2]))[:POPULATION_SIZE // 6]:
        population.append(crossover(parent1[2], parent2[2]))

    new_individuals = population[POPULATION_SIZE:]
    population[POPULATION_SIZE:] = [(0, 0, painting) for painting in new_individuals]

    # select some pictures to mutate, mutate random parameter
    for painting in sample(population[1:], POPULATION_SIZE//10):
        mutation(painting[2])

    # remove random addidtional individuals
    for painting in sample(population[1:], len(new_individuals)):
        population.remove(painting)

    population = [(*fitness(reference_image, painting[2].draw()), painting[2])
                  for painting in population]

    return sorted(population, key=lambda k: k[0])


def crossover(parent1, parent2):
    crossover_point = randint(1, SHAPES_NUMBER - 1)
    child = Painting(SHAPES_NUMBER, parent1.width, parent1.height)
    child.shapes = parent1.shapes[:crossover_point] + parent2.shapes[crossover_point:SHAPES_NUMBER]
    return child


def mutation(painting):
    for shape in painting.shapes:
        # shape.mutate_vertices()
        shape.rand_color()


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
