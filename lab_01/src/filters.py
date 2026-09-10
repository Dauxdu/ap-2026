import re
from typing import Callable, Iterable

from src.dataclasses import Profile

# Допустимые значения поля "Пол" для мужчин: М, м, Мужской, мужской.
_MALE_PATTERN = re.compile(r"^(м|мужской)$", re.IGNORECASE)


def is_male(profile: Profile) -> bool:
    """
    Проверет, что анкета принадлежит мужчине.

    :param profile: анкета
    :return: True, если значение поля "Пол" соответствует мужскому полу
    """
    return bool(_MALE_PATTERN.fullmatch(profile.gender))


def filter_profiles(
    profiles: Iterable[Profile], predicate: Callable[[Profile], bool]
) -> list[Profile]:
    """
    Отобирает анкеты, удовлетворяющие заданному условию.

    :param profiles: исходная коллекция анкет
    :param predicate: функция, принимающая анкету и возвращающая True/False
    :return: список анкет, для которых predicate вернул True
    """
    return list(filter(predicate, profiles))
