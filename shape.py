from random import randint


class Shape:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertices = []
        self.color = self.rand_color()

    def set_init_vertices(self) -> None:
        self.vertices = [
            [randint(1, self.screen_width), randint(1, self.screen_height)],
            [randint(1, self.screen_width), randint(1, self.screen_height)],
            [randint(1, self.screen_width), randint(1, self.screen_height)]
        ]

    @staticmethod
    def rand_color() -> tuple:
        # RGB, alpha
        return randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 180)

    def mutate_vertices(self):
        for vertice in self.vertices:
            if vertice[0] % 2 == 0:
                (vertice[0] + randint(1, self.screen_width // 20), vertice[1] + randint(1, self.screen_height // 20))
            else:
                (vertice[0] - randint(1, self.screen_width // 20), vertice[1] - randint(1, self.screen_height // 20))
