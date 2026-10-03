from lab_02.src.path_iterator import PathIterator


class PathHistory:
    """
    История просмотра поверх итератора.
    """

    def __init__(self, iterator: PathIterator) -> None:
        """
        :param iterator: итератор по путям к файлам
        """
        self.iterator = iterator
        self.total = len(iterator.paths)
        self.paths: list[str] = []
        self.position = -1

    def has_next(self) -> bool:
        """Проверить, есть ли путь после текущего."""
        return self.position < self.total - 1

    def has_previous(self) -> bool:
        """Проверить, есть ли путь перед текущим."""
        return self.position > 0

    def next_path(self) -> str:
        """
        Перейти к следующему пути.

        :return: следующий путь
        :raises StopIteration: если пути закончились
        """
        if self.position == len(self.paths) - 1:
            self.paths.append(next(self.iterator))
        self.position += 1
        return self.paths[self.position]

    def previous_path(self) -> str:
        """
        Вернуться к предыдущему пути.

        :return: предыдущий путь
        :raises IndexError: если текущий путь первый
        """
        if not self.has_previous():
            raise IndexError("это первый путь")
        self.position -= 1
        return self.paths[self.position]
