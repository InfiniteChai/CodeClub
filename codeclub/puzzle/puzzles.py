from codeclub.puzzle import GameBoard, Car, Giraffe, Snake


def puzzle1():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "gggG                ",
        "DDDggggG            ",
        "DDDDDDDggggG        ",
        "DDDDDDDDDDDggggG   M",
        "DDDDDDDDDDDDDDDggggg",
    ])
    car = board.add_component(Car(x=0, y=1))
    return board, car


def puzzle2():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "ggggG Gggggg       M",
        "DDDDG GDDDDggggggggg",
        "DDDDG GDDDDDDDDDDDDD",
        "DDDDG GDDDDDDDDDDDDD",
        "DDDDG GDDDDDDDDDDDDD",
        "DDDDgggDDDDDDDDDDDDD",
    ])

    car = board.add_component(Car(x=0, y=5))
    giraffe = board.add_component(Giraffe(x=5, y=10, height=2))
    return board, car, giraffe


def puzzle3():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                   M",
        "RRRR RRRRRRR RRRRRRR",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=5))
    giraffe_1 = board.add_component(Giraffe(x=4, y=10, height=8))
    giraffe_2 = board.add_component(Giraffe(x=12, y=10, height=8))
    return board, car, giraffe_1, giraffe_2


def puzzle4():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                   M",
        "GGG         GGGGGGGG",
        "gggggggggggggggggggg",
        "DDDDDDDDDDDDDDDDDDDD",
        "DDDDDDDDRRRDDDDDDDDD",
        "RRRRRRRRRRRRRRRRRRRR",
    ])

    car = board.add_component(Car(x=0, y=2))
    snake = board.add_component(Snake(x=3, y=3, length=2))
    return board, car, snake


def puzzle5():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                   M",
        "RR          RR    RR",
        "RRR         RRR   RR",
        "RRR         RRR   RR",
        "RRRRRRRRRRRRRRRRRRRR",
    ])

    car = board.add_component(Car(x=0, y=2))
    snake_1 = board.add_component(Snake(x=2, y=3, length=2))
    snake_2 = board.add_component(Snake(x=14, y=3, length=2))
    return board, car, snake_1, snake_2