import random

from shape import Shape


class Circle(Shape):
    def set_init_vertices(self) -> None:
        x = random.randint(0, self.screen_width)
        y = random.randint(0, self.screen_height)
        r = random.randint(2, self.screen_height // 10)
        self.parameters = [x, y, r]

    def mutate_vertices(self):
        r = random.randint(0, len(self.parameters) - 1)
        self.parameters[r] -= random.randint(-int(self.screen_height * self.mutation_strength),
                                      int(self.screen_height * self.mutation_strength))
        if (self.parameters[0] > self.screen_width or self.parameters[1] > self.screen_height or
                self.parameters[2] > self.screen_height // 2 or any(parameter < 0 for parameter in self.parameters)):
            self.set_init_vertices()
