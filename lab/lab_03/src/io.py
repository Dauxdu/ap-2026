import cv2
import numpy as np


def read_image(path: str) -> np.ndarray:
    """
    Прочитать цветное изображение из файла.

    :param path: путь к изображению
    :return: изображение
    :raises FileNotFoundError: если файл не удалось прочитать
    """
    image = cv2.imread(path, cv2.IMREAD_COLOR_RGB)
    if image is None:
        raise FileNotFoundError(f"не удалось прочитать изображение: {path}")
    return image


def write_image(path: str, image: np.ndarray) -> None:
    """
    Сохранить изображение в файл. Формат определяется по расширению.

    :param path: путь для сохранения
    :param image: изображение
    :raises OSError: если изображение не удалось сохранить
    """
    # OpenCV при записи ожидает порядок каналов BGR
    if not cv2.imwrite(path, image):
        raise OSError(f"не удалось сохранить изображение: {path}")
