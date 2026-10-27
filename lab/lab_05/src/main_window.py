import math
import os

from lab_02.src.path_iterator import PathIterator
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

UI_PATH = os.path.join(os.path.dirname(__file__), "ui/main_window.ui")
ZOOM_STEP = 0.25
MIN_ZOOM = 0.25
MAX_ZOOM = 4.0


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
        self.zoom: float | None = None

        self.open_button.clicked.connect(self.open_annotation)
        self.previous_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.fit_button.clicked.connect(self.fit_to_window)
        self.zoom_in_button.clicked.connect(self.zoom_in)

        self.update_controls()

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
        self.zoom_out_button.setEnabled(has_image)
        self.fit_button.setEnabled(has_image)
        self.zoom_in_button.setEnabled(has_image)

        if self.iterator is None:
            self.previous_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.info_label.setText("")
            return

        self.previous_button.setEnabled(self.iterator.has_previous())
        self.next_button.setEnabled(self.iterator.has_next())

        name = os.path.relpath(self.iterator.current(), self.annotation_dir)
        text = f"{self.iterator.index} из {len(self.iterator)}  ·  {name}"
        if has_image:
            text += f"  ·  {self.pixmap.width()}×{self.pixmap.height()} пикс.  ·  {self.current_scale():.0%}"
        self.info_label.setText(text)

    def render_image(self) -> None:
        """Отрисовать изображение в текущем масштабе и обновить кнопки."""
        if not self.pixmap.isNull():
            scaled = self.pixmap.scaled(
                self.pixmap.size() * self.current_scale(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled)
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
        Загрузить изображение и показать его вписанным в окно.

        :param path: путь к изображению
        """
        self.pixmap = QPixmap(path)
        if self.pixmap.isNull():
            self.image_label.setText(f"Не удалось открыть изображение:\n{path}")
        self.fit_to_window()

    def current_scale(self) -> float:
        """
        Масштаб, в котором сейчас показывается изображение.

        Если масштаб не выбран, изображение вписывается в окно, но
        только уменьшается: маленькое показывается в исходном размере.

        :return: масштаб изображения
        """
        if self.zoom is not None:
            return self.zoom
        available = self.scroll_area.viewport().size()
        # запас в 2 пикселя, чтобы не появлялись полосы прокрутки
        return min(
            1.0,
            (available.width() - 2) / self.pixmap.width(),
            (available.height() - 2) / self.pixmap.height(),
        )

    def zoom_in(self) -> None:
        """Увеличить масштаб до следующего кратного ZOOM_STEP, но не больше MAX_ZOOM."""
        steps = math.floor(self.current_scale() / ZOOM_STEP + 1e-6) + 1
        self.zoom = min(steps * ZOOM_STEP, MAX_ZOOM)
        self.render_image()

    def zoom_out(self) -> None:
        """Уменьшить масштаб до предыдущего кратного ZOOM_STEP, но не меньше MIN_ZOOM."""
        steps = math.ceil(self.current_scale() / ZOOM_STEP - 1e-6) - 1
        self.zoom = max(steps * ZOOM_STEP, MIN_ZOOM)
        self.render_image()

    def fit_to_window(self) -> None:
        """Вписать изображение в окно."""
        self.zoom = None
        self.render_image()
