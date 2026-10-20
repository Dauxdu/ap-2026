import os

import pandas as pd


class PathIterator:
    """
    Итератор по абсолютным путям к файлам из csv-аннотации.

    index - сколько путей уже выдано, он же номер текущего пути (с единицы).
    """

    def __init__(self, source: str) -> None:
        """
        :param source: путь к csv-файлу аннотации
        :raises FileNotFoundError: если файл аннотации не существует
        :raises ValueError: если в аннотации нет колонки absolute_path
        """
        if not os.path.isfile(source):
            raise FileNotFoundError(f"Файл аннотации не найден: {source}")
        self.index = 0
        self.paths = self.read_annotation(source)

    def __iter__(self) -> "PathIterator":
        """Вернуть сам итератор."""
        return self

    def __len__(self) -> int:
        """Вернуть общее количество путей."""
        return len(self.paths)

    def __next__(self) -> str:
        """
        Вернуть следующий путь.

        :return: абсолютный путь к файлу
        :raises StopIteration: если пути закончились
        """
        if not self.has_next():
            raise StopIteration
        self.index += 1
        return self.current()

    def previous(self) -> str:
        """
        Вернуться к предыдущему пути.

        :return: абсолютный путь к файлу
        :raises StopIteration: если текущий путь первый
        """
        if not self.has_previous():
            raise StopIteration
        self.index -= 1
        return self.current()

    def current(self) -> str:
        """
        Вернуть последний выданный путь.

        :return: абсолютный путь к файлу
        """
        return self.paths[self.index - 1]

    def has_next(self) -> bool:
        """Проверить, есть ли путь после текущего."""
        return self.index < len(self.paths)

    def has_previous(self) -> bool:
        """Проверить, есть ли путь перед текущим."""
        return self.index > 1

    @staticmethod
    def read_annotation(annotation_file: str) -> list[str]:
        """
        Прочитать абсолютные пути из csv-аннотации.

        :param annotation_file: путь к csv-файлу аннотации
        :return: список абсолютных путей
        :raises ValueError: если в аннотации нет колонки absolute_path
        """
        df = pd.read_csv(annotation_file)
        if "absolute_path" not in df.columns:
            raise ValueError("в аннотации нет колонки absolute_path")
        return df["absolute_path"].tolist()
