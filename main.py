import arcade
import random
import math
from line import Line
from constants import *
from typing import List

class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.BLACK)

        self.walls = []
        self.rays = []
        self.intersecting_points = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.change_x = 0
        self.change_y = 0
        # self.change_x = 2
        # self.change_y = 2

    def setup(self):
        self.mouse_x = random.randint(0, SCREEN_WIDTH)
        self.mouse_y = random.randint(0, SCREEN_HEIGHT)

        for i in range(WALLS_COUNT):
            x1 = random.randrange(SCREEN_WIDTH)
            x2 = random.randrange(SCREEN_WIDTH)
            y1 = random.randrange(SCREEN_HEIGHT)
            y2 = random.randrange(SCREEN_HEIGHT)

            self.walls.append(Line(x1, y1, x2, y2))
        for i in range(RAYS_COUNT):
            ray = Line(
                    0,
                    0,
                    RAY_LENGTH * math.cos((DEGREES / RAYS_COUNT) * i * (math.pi / 180)),
                    RAY_LENGTH * math.sin((DEGREES / RAYS_COUNT) * i * (math.pi / 180))
                )
            self.rays.append(ray)

    def on_draw(self):
        self.clear()

        self.recalculate()

        self.draw_lines(self.walls, arcade.csscolor.RED)
        self.draw_lines(self.rays, [255,255,255, 0.4*255])

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
        line: Line
        for index, line in enumerate(lines):
            arcade.draw_line(line.start_x, line.start_y, line.end_x, line.end_y, color)



    def recalculate(self):
        # if(self.mouse_x + self.change_x > SCREEN_WIDTH or self.mouse_x + self.change_x < 0):
        #     self.change_x = self.change_x * -1

        # if(self.mouse_y + self.change_y > SCREEN_HEIGHT or self.mouse_y + self.change_y < 0):
        #     self.change_y = self.change_y * -1
        self.mouse_x += self.change_x
        self.mouse_y += self.change_y

        ray: Line
        for index, ray in enumerate(self.rays):
            self.intersecting_points.clear()
            ray.update_b()

            wall: Line
            for wall in self.walls:
                cross_point = ray.cross_point_with_line(wall)
                if(cross_point != None):
                    self.intersecting_points.append(cross_point)

            if (len(self.intersecting_points) != 0):
                intersecting_points_sorted_by_distance = sorted(self.intersecting_points, key= lambda point_data: point_data["distance"])
                end_x = intersecting_points_sorted_by_distance[0]["x"]
                end_y = intersecting_points_sorted_by_distance[0]["y"]
            else:
                end_x = self.mouse_x + RAY_LENGTH * math.cos(((DEGREES) / RAYS_COUNT) * index * (math.pi / 180))
                end_y = self.mouse_y + RAY_LENGTH * math.sin(((DEGREES) / RAYS_COUNT) * index * (math.pi / 180))
                
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