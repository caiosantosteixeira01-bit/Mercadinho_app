from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()
