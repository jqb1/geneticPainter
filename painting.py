import pygame
import pygame.gfxdraw

from shape import Shape


class Painting:
    def __init__(self, shapes_number: int, width: int, height: int):
        self.shapes_number = shapes_number
        self.width = width
        self.height = height
        self.shapes = []

    def create_init_shapes(self):
        for i in range(self.shapes_number):
            shape = Shape(self.width, self.height)
            shape.set_init_vertices()
            self.shapes.append(shape)

    def draw(self):
        surface = pygame.Surface((self.width, self.height))
        for shape in self.shapes:
            pygame.gfxdraw.filled_polygon(surface, shape.vertices, shape.color)

        return surface
