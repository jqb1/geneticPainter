from random import randint, random


class Shape:
    mutation_strength = 0.2

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.parameters = []
        self.color = ()

    def rand_color(self) -> None:
        # RGB, alpha
        self.color = randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 180)

    def mutate_color(self):
        new_color = [color + randint(-int(255 * self.mutation_strength), int(255 * self.mutation_strength))
                     for color in self.color[:-1]]
        new_color.append(self.color[-1])
        self.color = tuple(new_color)

        if any(color > 255 or color < 0 for color in self.color[:-1]):
            self.rand_color()
