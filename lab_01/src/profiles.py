import re
from datetime import date

FIELD_PATTERNS = {
    "Фамилия": r"[А-Я].*",
    "Имя": r"[А-Я].*",
    "Пол": r"[Мм]ужской|[Жж]енский|[МмЖж]",
    "Дата рождения": (
        r"(?P<day>\d{1,2})(?P<sep>[./-])(?P<month>\d{1,2})(?P=sep)(?P<year>\d{4})"
    ),
    "Номер телефона или email": (
        r"(?:\+7|8)(?:\d{10}| (?:\(\d{3}\)|\d{3}) \d{3}[ -]\d{2}[ -]\d{2})"
        r"|[A-Za-z0-9._%+-]{1,64}@(?:gmail\.com|mail\.ru|yandex\.ru)"
    ),
    "Город": r"(?:г\. )?[А-Я].*",
}

MALE_PATTERN = re.compile(r"^Пол: (?:[Мм]ужской|[Мм])$", re.MULTILINE)


def parse_profiles(text: str) -> list[str]:
    """
    Разбить текст файла на отдельные анкеты.

    Анкеты в файле отделены друг от друга пустой строкой.

    :param text: содержимое файла с анкетами
    :return: список анкет
    """
    blocks = text.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def find_field(profile: str, label: str) -> re.Match | None:
    """
    Найти в анкете поле с указанным названием.

    :param profile: текст анкеты
    :param label: название поля
    :return: совпадение со значением поля в группе "value" или None
    """
    pattern = rf"^{label}: (?P<value>{FIELD_PATTERNS[label]})$"
    return re.search(pattern, profile, re.MULTILINE)


def is_valid_date(profile: str) -> bool:
    """
    Проверить, что дата рождения корректна, год находится в диапазоне от 1900 до текущего.

    :param profile: текст анкеты
    :return: True, если дата рождения корректна
    """
    match = find_field(profile, "Дата рождения")
    if not match:
        return False

    date_string = match["value"]

    date_match = re.match(FIELD_PATTERNS["Дата рождения"], date_string)
    if not date_match:
        return False

    try:
        parsed_date = date(
            int(date_match["year"]),
            int(date_match["month"]),
            int(date_match["day"]),
        )
        return 1900 <= parsed_date.year <= date.today().year
    except ValueError:
        return False


def is_valid(profile: str) -> bool:
    """
    Проверить, что все поля анкеты заполнены в корректном формате.

    :param profile: текст анкеты
    :return: True, если анкета корректна
    """
    return all(
        find_field(profile, label) for label in FIELD_PATTERNS
    ) and is_valid_date(profile)


def is_male(profile: str) -> bool:
    """
    Проверить, что анкета принадлежит мужчине.

    :param profile: текст анкеты
    :return: True, если поле "Пол" имеет мужское значение
    """
    return bool(MALE_PATTERN.search(profile))
