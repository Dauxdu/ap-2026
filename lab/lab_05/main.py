import sys

from lab_05.src.main_window import MainWindow
from PyQt6.QtWidgets import QApplication


def main() -> None:
    """Запустить приложение для просмотра изображений."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
