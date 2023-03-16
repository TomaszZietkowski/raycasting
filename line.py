from __future__ import annotations

import math

from constants import *


class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y
        self.a = self.calculate_a(self)
        self.b = self.calculate_b(self)
        self.directed_right = start_x < end_x

    def cross_point_with_line(self, other_line: Line):
        if self.is_parallel(other_line):
            return None

        if self.am_i_vertical():
            x_c = self.start_x
            y_c = other_line.a * x_c + other_line.b
        else:
            x_c = (self.b - other_line.b) / (other_line.a - self.a)
            y_c = self.a * x_c + self.b

        if x_c < self.start_x and self.directed_right:
            return None
        elif x_c > self.start_x and self.directed_right == False:
            return None

        distance = math.sqrt((x_c - self.start_x) ** 2 + (y_c - self.start_y) ** 2)

        if distance > RAY_LENGTH:
            return None

        is_other_line_directed_up = other_line.start_y < other_line.end_y

        if is_other_line_directed_up and (y_c >= other_line.start_y and y_c <= other_line.end_y) == False:
            return None
        elif is_other_line_directed_up == False and (y_c <= other_line.start_y and y_c >= other_line.end_y) == False:
            return None
        else:
            return {"x": x_c, "y": y_c, "distance": distance}

    def is_parallel(self, other_line: Line):
        return self.a == other_line.a

    def am_i_vertical(self):
        return self.start_x == self.end_x

    def calculate_a(self, line: Line):
        if line.start_x == line.end_x:
            return 0

        return (line.start_y - line.end_y) / (line.start_x - line.end_x)

    def calculate_b(self, line: Line):
        return line.start_y - self.a * line.start_x

    def update_b(self):
        if self.start_x == self.end_x:
            self.b = SCREEN_HEIGHT
        else:
            self.b = self.calculate_b(self)

    def __str__(self):
        return f"start x {self.start_x}, start_y {self.start_y}, end_x { self.end_x}, end_y {self.end_y},  a {self.a}.  b {self.b}"
