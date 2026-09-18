import argparse

from src.io import read_file, write_file
from src.profiles import is_male, parse_profiles


def parse_arguments() -> argparse.Namespace:
    """
    Разобрать аргументы командной строки.

    :return: аргументы input_file и output
    """
    parser = argparse.ArgumentParser(description="Подсчёт анкет мужчин.")
    parser.add_argument("input_file", type=str, help="файл с анкетами")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.txt",
        help="файл для результата",
    )
    return parser.parse_args()


def main(input_file: str, output_file: str) -> None:
    """
    Отобрать мужские анкеты, вывести их количество и сохранить в файл.

    :param input_file: путь к файлу с анкетами
    :param output_file: путь к файлу для сохранения результата
    """
    try:
        profiles = parse_profiles(read_file(input_file))
        male_profiles = [profile for profile in profiles if is_male(profile)]
        print(f"Количество анкет мужчин: {len(male_profiles)}")
        write_file(output_file, "\n\n".join(male_profiles) + "\n")
        print(f"Анкеты сохранены в файл: {output_file}")
    except OSError as exc:
        print(f"Ошибка при работе с файлом: {exc}")


if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output)
