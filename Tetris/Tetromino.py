import random

class Tetromino:
    """
    A class representing a tetromino (a block in Tetris)
    """

    # Define the different shapes and colors of the tetrominoes
    SHAPES = {
        'I': [[1, 1, 1, 1]],
        'O': [[1, 1], [1, 1]],
        'T': [[0, 1, 0], [1, 1, 1]],
        'S': [[0, 1, 1], [1, 1, 0]],
        'Z': [[1, 1, 0], [0, 1, 1]],
        'J': [[1, 0, 0], [1, 1, 1]],
        'L': [[0, 0, 1], [1, 1, 1]],
    }
    COLORS = {
        'I': 'cyan',
        'O': 'yellow',
        'T': 'purple',
        'S': 'green',
        'Z': 'red',
        'J': 'blue',
        'L': 'orange',
    }

    def __init__(self):
        """
        Initializes a new Tetromino object with the specified shape, color, and position.
        """
        key = random.choice(list(Tetromino.SHAPES.keys()))
        self.shape = Tetromino.SHAPES[key]
        self.color = Tetromino.COLORS[key]
        self.x = 0
        self.y = 0
        self.rotation = 0

    def move_down(self):
        """
        Moves the tetromino down one row.
        """
        self.y += 1

    def move_left(self):
        """
        Moves the tetromino left one column.
        """
        self.x -= 1

    def move_right(self):
        """
        Moves the tetromino right one column.
        """
        self.x += 1

    def rotate(self):
        """
        Rotates the tetromino clockwise 90 degrees.
        """
        self.rotation = (self.rotation + 1) % 4
        self.shape = list(zip(*reversed(self.shape)))

    def get_blocks(self):
        """
        Returns the coordinates of the blocks in the tetromino.
        """
        blocks = []
        for y, row in enumerate(self.shape):
            for x, block in enumerate(row):
                if block:
                    blocks.append((self.x + x, self.y + y))
        return blocks


