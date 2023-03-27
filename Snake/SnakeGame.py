import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from .Coordinate import Coordinate
from .Snake import Snake


class SnakeGame(QWidget):
    H_CELL_NUM = 20
    V_CELL_NUM = 20
    CELL_SIZE = 30

    gameOver = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_game()

    def init_ui(self):
        self.setWindowTitle("Snake Game")

        self.resize(self.H_CELL_NUM * self.CELL_SIZE, self.V_CELL_NUM * self.CELL_SIZE)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

    def init_game(self):
        # 创建游戏区域和贪吃蛇
        self.board = [[0 for _ in range(self.V_CELL_NUM)] for _ in range(self.H_CELL_NUM)]
        self.snake = Snake(self.H_CELL_NUM,self.V_CELL_NUM)

        # 在游戏区域中随机生成一个食物
        self.generate_food()

        # 设置定时器来控制贪吃蛇的移动速度
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_snake)
        self.timer.start(200)

    def paintEvent(self, event):
        # 绘制游戏区域和贪吃蛇、食物
        painter = QPainter(self)

        # 绘制游戏区域
        painter.setPen(Qt.NoPen)
        for i in range(self.H_CELL_NUM):
            for j in range(self.V_CELL_NUM):
                if (i + j) % 2 == 0:
                    painter.setBrush(QBrush(QColor(50, 50, 50)))
                else:
                    painter.setBrush(QBrush(QColor(100, 100, 100)))
                painter.drawRect(i * self.CELL_SIZE, j * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)

        # 绘制贪吃蛇
        for x, y in self.snake.body:
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawRect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)

        # 绘制食物
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        painter.drawRect(self.food_coord.x * self.CELL_SIZE,
                         self.food_coord.y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)

    def generate_food(self):
        # 随机生成一个食物
        self.food_coord = Coordinate.random_coord(self.H_CELL_NUM-1, self.V_CELL_NUM-1)

    def move_snake(self):
        # 将贪吃蛇移动一个格子
        self.snake.move()

        # 如果贪吃蛇吃到了食物，则将食物放置在新的位置，并将贪吃蛇的长度加一
        if self.snake.head == self.food_coord:
            self.generate_food()
            self.snake.grow()

        # 如果贪吃蛇撞到了边界或者自己的身体，则游戏结束
        if self.snake.head.x < 0 or self.snake.head.x >= self.H_CELL_NUM - 1 or \
                self.snake.head.y < 0 or self.snake.head.y >= self.V_CELL_NUM - 1 or \
                self.snake.head in self.snake.body[1:]:
            self.timer.stop()
            self.gameOver.emit()

        self.update()

    def keyPressEvent(self, event):
        # 让玩家可以通过wasd控制这条贪吃蛇
        key = event.key()
        if key == Qt.Key_W:
            self.snake.change_direction(Coordinate(0, -1))
        elif key == Qt.Key_S:
            self.snake.change_direction(Coordinate(0, 1))
        elif key == Qt.Key_A:
            self.snake.change_direction(Coordinate(-1, 0))
        elif key == Qt.Key_D:
            self.snake.change_direction(Coordinate(1, 0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    snake = SnakeGame()
    snake.show()
    sys.exit(app.exec_())
