from PyQt5.QtWidgets import QMainWindow, QAction, QApplication
from PyQt5.QtGui import QIcon
from canvas import Canvas
from model import MyModel


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self._setupUI()
        self._setupToolbar()

    def _setupUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("MyGLDrawer")

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.model = MyModel()
        self.canvas.setModel(self.model)

    def _setupToolbar(self):
        tb = self.addToolBar("File")
        actions = [
            ("icons/FIT.png", "fit"),
            #("icons/fit.jpg", "rotate"),
        ]

        for icon, text in actions:
            action = QAction(QIcon(icon), text, self)
            tb.addAction(action)

        tb.actionTriggered[QAction].connect(self._toolbarAction)

    def _toolbarAction(self, action):
        if action.text() == "fit":
            self.canvas.fitWorldToViewport()
