import pygame
import pygame.gfxdraw

from triangle import Triangle


class Painting:
    def __init__(self, shapes_number: int, width: int, height: int):
        self.shapes_number = shapes_number
        self.width = width
        self.height = height
        self.shapes = ()

    def create_init_shapes(self):
        shapes = []
        for i in range(self.shapes_number):
            shape = Triangle(self.width, self.height)
            shape.rand_color()
            shape.set_init_vertices()
            shapes.append(shape)
        self.shapes = tuple(shapes)

    def draw(self):
        surface = pygame.Surface((self.width, self.height))
        for shape in self.shapes:
            if isinstance(shape, Triangle):
                pygame.gfxdraw.filled_polygon(surface, shape.parameters, shape.color)
            else:
                pygame.gfxdraw.filled_circle(surface, *shape.parameters, shape.color)

        return surface
