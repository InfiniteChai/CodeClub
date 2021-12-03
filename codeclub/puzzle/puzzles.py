from codeclub.puzzle import GameBoard, Car, Giraffe, Snake, Well


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
        "                    ",
        "GGGGG GG            ",
        "    G  GG           ",
        "    G   GG          ",
        "    G    GG        M",
        "    G     GGGGGGGGGG",
        "    gggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=5))
    giraffe = board.add_component(Giraffe(x=5, y=10, height=2))
    return board, car, giraffe

def puzzle4():
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


def puzzle5():
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


def puzzle6():
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

def puzzle7():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                   M",
        "R    R R     R RRRRR",
        "RRRRRR RRRRRRR RRRRR",
        "                    ",
        "                    ",
        "      G             ",
        "      G       G     ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=2))
    snake_1 = board.add_component(Snake(x=1, y=3, length=2))
    snake_2 = board.add_component(Snake(x=8, y=3, length=2))
    giraffe_1 = board.add_component(Giraffe(x=6, y=6, height=2))
    giraffe_2 = board.add_component(Giraffe(x=14, y=7, height=2))
    return board, car, snake_1, snake_2, giraffe_1, giraffe_2


def puzzle8():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "RG                  ",
        "RGG G               ",
        "RGG GG G            ",
        "       GG G        M",
        "          GG GGGGGGG",
        "                    ",
        "                    ",
        "GGGGGGGGGGGGGGGGGGGG",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=1))
    giraffe_1 = board.add_component(Giraffe(x=3, y=8, height=2))
    giraffe_2 = board.add_component(Giraffe(x=6, y=8, height=2))
    giraffe_3 = board.add_component(Giraffe(x=9, y=8, height=2))
    giraffe_4 = board.add_component(Giraffe(x=12, y=8, height=2))
    return board, car, giraffe_1, giraffe_2, giraffe_3, giraffe_4


def puzzle9():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                    ",
        "                   M",
        "RRRRRRRRR       RRRR",
        "RRRRRRRRRR      RRRR",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=3))
    snake_1 = board.add_component(Snake(x=9, y=4, length=2))
    giraffe_1 = board.add_component(Giraffe(x=11, y=9, height=8))
    return board, car, snake_1, giraffe_1


def puzzle10():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "GGGG GGGGGGGGGG    M",
        "GGG         GGGGGGGG",
        "   G                ",
        "   G                ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=3))
    snake_1 = board.add_component(Snake(x=3, y=5, length=7))
    giraffe_1 = board.add_component(Giraffe(x=4, y=7, height=2))
    return board, car, snake_1, giraffe_1


def puzzle11():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                   M",
        "GGG GG GG GGG GGGGGG",
        "                    ",
        "                    ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=4))
    giraffes = [board.add_component(Giraffe(x=3, y=7, height=6)), board.add_component(Giraffe(x=6, y=7, height=6)),
                board.add_component(Giraffe(x=9, y=7, height=6)), board.add_component(Giraffe(x=13, y=7, height=6))]
    return board, car, giraffes

def puzzle12():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                    ",
        "GGG G               ",
        "    GG G            ",
        "    GG GG G        M",
        "    GG GG GGG GGGGGG",
        "                    ",
        "                    ",
        "                    ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=2))
    giraffes = [board.add_component(Giraffe(x=3, y=9, height=8)), board.add_component(Giraffe(x=6, y=9, height=8)),
                board.add_component(Giraffe(x=9, y=9, height=8)), board.add_component(Giraffe(x=13, y=9, height=8))]
    return board, car, giraffes


def puzzle13():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                   M",
        "R R R R R R R R R RR",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                 G   ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=2))
    giraffes = []
    for x in range(1,17,2):
        giraffes.append(board.add_component(Giraffe(x=x,y=9,height=4)))
    giraffes.append(board.add_component(Giraffe(x=17, y=8, height=6)))
    return board, car, giraffes


def puzzle14():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                   M",
        "RRR  RRRRRRRRRRRRRRR",
        "  R  R              ",
        "  R  R              ",
        "  RRRR              ",
        "                    ",
        "                    ",
        "                    ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=2))
    well = board.add_component(Well(x=3, y=5, max_level=3))
    well.crocodile.toggle()
    return board, car, well


def puzzle15():
    board = GameBoard.setup([
        "                    ",
        "                    ",
        "                   M",
        "RRR  R  R  R  R  RRR",
        "  R  R  R  R  R  R  ",
        "  R  R  R  R  R  R  ",
        "  RRRRRRRRRRRRRRRR  ",
        "                    ",
        "gggggggggggggggggggg",
    ])

    car = board.add_component(Car(x=0, y=2))
    wells = [
        board.add_component(Well(x=3, y=5, max_level=3)),
        board.add_component(Well(x=6, y=5, max_level=3)),
        board.add_component(Well(x=9, y=5, max_level=3)),
        board.add_component(Well(x=12, y=5, max_level=3)),
        board.add_component(Well(x=15, y=5, max_level=3)),
    ]
    wells[2].crocodile.toggle()
    wells[3].crocodile.toggle()
    return board, car, wells