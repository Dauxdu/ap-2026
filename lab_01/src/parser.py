import re

from src.dataclasses import Profile

_PROFILE_PATTERN = re.compile(
    r"(?P<index>\d+)\)\s*\n"
    r"Фамилия:\s*(?P<surname>.+)\n"
    r"Имя:\s*(?P<name>.+)\n"
    r"Пол:\s*(?P<gender>.+)\n"
    r"Дата рождения:\s*(?P<birth_date>.+)\n"
    r"Номер телефона или email:\s*(?P<contact>.+)\n"
    r"Город:\s*(?P<city>.+)"
)


def parse_profiles(text: str) -> list[Profile]:
    """
    Извлекает список анкет из текста файла.

    :param text: содержимое файла с анкетами
    :return: список объектов Profile в порядке их появления в файле
    """
    profiles = []
    for match in _PROFILE_PATTERN.finditer(text):
        profiles.append(_match_to_profile(match))
    return profiles


def _match_to_profile(match: re.Match) -> Profile:
    """
    Преобразует найденное совпадение регулярного выражения в объект Profile.

    :param match: объект совпадения, полученный из _PROFILE_PATTERN
    :return: анкета, собранная из групп совпадения
    """
    return Profile(
        index=int(match.group("index")),
        surname=match.group("surname").strip(),
        name=match.group("name").strip(),
        gender=match.group("gender").strip(),
        birth_date=match.group("birth_date").strip(),
        contact=match.group("contact").strip(),
        city=match.group("city").strip(),
        raw_text=match.group(0).strip(),
    )
