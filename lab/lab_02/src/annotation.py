import os

import pandas as pd


def write_annotation(paths: list[str], annotation_file: str) -> None:
    """
    Сохранить csv-аннотацию с абсолютным и относительным путём к файлам.

    Относительный путь считается от папки, где лежит файл аннотации.

    :param paths: пути к скачанным файлам
    :param annotation_file: путь к csv-файлу аннотации
    """
    base_dir = os.path.dirname(os.path.abspath(annotation_file))

    absolute_paths = [os.path.abspath(path) for path in paths]
    relative_paths = [os.path.relpath(p, base_dir) for p in absolute_paths]

    annotation = pd.DataFrame(
        {"absolute_path": absolute_paths, "relative_path": relative_paths}
    )
    annotation.to_csv(annotation_file, index=False)
