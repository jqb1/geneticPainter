from genetics import fitness
import cv2
import pygame


def test_fitness_function():
    cv2_image = cv2.imread('../monia350x350.png')
    pygame_image = pygame.image.load('../monia350x350.png')
    diff, _ = fitness(cv2_image, pygame_image)
    assert diff == 0
