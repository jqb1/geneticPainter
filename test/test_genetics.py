from unittest.mock import Mock

from circle import Circle
from genetics import GeneticsController
from painting import Painting
import cv2
import pygame
import pytest

SHAPES_NUMBER = 150
SHAPE = Circle


@pytest.fixture
def random_painting():
    painting = Painting(SHAPES_NUMBER, 100, 100)
    painting.create_init_shapes(False)
    return painting


@pytest.mark.asyncio
async def test_fitness_function():
    cv2_image = cv2.imread('../test_images/mona_lisa.png')
    pygame_image = pygame.image.load('../test_images/mona_lisa.png')

    painting = Mock()
    painting.draw.return_value = pygame_image
    result, *_ = await GeneticsController.fitness(cv2_image, painting)
    assert result == 0


def test_painting_creation(random_painting):
    assert len(random_painting.shapes) == SHAPES_NUMBER
    assert all(isinstance(shape, Circle) for shape in random_painting.shapes)


def test_painting_draw(random_painting):
    surface = random_painting.draw()
    assert isinstance(surface, pygame.Surface)


def test_mutate_vertices():
    circle = Circle(100, 100)
    circle.parameters = [1, 2, 3]
    circle.mutate_vertices()
    assert circle.parameters != [1, 2, 3]
