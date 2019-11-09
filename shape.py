from random import randint, random


class Shape:
    mutation_strength = 10

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.parameters = []
        self.color = ()

    def set_init_vertices(self) -> None:
        x = randint(0, self.screen_width)
        y = randint(0, self.screen_height)
        r = randint(1, self.screen_height // 10)
        self.parameters = [x, y, r]

    def rand_color(self) -> None:
        # RGB, alpha
        self.color = randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 180)

    def mutate_color(self):
        if random() > 0.5:
            new_color = [color + int(255 * self.mutation_strength) for color in self.color]
            new_color[-1] += 180 * self.mutation_strength
            self.color = tuple(new_color)
        else:
            new_color = [color - int(255 * self.mutation_strength) for color in self.color]
            new_color[-1] = 180 * self.mutation_strength
            self.color = tuple(new_color)

    def mutate_vertices(self):
        r = randint(0, len(self.parameters) - 1)
        if r == 2:
            self.parameters[r] -= randint(-1, 1)

        if(self.parameters[r]) < 0:
            self.parameters[r] = 0
