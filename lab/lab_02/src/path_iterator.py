import os

import pandas as pd


class PathIterator:
    """
    Итератор по абсолютным путям к файлам из csv-аннотации.
    """

    def __init__(self, source: str) -> None:
        """
        :param source: путь к csv-файлу аннотации
        :raises FileNotFoundError: если файл аннотации не существует
        """
        if not os.path.isfile(source):
            raise FileNotFoundError(f"Файл аннотации не найден: {source}")
        self.index = 0
        self.paths = self.read_annotation(source)

    @staticmethod
    def read_annotation(annotation_file: str) -> list[str]:
        """
        Прочитать абсолютные пути из csv-аннотации.

        :param annotation_file: путь к csv-файлу аннотации
        :return: список абсолютных путей
        """
        return pd.read_csv(annotation_file)["absolute_path"].tolist()

    def __iter__(self) -> "PathIterator":
        """Вернуть сам итератор."""
        return self

    def __next__(self) -> str:
        """
        Вернуть следующий путь.

        :return: абсолютный путь к файлу
        :raises StopIteration: если пути закончились
        """
        if self.index >= len(self.paths):
            raise StopIteration
        path = self.paths[self.index]
        self.index += 1
        return path
