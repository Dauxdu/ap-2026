import os
import argparse

import requests

from src.annotation import write_annotation
from src.path_iterator import PathIterator
from src.scraper import (
    get_genres,
    get_book_urls,
    get_cover_url,
    download_covers,
    download_file,
)


def parse_arguments() -> argparse.Namespace:
    """
    Разобрать и проверить аргументы командной строки.

    :return: аргументы count, output_dir и annotation_file
    """
    parser = argparse.ArgumentParser(description="Скачивание обложек книг.")
    parser.add_argument("count", type=int, help="книг одного жанра (от 1)")
    parser.add_argument("output_dir", type=str, help="папка для обложек")
    parser.add_argument("annotation_file", type=str, help="csv-аннотация")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("количество книг жанра должно быть не меньше 1")
    return args


def main(count: int, output_dir: str, annotation_file: str) -> None:
    """
    Скачать обложки, составить аннотацию и обойти файлы итератором.

    :param count: сколько обложек скачать для каждого жанра
    :param output_dir: папка для сохранения
    :param annotation_file: путь к csv-файлу аннотации
    """
    try:
        paths = download_covers(output_dir, count)
        write_annotation(paths, annotation_file)
        print(f"Скачано обложек: {len(paths)}")
        print(f"Аннотация: {annotation_file}")
        for path in PathIterator(annotation_file):
            print(path)
    except requests.RequestException as exc:
        print(f"Ошибка сети: {exc}")
    except OSError as exc:
        print(f"Ошибка при работе с файлами: {exc}")


if __name__ == "__main__":
    args = parse_arguments()
    main(args.count, args.output_dir, args.annotation_file)
