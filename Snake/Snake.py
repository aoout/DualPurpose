from .Coordinate import Coordinate


class Snake:
    def __init__(self,H_CELL_NUM:int,V_CELL_NUM:int) -> None:
        self.body = [Coordinate.random_coord(H_CELL_NUM-4, V_CELL_NUM-4,3,3)]
        self.direction = Coordinate(1, 0)
        self.head = self.body[0]

    def move(self) -> None:
        self.head = self.head + self.direction
        self.body.insert(0, self.head)
        self.body.pop()

    def change_direction(self, new_direction:Coordinate) -> None:
        if not self.direction + new_direction == Coordinate(0, 0):
            self.direction = new_direction

    def grow(self) -> None:
        tail = self.body[-1] - self.direction
        self.body.append(tail)
