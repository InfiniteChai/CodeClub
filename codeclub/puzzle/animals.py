import functools
from typing import List, Optional

from ipycanvas import Canvas
from ipywidgets import Image
import os
from codeclub.puzzle.gameboard import Component, GameBoard, CellCorner


class Snake(Component):
    def __init__(self, x: int, y: int, length: int = 2):
        self.x = x
        self.y = y
        self._length = length
        self.game_board: Optional[GameBoard] = None

    def set_gameboard(self, board: GameBoard):
        self.game_board = board
        board.set_cells(tuple((self.x+i, self.y) for i in range(self.length)), self)

    def draw(self, board: GameBoard, canvas: Canvas):
        dynamic_width = board.pixels(self.length-1)
        canvas.save()
        canvas.begin_path()
        canvas.rect(*board.coordinates(self.x + 1, self.y, corner=CellCorner.TOP_LEFT), width=dynamic_width, height=board.pixels(2))
        canvas.clip()
        canvas.draw_image(self.dynamic_canvas, *board.coordinates(self.x + self.length - 9, self.y, corner=CellCorner.TOP_LEFT))
        canvas.restore()
        canvas.draw_image(self.static_canvas, *board.coordinates(self.x, self.y, corner=CellCorner.TOP_LEFT))

    @classmethod
    @property
    @functools.lru_cache(maxsize=None)
    def dynamic_canvas(cls):
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), "images/snake_right.png"))
        canvas = Canvas(width=120*10, height=240)
        canvas.draw_image(sprite, 0, 0)
        return canvas

    @classmethod
    @property
    @functools.lru_cache(maxsize=None)
    def static_canvas(cls):
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), "images/snake_left.png"))
        canvas = Canvas(width=240, height=240)
        canvas.draw_image(sprite, 0, 0)
        return canvas

    @property
    def length(self) -> int:
        return self._length

    @length.setter
    def length(self, value: int):
        if value == self._length:
            return

        l0 = self._length
        cells = self.game_board.non_empty_cells(tuple((self.x+i, self.y) for i in range(value)), self)
        if len(cells) == 0:
            t1 = abs(l0 - value)/4.0
            def animation_step(t):
                self._length = (l0*(t1-t) + value*t)/t1
            self.game_board.animate(t1, animation_step)
            self._length = value
            self.game_board.set_cells(tuple((self.x + i, self.y) for i in range(self.length)), self)
        else:
            l1 = cells[0][0] - self.x
            if l0 != l1:
                t1 = abs(l0 - l1)/4.0
                def animation_step(t):
                    self._length = (l0*(t1-t) + l1*t)/t1
                self.game_board.animate(t1, animation_step)
                self._length = l1
                self.game_board.set_cells(tuple((self.x + i, self.y) for i in range(self.length)), self)
            #self.game_board.error_cell(cells[0])
            raise Exception(f"Cannot set snake length to {value} as will hit cell {cells[0]}")


class Crocodile(Component):
    def __init__(self, x: int, y: int, open: bool = False):
        self.x = x
        self.y = y
        self._open = open
        self.game_board: Optional[GameBoard] = None

    @property
    def mouth_closed(self) -> bool:
        return not self._open

    def toggle(self):
        self._open = not self._open
        self.set_gameboard(self.game_board)
        self.game_board.draw()

    def set_gameboard(self, board: GameBoard):
        self.game_board = board
        cells = [(self.x, self.y), (self.x+1, self.y)]
        if self._open:
            cells.append((self.x, self.y-1))
        board.set_cells(tuple(cells), self)

    def draw(self, board: GameBoard, canvas: Canvas):
        image = self.open_canvas if self._open else self.close_canvas
        canvas.draw_image(image, *board.coordinates(self.x, self.y-0.5, corner=CellCorner.TOP_LEFT))

    @classmethod
    @property
    @functools.lru_cache(maxsize=None)
    def open_canvas(cls):
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), "images/croc_open.png"))
        canvas = Canvas(height=120 * 11, width=240)
        canvas.draw_image(sprite, 0, 0)
        return canvas

    @classmethod
    @property
    @functools.lru_cache(maxsize=None)
    def close_canvas(cls):
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), "images/croc_close.png"))
        canvas = Canvas(height=120 * 11, width=240)
        canvas.draw_image(sprite, 0, 0)
        return canvas


