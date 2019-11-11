from random import randint, random


class Shape():
    mutation_strength = 0.4

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.parameters = []
        self.color = ()

    def set_init_vertices(self) -> None:
        x = randint(0, self.screen_width)
        y = randint(0, self.screen_height)
        r = randint(5, self.screen_height // 10)
        self.parameters = [x, y, r]

    def rand_color(self) -> None:
        # RGB, alpha
        self.color = randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 180)

    def mutate_color(self):
        if random() > 0.5:
            new_color = [color + randint(0, int(255 * self.mutation_strength)) for color in self.color[:-1]]
            new_color.append(self.color[-1])
            self.color = tuple(new_color)
        else:
            new_color = [color - randint(0, int(255 * self.mutation_strength)) for color in self.color[:-1]]
            new_color.append(self.color[-1])
            self.color = tuple(new_color)

        if any(color > 255 or color < 0 for color in self.color[:-1]):
            self.rand_color()

    def mutate_vertices(self):
        r = randint(0, len(self.parameters) - 1)
        self.parameters[r] -= randint(-10, 10)
        if self.parameters[0] > self.screen_width or self.parameters[1] > self.screen_height or \
                self.parameters[2] > self.screen_height // 2 or any(parameter < 0 for parameter in self.parameters):
            self.set_init_vertices()
