import argparse
import os
import time
from copy import deepcopy
from random import randint, sample, random

import cv2
import pygame

from painting import Painting

POPULATION_SIZE = 30
SHAPES_NUMBER = 300


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
    since_last = 0
    running = True
    while running:
        population = generate_new_population(population, reference_image)
        population_num += 1
        print(f'Population:{population_num}, changes so far:{changes}, fitness: {best_image[0]}')
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
    # start = time.time()
    for parent1, parent2 in list(zip(population[0::2], population[1::2]))[:POPULATION_SIZE // 6]:
        population.append(crossover(parent1[2], parent2[2]))

    new_individuals = population[POPULATION_SIZE:]
    population[POPULATION_SIZE:] = [(0, 0, painting) for painting in new_individuals]

    # select some pictures to mutate, mutate random parameter
    for painting in sample(population[1:], POPULATION_SIZE//3):
        mutation(painting[2])

    # remove random additional individuals
    for individual in sample(population[1:], len(new_individuals)):
        population.remove(individual)
    population = [(*fitness(reference_image, painting[2].draw()), painting[2])
                  for painting in population]
    # stop = time.time()
    # print(stop - start)
    return sorted(population, key=lambda k: k[0])


def crossover(parent1, parent2):
    crossover_point = randint(1, SHAPES_NUMBER - 1)
    child = Painting(SHAPES_NUMBER, parent1.width, parent1.height)
    child.shapes = deepcopy(parent1.shapes[:crossover_point]) + deepcopy(parent2.shapes[crossover_point:SHAPES_NUMBER])
    return child


def mutation(painting):
    for shape in sample(painting.shapes, 1):
        if random() > 0.5:
            shape.mutate_vertices()
        else:
            shape.mutate_color()


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
