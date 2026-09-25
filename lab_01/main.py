import argparse

from src.io import read_file, write_file
from src.profiles import parse_profiles, is_valid, is_male


def parse_arguments() -> argparse.Namespace:
    """
    Прочитать аргументы командной строки.

    :return: аргументы input и output
    """
    parser = argparse.ArgumentParser(description="Подсчёт анкет мужчин.")
    parser.add_argument("input", type=str, help="файл с анкетами")
    parser.add_argument(
        "-o", "--output", type=str, default="output.txt", help="файл для результата"
    )
    return parser.parse_args()


def main(input: str, output: str) -> None:
    """
    Отобрать мужские анкеты, вывести их количество и сохранить в файл.

    :param input: путь к файлу с анкетами
    :param output: путь к файлу для сохранения результата
    """
    try:
        profiles = parse_profiles(read_file(input))
        valid_profiles = [profile for profile in profiles if is_valid(profile)]
        male_profiles = [profile for profile in valid_profiles if is_male(profile)]
        print(f"Количество анкет мужчин: {len(male_profiles)}")
        write_file(output, "\n\n".join(male_profiles) + "\n")
        print(f"Анкеты сохранены в файл: {output}")
    except OSError as exc:
        print(f"Ошибка при работе с файлом: {exc}")


if __name__ == "__main__":
    args = parse_arguments()
    main(args.input, args.output)
