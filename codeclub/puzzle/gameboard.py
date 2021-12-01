from __future__ import annotations

import functools
import os
from abc import ABC, abstractmethod
from enum import Enum, auto
from time import sleep
from typing import Tuple, Callable, List, Dict, Optional, Union
from dataclasses import dataclass
from ipycanvas import MultiCanvas, Canvas, hold_canvas
from ipywidgets import Image

Coordinate = Tuple[int, int]

class CellCorner(Enum):
    TOP_LEFT = (0, 0)
    TOP_RIGHT = (1, 0)
    BOTTOM_LEFT = (0, 1)
    BOTTOM_RIGHT = (1, 1)
    CENTER = (0.5, 0.5)

    @property
    def x_offset(self) -> int:
        return self.value[0]

    @property
    def y_offset(self) -> int:
        return self.value[1]


class ComponentLayer(Enum):
    DYNAMIC = auto()
    STATIC = auto()


class Component(ABC):
    @classmethod
    @property
    def layer_type(cls) -> ComponentLayer:
        return ComponentLayer.DYNAMIC

    @abstractmethod
    def draw(self, board: GameBoard, canvas: Canvas):
        ...

    @abstractmethod
    def set_gameboard(self, board: GameBoard):
        ...


class BlockType(Enum):
    GRASS = "images/grass.png"
    GRASS_GROUND = "images/grass_ground.png"
    ROCK = "images/rock.png"
    DIRT = "images/dirt.png"
    SKY = "images/sky.png"


class StaticBlock(Component):
    def __init__(self, type: BlockType, coord: Coordinate):
        self.type = type
        self.coord = coord
        self.static_canvas(type)

    @classmethod
    @property
    def layer_type(cls) -> ComponentLayer:
        return ComponentLayer.STATIC

    def draw(self, board: GameBoard, canvas: Canvas):
        canvas.draw_image(self.static_canvas(self.type), *board.coordinates(self.coord[0], self.coord[1]))

    def set_gameboard(self, board: GameBoard):
        board.set_cells((self.coord,), self)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def static_canvas(cls, type: BlockType) -> Canvas:
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), type.value))
        canvas = Canvas(width=120, height=120)
        canvas.draw_image(sprite, 0, 0)
        return canvas

    def __str__(self) -> str:
        return f"{self.type.name}{self.coord}"


class Monkey(Component):
    def __init__(self, coord: Coordinate):
        self.coord = coord
        self.static_canvas

    def draw(self, board: GameBoard, canvas: Canvas):
        canvas.draw_image(self.static_canvas, *board.coordinates(self.coord[0], self.coord[1]))

    def set_gameboard(self, board: GameBoard):
        board.set_cells((self.coord,), self)

    @property
    @functools.lru_cache(maxsize=None)
    def static_canvas(self) -> Canvas:
        sprite = Image.from_file(os.path.join(os.path.dirname(__file__), "images/monkey.png"))
        canvas = Canvas(width=120, height=120)
        canvas.draw_image(sprite, 0, 0)
        return canvas

    def __str__(self) -> str:
        return f"MONKEY{self.coord}"

