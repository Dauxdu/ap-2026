import re

MALE_PATTERN = re.compile(r"^Пол:\s*(?:[Мм]ужской|[Мм])$", re.MULTILINE)


def parse_profiles(text: str) -> list[str]:
    """
    Разбить текст файла на отдельные анкеты.

    Анкеты в файле отделены друг от друга пустой строкой.

    :param text: содержимое файла с анкетами
    :return: список анкет
    """
    blocks = text.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def is_male(profile: str) -> bool:
    """
    Проверить, что анкета принадлежит мужчине.

    :param profile: текст анкеты
    :return: True, если поле "Пол" имеет мужское значение
    """
    return MALE_PATTERN.search(profile) is not None
