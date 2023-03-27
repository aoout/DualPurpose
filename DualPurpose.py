import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout,QMessageBox
from Tetris import TetrisGame
from Snake import SnakeGame

class DualPurpose(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        self.tetris = TetrisGame()
        self.snake = SnakeGame()

        hbox.addWidget(self.tetris)
        hbox.addWidget(self.snake)

        self.setLayout(hbox)

        self.resize(1300,700)
        self.setWindowTitle('Dual Purpose')
        self.show()

        self.tetris.gameOver.connect(self.onGameOver)
        self.snake.gameOver.connect(self.onGameOver)

    def keyPressEvent(self, event):
        self.tetris.keyPressEvent(event)
        self.snake.keyPressEvent(event)

    def onGameOver(self):
        msgBox = QMessageBox()
        msgBox.setText("Game Over!")
        msgBox.exec_()


    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DualPurpose()
    sys.exit(app.exec_())
