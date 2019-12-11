import argparse
import os
import asyncio
from copy import deepcopy
from random import randint, sample, random
import cv2
import pygame

from painting import Painting


class GeneticsController:

    def __init__(self, reference_image, population_size: int, shapes_number: int, triangles: bool, save_interval: bool):
        self.population_size = population_size if population_size else 30
        if shapes_number:
            self.shapes_number = shapes_number
        elif triangles:
            self.shapes_number = 50
        else:
            self.shapes_number = 150
        self.reference_image = reference_image
        self.draw_triangles = triangles
        self.save_interval = save_interval

    def start_genetics(self, ):
        height, width = self.reference_image.shape[:2]
        screen = pygame.display.set_mode([width, height])
        population_num = 0
        changes = 0

        population = self.generate_initial_population(width, height)
        best_image = population[0]
        screen.blit(population[0][1], (0, 0))
        pygame.display.flip()
        running = True
        while running:
            event_loop = asyncio.get_event_loop()
            asyncio.set_event_loop(event_loop)
            population = event_loop.run_until_complete(self.generate_new_population(population))
            if self.save_interval and population_num % self.save_interval == 0:
                save_image(best_image[1], f'{population_num}x{best_image[0]}.jpg')
            population_num += 1
            print(f'Population:{population_num}, changes so far:{changes}, fitness: {best_image[0]}')
            if population[0][0] < best_image[0] or best_image[0] == 0:
                best_image = population[0]
                screen.blit(population[0][1], (0, 0))
                pygame.display.flip()
                changes += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.display.quit()

    async def generate_new_population(self, population: list):

        for parent1, parent2 in list(zip(population[0::2], population[1::2]))[:self.population_size // 6]:
            population.append(self.crossover(parent1[2], parent2[2]))

        new_individuals = population[self.population_size:]
        population[self.population_size:] = [(0, 0, painting) for painting in new_individuals]

        # select some pictures to mutate, mutate random parameter
        for painting in sample(population[1:], self.population_size // 3):
            self.mutation(painting[2])

        # remove random additional individuals
        for individual in sample(population[1:], len(new_individuals)):
            population.remove(individual)

        async def pop_generator():
            for ind in population:
                yield ind[2]

        population = [await self.fitness(self.reference_image, individual) async for individual in pop_generator()]
        return sorted(population, key=lambda k: k[0])

    def crossover(self, parent1: Painting, parent2: Painting):
        crossover_point = randint(1, self.shapes_number - 1)
        child = Painting(self.shapes_number, parent1.width, parent1.height)
        child.shapes = deepcopy(parent1.shapes[:crossover_point]) + deepcopy(
            parent2.shapes[crossover_point:self.shapes_number])
        return child

    @staticmethod
    def mutation(painting: Painting):
        for shape in sample(painting.shapes, 1):
            if random() > 0.5:
                shape.mutate_vertices()
            else:
                shape.mutate_color()

    def generate_initial_population(self, width: int, height: int):
        paintings = []
        for _ in range(self.population_size):
            painting = Painting(self.shapes_number, width, height)
            painting.create_init_shapes(self.draw_triangles)
            paintings.append(painting)

        images = [(0, painting.draw(), painting) for painting in paintings]
        return images

    @staticmethod
    async def fitness(image, painting: Painting) -> tuple:
        # transpose from (width, height) to (height, width) and change from RGB to BGR
        painting_surface = painting.draw()
        painting_array = pygame.surfarray.pixels3d(painting_surface).transpose([1, 0, 2])
        paiting_image = cv2.cvtColor(painting_array, cv2.COLOR_RGB2BGR)
        diff = cv2.absdiff(paiting_image, image).sum()
        return diff, painting_surface, painting


def read_image():
    def file_type(file_path):
        if not os.path.exists(file_path):
            raise argparse.ArgumentTypeError('File does not exist')
        return file_path

    parser = argparse.ArgumentParser('Process image')
    parser.add_argument('-f', dest='file_path', required=True, type=file_type,
                        help="input image file path")

    parser.add_argument('-p', dest='size_of_population', required=False, type=int,
                        help="population size")

    parser.add_argument('-n', dest='numer_of_shapes', required=False, type=int,
                        help='number of shapes')

    parser.add_argument('-t', action='store_true', required=False, help='Draw with triangles')
    parser.add_argument('-s', dest='saving_interval', required=False, type=int,
                        help='Set saving image interval, saving results in your current dir')

    args = parser.parse_args()

    img = cv2.imread(args.file_path)
    genetics_controller = GeneticsController(img, args.size_of_population, args.numer_of_shapes, args.t,
                                             args.saving_interval)
    genetics_controller.start_genetics()


def save_image(window, filename):
    pygame.image.save(window, filename)


if __name__ == "__main__":
    read_image()
