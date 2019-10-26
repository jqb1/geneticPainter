from random import randint


class Shape:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertices = []
        self.color = self._rand_color()

    def set_init_vertices(self) -> None:
        self.vertices = [
            (randint(1, self.screen_width), randint(1, self.screen_height)),
            (randint(1, self.screen_width), randint(1, self.screen_height)),
            (randint(1, self.screen_width), randint(1, self.screen_height))
        ]

    @staticmethod
    def _rand_color() -> tuple:
        # RGB, alpha
        return randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 180)
