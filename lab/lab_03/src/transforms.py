import cv2
import numpy as np


def crop(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Обрезать изображение до заданного размера от левого верхнего угла.

    :param image: исходное изображение
    :param width: ширина результата
    :param height: высота результата
    :return: обрезанное изображение
    :raises ValueError: если заданный размер больше изображения
    """
    image_height, image_width = image.shape[:2]
    if width > image_width or height > image_height:
        raise ValueError(
            f"размер обрезки {width}x{height} больше изображения "
            f"{image_width}x{image_height}"
        )
    return image[:height, :width]


def rotate(image: np.ndarray, angle: float) -> np.ndarray:
    """
    Повернуть изображение вокруг центра, сохранив его размер.

    Углы, вышедшие за границы, обрезаются, освободившаяся
    область заполняется чёрным.

    :param image: исходное изображение
    :param angle: угол в градусах, положительный - против часовой стрелки
    :return: повёрнутое изображение
    """
    image_height, image_width = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((image_width / 2, image_height / 2), angle, 1)
    return cv2.warpAffine(image, matrix, (image_width, image_height))


def overlay(image: np.ndarray, top: np.ndarray, alpha: float) -> np.ndarray:
    """Наложить полупрозрачное изображение поверх другого.

    Накладываемое изображение приводится к размеру основного.

    :param image: основное изображение
    :param top: накладываемое изображение
    :param alpha: непрозрачность накладываемого, от 0 до 1
    :return: результат наложения
    """
    image_height, image_width = image.shape[:2]
    top = cv2.resize(top, (image_width, image_height))
    return cv2.addWeighted(image, 1 - alpha, top, alpha, 0.0)
