from random import randint


class Shape:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertices = []
        self.color = ()

    def set_init_vertices(self) -> None:
        self.vertices = [
            [randint(1, self.screen_width), randint(1, self.screen_height)],
            [randint(1, self.screen_width), randint(1, self.screen_height)],
            [randint(1, self.screen_width), randint(1, self.screen_height)]
        ]

    def rand_color(self) -> tuple:
        # RGB, alpha
        self.color = randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 180)

    def mutate_vertices(self):
        for i in range(len(self.vertices)):
            if self.vertices[i][0] % 2 == 0:
                self.vertices[i] = [self.vertices[i][0] + randint(1, self.screen_width // 20),
                                    self.vertices[i][1] + randint(1, self.screen_height // 20)]
            else:
                self.vertices[i] = [self.vertices[i][0] - randint(1, self.screen_width // 20),
                                    self.vertices[i][1] - randint(1, self.screen_height // 20)]
