import sys
from copy import copy

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from .Tetromino import Tetromino


class TetrisGame(QWidget):
    gameOver = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_game()

    def init_ui(self):
        self.setWindowTitle("Tetris")

        # 设置游戏区域的大小
        self.width = 300
        self.height = 600

        self.resize( self.width, self.height)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

    def init_game(self):
        # 创建游戏区域和游戏中的方块
        self.board = [[0] * 10 for _ in range(20)]
        self.current_piece = Tetromino()

        # 设置定时器来控制方块的下落速度
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_down)
        self.timer.start(500)

    def paintEvent(self, event):
        # 绘制游戏区域和方块
        painter = QPainter(self)

        # 绘制游戏区域
        painter.setPen(Qt.NoPen)
        for i in range(20):
            for j in range(10):
                if (i+j)%2 == 0:
                    painter.setBrush(QBrush(QColor(50, 50, 50)))
                else:
                    painter.setBrush(QBrush(QColor(100, 100, 100)))
                painter.drawRect(j * 30, i * 30, 30, 30)

        # 绘制方块
        for x, y in self.current_piece.get_blocks():
            painter.setBrush(QBrush(QColor(self.current_piece.color)))
            painter.drawRect(x * 30, y * 30, 30, 30)

        # 绘制已经触底的方块
        for y in range(20):
            for x in range(10):
                if self.board[y][x] != 0:
                    painter.setBrush(QBrush(QColor(self.board[y][x])))
                    painter.drawRect(x * 30, y * 30, 30, 30)

    def move_down(self):
        # 将当前方块向下移动一个格子
        new_piece = copy(self.current_piece)
        new_piece.move_down()

        if self.is_valid_piece(new_piece):
            del self.current_piece
            self.current_piece = new_piece
        else:
            # 如果方块无法移动，则将其添加到游戏区域中，并生成一个新的方块
            for x, y in self.current_piece.get_blocks():
                self.board[y][x] = self.current_piece.color

            self.current_piece = Tetromino()
            if not self.is_valid_piece(self.current_piece):
                self.timer.stop()
                self.gameOver.emit()

        self.update()

    def is_valid_piece(self, piece):
        # 检查方块是否可以继续移动
        for x, y in piece.get_blocks():
            if x < 0 or x >= 10 or y < 0 or y >= 20 or self.board[y][x] != 0:
                return False
        return True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            new_piece = copy(self.current_piece)
            new_piece.rotate()
            if self.is_valid_piece(new_piece):
                del self.current_piece
                self.current_piece = new_piece
                self.update()
        elif event.key() == Qt.Key_A:
            new_piece = copy(self.current_piece)
            new_piece.move_left()
            if self.is_valid_piece(new_piece):
                del self.current_piece
                self.current_piece = new_piece
                self.update()
        elif event.key() == Qt.Key_S:
            new_piece = copy(self.current_piece)
            new_piece.move_down()
            while self.is_valid_piece(new_piece):
                del self.current_piece
                self.current_piece = new_piece
                new_piece = copy(self.current_piece)
                new_piece.move_down()
            self.update()
        elif event.key() == Qt.Key_D:
            new_piece = copy(self.current_piece)
            new_piece.move_right()
            if self.is_valid_piece(new_piece):
                del self.current_piece
                self.current_piece = new_piece
                self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tetris = TetrisGame()
    tetris.show()
    sys.exit(app.exec_())