class GameBoard:
    registry: Dict[chr, Callable[[Coordinate], Component]] = {}

    def __init__(self, cols: int = 20, rows: int = 15, cellsize: int = 120):
        self.cols = cols
        self.rows = rows
        self.cellsize = cellsize
        self.cells: List[List[Optional[Component]]] = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self._hovered_cell = None
        self.components: List[Component] = []
        self.canvas = MultiCanvas(5, width=self.width, height=self.height)
        self.canvas.layout.width = "100%"
        self.canvas.layout.height = "auto"
        self.draw_background()
        self.text_canvas.on_mouse_move(self.handle_mouse_move)

    def add(self, coord: Coordinate, component: Component):
        ...

    def __getitem__(self, item: Coordinate) -> Optional[Component]:
        return self.cells[item[1]][item[0]]

    def __setitem__(self, key: Coordinate, value: Optional[Component]):
        self.cells[key[1]][key[0]] = value

    def non_empty_cells(self, cells: Tuple[Coordinate,...], component: Optional[Component] = None) -> Tuple[Coordinate,...]:
        return tuple([cell for cell in cells if self[cell] not in {None, component}])

    def set_cells(self, cells: Tuple[Coordinate,...], component: Optional[Component]):
        for y, row in enumerate(self.cells):
            for x, value in enumerate(row):
                if value == component:
                    self[(x,y)] = None
        for cell in cells:
            self[cell] = component

    def add_component(self, component: Component, draw: bool = True) -> Component:
        self.components.append(component)
        component.set_gameboard(self)
        if draw:
            self.draw(layer=component.layer_type)

        return component

    def draw(self, layer: ComponentLayer = ComponentLayer.DYNAMIC):
        c = self.dynamic_canvas if layer == ComponentLayer.DYNAMIC else self.static_canvas
        with hold_canvas(c):
            c.clear()
            for component in self.components:
                if component.layer_type == layer:
                    component.draw(self, c)

    def animate(self, t1: float, step_function: Callable[[float], None]):
        t = 0.0
        while t < t1:
            step_function(t)
            self.draw()
            t += 0.02
            sleep(0.02)
        step_function(t1)
        self.draw()

    @property
    def width(self) -> int:
        return self.cols * self.cellsize

    @property
    def height(self) -> int:
        return self.rows * self.cellsize

    @property
    def background_canvas(self) -> Canvas:
        return self.canvas[0]

    @property
    def static_canvas(self) -> Canvas:
        return self.canvas[1]

    @property
    def dynamic_canvas(self) -> Canvas:
        return self.canvas[2]

    @property
    def grid_canvas(self) -> Canvas:
        return self.canvas[3]

    @property
    def text_canvas(self) -> Canvas:
        return self.canvas[4]

    @property
    def hovered_cell(self):
        return self._hovered_cell

    @hovered_cell.setter
    def hovered_cell(self, value: Coordinate):
        if value == self._hovered_cell:
            return
        self._hovered_cell = value
        self.draw_text()

    def handle_mouse_move(self, x: int, y: int):
        self.hovered_cell = int(x/self.cellsize), int(y/self.cellsize)

    def draw_text(self):
        c = self.text_canvas
        c.clear_rect(x=0, y=0, width=self.width, height=self.height)
        cell = self.hovered_cell
        if cell is not None:
            c.fill_style = "#FFFFFF"
            c.text_align = "center"
            c.text_baseline = "middle"
            c.font = "32px serif"
            c.fill_text(f"{cell[0],cell[1]}", *self.coordinates(cell[0], cell[1], corner=CellCorner.CENTER))

    def draw_background(self):
        c = self.background_canvas
        c.clear_rect(x=0, y=0, width=self.width, height=self.height)
        c.fill_style = "#CFEEF5"
        c.fill_rect(x=0, y=0, width=self.width, height=self.height)

        c = self.grid_canvas
        c.clear_rect(x=0, y=0, width=self.width, height=self.height)
        c.stroke_style = "#FFFFFF"
        c.begin_path()

        for i in range(1, self.cols):
            c.move_to(*self.coordinates(x=i, y=0))
            c.line_to(*self.coordinates(x=i, y=self.rows-1, corner=CellCorner.BOTTOM_LEFT))
            c.stroke()

        for i in range(1, self.rows):
            c.move_to(*self.coordinates(x=0, y=i))
            c.line_to(*self.coordinates(x=self.cols-1, y=i, corner=CellCorner.TOP_RIGHT))
            c.stroke()

    def coordinates(self, x: Union[int, float] = 0, y: Union[int, float] = 0, corner: CellCorner = CellCorner.TOP_LEFT) -> (int, int):
        return int((x + corner.x_offset)*self.cellsize), int((y + corner.y_offset)*self.cellsize)

    def pixels(self, x: int = 0) -> int:
        return self.cellsize*x

    @classmethod
    def setup(cls, rows: List[str]) -> GameBoard:
        board = GameBoard(rows=len(rows), cols=len(rows[0]))
        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                if value != ' ':
                    func = cls.registry[value]
                    board.add_component(func((x,y)), draw=False)
        board.draw(layer=ComponentLayer.STATIC)
        board.draw(layer=ComponentLayer.DYNAMIC)
        return board


GameBoard.registry['R'] = lambda coord: StaticBlock(type=BlockType.ROCK, coord=coord)
GameBoard.registry['G'] = lambda coord: StaticBlock(type=BlockType.GRASS, coord=coord)
GameBoard.registry['g'] = lambda coord: StaticBlock(type=BlockType.GRASS_GROUND, coord=coord)
GameBoard.registry['D'] = lambda coord: StaticBlock(type=BlockType.DIRT, coord=coord)
GameBoard.registry['M'] = lambda coord: Monkey(coord=coord)


def __warmup():
    canvas = Canvas(width=240, height=240)
    board = GameBoard()
    for func in GameBoard.registry.values():
        component = func((0,0))
        component.draw(board, canvas)


__warmup()