class Well(Component):
    def __init__(self, x: int, y: int, level: int = 1, max_level: int = 1):
        self.x = x
        self.y = y
        self._level = level
        self.crocodile = Crocodile(x, y + 1 - level, open=False)
        self.max_level = max_level
        self.game_board: Optional[GameBoard] = None

    @property
    def water_level(self) -> int:
        return self._level

    def fill(self):
        if self._level >= self.max_level:
            raise Exception("The well is already full!")
        t1 = 0.25
        l0 = self._level
        def animation_step(t):
            self._level = (l0*(t1-t) + (l0+1)*t)/t1
            self.crocodile.y = self.y + 1 - self._level

        self.game_board.animate(t1, animation_step)
        self.crocodile.y = self.y - l0
        self._level = l0 + 1
        self.crocodile.set_gameboard(self.game_board)

    def empty(self):
        t1 = (self._level - 1 ) * 0.25
        l0 = self._level

        def animation_step(t):
            self._level = (l0 * (t1 - t) + t) / t1
            self.crocodile.y = self.y + 1 - self._level
        if l0 != 1:
            self.game_board.animate(t1, animation_step)
        self.crocodile.y = self.y + 1
        self._level = 1
        self.crocodile.set_gameboard(self.game_board)

    def set_gameboard(self, board: GameBoard):
        board.add_component(self.crocodile, draw=True)
        #board.components[-2] = self.crocodile
        #board.components[-1] = self

        self.game_board = board

    def draw(self, board: GameBoard, canvas: Canvas):
        canvas.save()
        canvas.fill_style = "#5c78e4"
        canvas.global_alpha = 0.2
        canvas.fill_rect(*board.coordinates(self.x, self.y-self._level, corner=CellCorner.BOTTOM_LEFT), width=board.pixels(2), height=board.pixels(self._level))
        canvas.restore()


class Giraffe(Component):
    def __init__(self, x: int, y: int, height: int = 2):
        self.x = x
        self.y = y
        self._height = height
        self.game_board: Optional[GameBoard] = None

    def set_gameboard(self, board: GameBoard):
        self.game_board = board
        board.set_cells(tuple((self.x, self.y-i) for i in range(self.height)), self)

    def draw(self, board: GameBoard, canvas: Canvas):
        dynamic_height = board.pixels(self.height-1)
        canvas.save()
        canvas.begin_path()
        canvas.rect(*board.coordinates(self.x, self.y+1-self.height, corner=CellCorner.TOP_LEFT), height=dynamic_height, width=board.pixels(2))
        canvas.clip()
        canvas.draw_image(self.dynamic_canvas, *board.coordinates(self.x, self.y + 1 - self.height, corner=CellCorner.TOP_LEFT))
        canvas.restore()
        canvas.draw_image(self.static_canvas, *board.coordinates(self.x, self.y, corner=CellCorner.TOP_LEFT))

    @classmethod
    @property
    @functools.lru_cache(maxsize=None)
    def dynamic_canvas(cls):
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), "images/giraffe_top.png"))
        canvas = Canvas(height=120*11, width=240)
        canvas.draw_image(sprite, 0, 0)
        return canvas

    @classmethod
    @property
    @functools.lru_cache(maxsize=None)
    def static_canvas(cls):
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), "images/giraffe_bottom.png"))
        canvas = Canvas(width=240, height=240)
        canvas.draw_image(sprite, 0, 0)
        return canvas

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int):
        if value == self._height:
            return

        h0 = self._height
        cells = self.game_board.non_empty_cells(tuple((self.x, self.y-i) for i in range(value)), self)
        if len(cells) == 0:
            t1 = abs(h0 - value)/4.0
            def animation_step(t):
                self._height = (h0*(t1-t) + value*t)/t1
            self.game_board.animate(t1, animation_step)
            self._height = value
            self.game_board.set_cells(tuple((self.x, self.y-i) for i in range(self.height)), self)
        else:
            h1 = cells[0][0] - self.y
            if h0 != h1:
                t1 = abs(h0 - h1)/4.0
                def animation_step(t):
                    self._height = (h0*(t1-t) + h1*t)/t1
                self.game_board.animate(t1, animation_step)
                self._height = h1
                self.game_board.set_cells(tuple((self.x, self.y-i) for i in range(self.height)), self)
            #self.game_board.error_cell(cells[0])
            raise Exception(f"Cannot set giraffe height to {value} as will hit cell {cells[0]}")


def __warmup():
    canvas = Canvas(width=100, height=100)
    board = GameBoard()
    component = Snake(x=0, y=0)
    component.draw(board, canvas)
    component = Giraffe(x=0, y=0)
    component.draw(board, canvas)


__warmup()