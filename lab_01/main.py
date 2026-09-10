"""
Лабораторная работа №1. Вариант 1.

Задание: посчитать количество анкет мужчин в списке анкет.
Вывести их количество на экран и сохранить эти анкеты в новый файл.
"""

import argparse

from src.parser import parse_profiles
from src.io import read_file, write_profiles
from src.filters import filter_profiles, is_male


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    :return: пространство имён с аргументами input_file и output_file
    """
    argparser = argparse.ArgumentParser(
        description="Подсчёт количества анкет мужчин и сохранение их в отдельный файл."
    )
    argparser.add_argument("input_file", type=str, help="путь к файлу с анкетами")
    argparser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.txt",
        help="путь к файлу для сохранения результата",
    )
    return argparser.parse_args()


def main(input_file: str, output_file: str) -> None:
    """
    :param input_file: путь к исходному файлу с анкетами
    :param output_file: путь к файлу для сохранения мужских анкет
    """
    try:
        text = read_file(input_file)

        profiles = parse_profiles(text)
        if not profiles:
            print("В файле не найдено ни одной корректной анкеты.")
            return

        male_profiles = filter_profiles(profiles, is_male)

        print(f"Количество анкет мужчин: {len(male_profiles)}")

        write_profiles(output_file, male_profiles)
        print(f"Анкеты мужчин сохранены в файл: {output_file}")
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.input_file}' не найден.")
    except OSError as exc:
        print(f"Ошибка при работе с файлами: {exc}")


if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output)
