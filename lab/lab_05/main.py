import sys

from lab_05.src.window import MainWindow
from PyQt6.QtWidgets import QApplication


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
