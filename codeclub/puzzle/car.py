import functools
import os
from typing import Optional

from ipycanvas import Canvas
from ipywidgets import Image

from codeclub.puzzle.animals import Crocodile
from codeclub.puzzle.gameboard import Component, GameBoard, CellCorner, Monkey


class Car(Component):
    def __init__(self, x: int, y: int):
        self.coord = (x, y)
        self.game_board: Optional[GameBoard] = None

    def set_gameboard(self, board: GameBoard):
        self.game_board = board
        board.set_cells((self.coord,), self)

    def draw(self, board: GameBoard, canvas: Canvas):
        canvas.draw_image(self.car_canvas, *board.coordinates(self.coord[0], self.coord[1], corner=CellCorner.TOP_LEFT))

    @classmethod
    @property
    @functools.lru_cache(maxsize=None)
    def car_canvas(cls):
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), "images/car.png"))
        canvas = Canvas(width=120, height=120)
        canvas.draw_image(sprite, 0, 0)
        return canvas

    def drive(self):
        position = self.coord
        result = None
        path = [position]
        # Work out the path we'll draw, plus the result
        while True:
            # Next check if we've reached the end of the board.
            if position[0] == self.game_board.cols - 1:
                result = False
                break

            if position[1] < self.game_board.rows - 1:
                below = self.game_board[(position[0], position[1]+1)]
                if below is None:
                    position = (position[0], position[1]+1)
                    path.append(position)
                    continue
                if isinstance(below, Crocodile) and not below.mouth_closed:
                    result = False
                    break

            right = self.game_board[(position[0]+1, position[1])]
            # We've reached the target
            if isinstance(right, Monkey):
                result = True
                break

            if right is None:
                position = (position[0]+1, position[1])
                path.append(position)
                continue

            result = False
            break

        # Only bother drawing if we have somewhere to go!
        if len(path) > 1:
            t1 = len(path)/6.0

            def animation_step(t):
                # Let's start with just a linear path (we'll switch to a curve later)
                f = t * 6.0
                i = int(f)
                a = f - i
                if i >= len(path) - 1:
                    self.coord = path[-1]
                else:
                    c0 = path[i]
                    c1 = path[i+1]
                    self.coord = (c0[0]*(1-a) + c1[0]*a, c0[1]*(1-a) + c1[1]*a)

            self.game_board.animate(t1, animation_step)

        self.coord = path[-1]
        self.game_board.set_cells((self.coord,), self)

        if not result:
            raise Exception("Blocked from further movement")

        print("Car reached the monkey successfully. Well done!")


def __warmup():
    canvas = Canvas(width=100, height=100)
    board = GameBoard()
    component = Car(x=0, y=0)
    component.draw(board, canvas)


__warmup()