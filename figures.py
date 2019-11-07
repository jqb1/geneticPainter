import argparse
import os

import cv2
import pygame

from painting import Painting
from random import randint

POPULATION_SIZE = 20
SHAPES_NUMBER = 50


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


def generate_new_population(previous_population, reference_image):
    def mutate_random_shapes(_painting):
        for _ in range(randint(3, 10)):
            selected_shape = _painting[2].shapes[randint(1, SHAPES_NUMBER - 2)]
            selected_shape.rand_color()
            selected_shape.mutate_vertices()
        return _painting[2]

    new_population = []
    child1, child2 = crossover(previous_population[0][2], previous_population[1][2])
    mutation(child1)
    mutation(child2)
    new_population.extend([child1, child2])

    for painting in previous_population[2:POPULATION_SIZE]:
        new_population.append(mutate_random_shapes(painting))

    images_with_fitneses = [(*fitness(reference_image, painting.draw()), painting) for painting in new_population]
    return sorted(images_with_fitneses, key=lambda k: k[0])


def crossover(parent1, parent2):
    child1 = Painting(SHAPES_NUMBER, parent1.width, parent1.height)
    child2 = Painting(SHAPES_NUMBER, parent1.width, parent1.height)
    child1.shapes = parent1.shapes[:SHAPES_NUMBER // 2] + parent2.shapes[SHAPES_NUMBER // 2:SHAPES_NUMBER]
    child2.shapes = parent1.shapes[SHAPES_NUMBER // 2:SHAPES_NUMBER] + parent2.shapes[:SHAPES_NUMBER // 2]
    return child1, child2


def mutation(painting):
    for _ in range(SHAPES_NUMBER // 20):
        r = randint(1, len(painting.shapes) - 1)
        shape_to_mutate = painting.shapes[r]
        shape_to_mutate.mutate_vertices()
        shape_to_mutate.rand_color()


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
