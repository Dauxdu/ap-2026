import os

from lab_02.src.path_iterator import PathIterator
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

UI_PATH = os.path.join(os.path.dirname(__file__), "ui/main_window.ui")
MAX_ZOOM = 4.0
MIN_ZOOM = 0.25
ZOOM_STEP = 0.25


class MainWindow(QMainWindow):
    """
    Главное окно для просмотра изображений из аннотации.
    """

    def __init__(self) -> None:
        """Создать окно и его элементы."""
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.iterator: PathIterator | None = None
        self.annotation_dir = ""
        self.pixmap = QPixmap()
        self.zoom = 1.0

        self.open_button.clicked.connect(self.open_annotation)
        self.previous_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_reset_button.clicked.connect(self.zoom_reset)
        self.zoom_in_button.clicked.connect(self.zoom_in)

    def open_annotation(self) -> None:
        """Выбрать файл аннотации и показать первое изображение."""
        path, _ = QFileDialog.getOpenFileName(self, "Файл аннотации", "", "CSV (*.csv)")
        if not path:
            return

        try:
            iterator = PathIterator(path)
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть аннотацию:\n{exc}")
            return
        if len(iterator) == 0:
            QMessageBox.warning(self, "Пустая аннотация", "В аннотации нет ни одного файла.")
            return

        self.iterator = iterator
        self.annotation_dir = os.path.dirname(path)
        self.statusBar().showMessage(f"Аннотация: {path}")
        self.show_next()

    def update_controls(self) -> None:
        """Обновить доступность кнопок и подпись под изображением."""
        has_image = not self.pixmap.isNull()
        self.zoom_out_button.setEnabled(has_image and self.zoom > MIN_ZOOM)
        self.zoom_reset_button.setEnabled(has_image)
        self.zoom_in_button.setEnabled(has_image and self.zoom < MAX_ZOOM)

        if self.iterator is None:
            return

        self.previous_button.setEnabled(self.iterator.has_previous())
        self.next_button.setEnabled(self.iterator.has_next())

        name = os.path.relpath(self.iterator.current(), self.annotation_dir)
        text = f"{self.iterator.index} из {len(self.iterator)}  ·  {name}"
        if has_image:
            text += f"  ·  {self.pixmap.width()}×{self.pixmap.height()} пикс.  ·  {self.zoom:.0%}"
        self.info_label.setText(text)

    def render_image(self) -> None:
        """Отрисовать изображение в текущем масштабе и обновить кнопки."""
        if not self.pixmap.isNull():
            self.image_label.setPixmap(self.pixmap.scaled(self.pixmap.size() * self.zoom))
        self.update_controls()

    def show_next(self) -> None:
        """Показать следующее изображение."""
        if self.iterator is not None and self.iterator.has_next():
            self.show_image(next(self.iterator))

    def show_previous(self) -> None:
        """Показать предыдущее изображение."""
        if self.iterator is not None and self.iterator.has_previous():
            self.show_image(self.iterator.previous())

    def show_image(self, path: str) -> None:
        """
        Загрузить изображение и показать его в исходном размере.

        :param path: путь к изображению
        """
        self.pixmap = QPixmap(path)
        if self.pixmap.isNull():
            self.image_label.setText(f"Не удалось открыть изображение:\n{path}")
        self.zoom_reset()

    def zoom_reset(self) -> None:
        """Показать изображение в исходном размере."""
        self.zoom = 1.0
        self.render_image()

    def zoom_in(self) -> None:
        """Увеличить масштаб на ZOOM_STEP, но не больше MAX_ZOOM."""
        self.zoom = min(self.zoom + ZOOM_STEP, MAX_ZOOM)
        self.render_image()

    def zoom_out(self) -> None:
        """Уменьшить масштаб на ZOOM_STEP, но не меньше MIN_ZOOM."""
        self.zoom = max(self.zoom - ZOOM_STEP, MIN_ZOOM)
        self.render_image()
