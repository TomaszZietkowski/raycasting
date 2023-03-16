import math
import random
from typing import List

import arcade

from line import Line


class MyGame(arcade.Window):
    def __init__(
        self,
        screen_width: int = 800,
        screen_height: int = 640,
        screen_title: str = "Ray tracing",
        walls_count: int = 20,
    ):

        # Call the parent class and set up the window
        super().__init__(screen_width, screen_height, screen_title)

        arcade.set_background_color(arcade.csscolor.BLACK)

        self.walls: List = []
        self.rays: List = []
        self.intersecting_points: List = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.change_x = 0
        self.change_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.__degress = 360
        self.__rays_count = math.floor(self.__degress * 2.04)
        self.wall_count = walls_count

    def setup(self):
        self.mouse_x = random.randint(0, self.screen_width)
        self.mouse_y = random.randint(0, self.screen_height)
        self.walls = [
            Line(
                start_x=random.randrange(self.screen_width),
                end_x=random.randrange(self.screen_width),
                start_y=random.randrange(self.screen_height),
                end_y=random.randrange(self.screen_height),
                ray_length=self.screen_width,
                screen_height=self.screen_height,
            )
            for i in range(self.wall_count)
        ]
        self.rays = [
            Line(
                start_x=0,
                start_y=0,
                end_x=self.screen_width * math.cos((self.__degress / self.__rays_count) * i * (math.pi / 180)),
                end_y=self.screen_width * math.sin((self.__degress / self.__rays_count) * i * (math.pi / 180)),
                ray_length=self.screen_width,
                screen_height=self.screen_height,
            )
            for i in range(self.__rays_count)
        ]

    def on_draw(self):
        self.clear()

        self.recalculate()

        self.draw_lines(self.walls, arcade.csscolor.RED)
        self.draw_lines(self.rays, [255, 255, 255, 0.4 * 255])

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_x = x
        self.mouse_y = y

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.change_y = 1
        elif key == arcade.key.DOWN:
            self.change_y = -1
        elif key == arcade.key.LEFT:
            self.change_x = -1
        elif key == arcade.key.RIGHT:
            self.change_x = 1

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0

    def draw_lines(self, lines: List[Line], color=arcade.csscolor.WHITE):

        for line in lines:
            arcade.draw_line(line.start_x, line.start_y, line.end_x, line.end_y, color)

    def recalculate(self):
        # if(self.mouse_x + self.change_x > SCREEN_WIDTH or self.mouse_x + self.change_x < 0):
        #     self.change_x = self.change_x * -1

        # if(self.mouse_y + self.change_y > SCREEN_HEIGHT or self.mouse_y + self.change_y < 0):
        #     self.change_y = self.change_y * -1
        self.mouse_x += self.change_x
        self.mouse_y += self.change_y

        for index, ray in enumerate(self.rays):
            self.intersecting_points.clear()
            ray.update_b()

            for wall in self.walls:
                cross_point = ray.cross_point_with_line(wall)
                if cross_point:
                    self.intersecting_points.append(cross_point)

            if len(self.intersecting_points) != 0:
                intersecting_points_sorted_by_distance = sorted(
                    self.intersecting_points, key=lambda point_data: point_data["distance"]
                )
                end_x = intersecting_points_sorted_by_distance[0]["x"]
                end_y = intersecting_points_sorted_by_distance[0]["y"]
            else:
                end_x = self.mouse_x + self.screen_width * math.cos(
                    ((self.__degress) / self.__rays_count) * index * (math.pi / 180)
                )
                end_y = self.mouse_y + self.screen_width * math.sin(
                    ((self.__degress) / self.__rays_count) * index * (math.pi / 180)
                )

            ray.start_x = self.mouse_x
            ray.start_y = self.mouse_y
            ray.end_x = end_x
            ray.end_y = end_y


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
