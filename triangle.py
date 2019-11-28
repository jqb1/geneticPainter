from random import randint

from shape import Shape


class Triangle(Shape):
    def set_init_vertices(self) -> None:
        for i in range(3):
            self.parameters.append([randint(0, self.screen_width), randint(0, self.screen_height)])

    def mutate_vertices(self):
        r1, r2 = randint(0, len(self.parameters) - 1), randint(0, len(self.parameters[0]) - 1)
        self.parameters[r1][r2] -= randint(-int(self.screen_height * self.mutation_strength),
                                           int(self.screen_height * self.mutation_strength))
        if (self.parameters[r1][0] > self.screen_width or self.parameters[r2][1] > self.screen_height
                or any(parameter < 0 for parameter in self.parameters[r1])):
            self.set_init_vertices()
