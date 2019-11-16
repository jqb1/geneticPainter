from unittest.mock import Mock

from genetics import GeneticsController
import cv2
import pygame
import pytest


@pytest.mark.asyncio
async def test_fitness_function():
    cv2_image = cv2.imread('../mona_lisa.png')
    pygame_image = pygame.image.load('../mona_lisa.png')

    painting = Mock()
    painting.draw.return_value = pygame_image
    result, *_ = await GeneticsController.fitness(cv2_image, painting)
    assert result == 0
