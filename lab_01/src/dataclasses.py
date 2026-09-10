from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    """
    Класс анкеты человека из файла с исходными данными.

    :param index: порядковый номер анкеты
    :param surname: фамилия
    :param name: имя
    :param gender: пол
    :param birth_date: дата рождения
    :param contact: номер телефона или email
    :param city: город
    :param raw_text: исходный текст анкеты
    """

    index: int
    surname: str
    name: str
    gender: str
    birth_date: str
    contact: str
    city: str
    raw_text: str
