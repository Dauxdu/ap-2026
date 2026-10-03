import cv2
import pandas as pd


def load_annotation(annotation_file: str) -> pd.DataFrame:
    """
    Загрузить аннотацию в DataFrame.

    :param annotation_file: путь к csv-файлу аннотации
    :return: таблица с колонками absolute_path и relative_path
    """
    return pd.read_csv(
        annotation_file, header=0, names=["absolute_path", "relative_path"]
    )


def get_image_height(path: str) -> int:
    """
    Получить длину (высоту) изображения в пикселях.

    :param path: путь к изображению
    :return: количество строк пикселей
    :raises FileNotFoundError: если изображение не удалось прочитать
    """
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"не удалось прочитать изображение: {path}")
    return image.shape[0]


def add_height_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавить колонку height с длиной каждого изображения.

    :param df: таблица с колонкой absolute_path
    :return: новая таблица с колонкой height
    """
    return df.assign(height=df["absolute_path"].apply(get_image_height))


def sort_by_height(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """
    Отсортировать таблицу по длине изображения.

    :param df: таблица с колонкой height
    :param ascending: True - по возрастанию, False - по убыванию
    :return: отсортированная таблица
    """
    return df.sort_values("height", ascending=ascending)


def filter_by_height(
    df: pd.DataFrame, min_height: int, max_height: int
) -> pd.DataFrame:
    """
    Оставить изображения с длиной в заданном диапазоне.

    :param df: таблица с колонкой height
    :param min_height: минимальная длина
    :param max_height: максимальная длина
    :return: отфильтрованная таблица
    """
    return df[df["height"].between(min_height, max_height)]
