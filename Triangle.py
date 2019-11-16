from random import randint

from shape import Shape


class Triangle(Shape):
    def set_init_vertices(self) -> None:
        for i in range(3):
            self.parameters.append(randint(0, self.screen_width), randint(0, self.screen_height))

    def rand_color(self) -> None:
        # RGB, alpha
        self.color = randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 180)

    def mutate_vertices(self):
        r = randint(0, len(self.parameters) - 1)
        self.parameters[r] -= randint(-20, 20)
        if (self.parameters[0] > self.screen_width or self.parameters[1] > self.screen_height or
                self.parameters[2] > self.screen_height // 2 or any(parameter < 0 for parameter in self.parameters)):
            self.set_init_vertices()
