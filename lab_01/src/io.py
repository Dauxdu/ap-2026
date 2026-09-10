from src.dataclasses import Profile


def read_file(file_path: str) -> str:
    """
    Читает содержимое текстового файла с анкетами.

    :param file_path: путь к файлу
    :return: содержимое файла в виде строки
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def write_profiles(file_path: str, profiles: list[Profile]) -> None:
    """
    Сохраняет список анкет в новый файл.

    :param file_path: путь к файлу для сохранения результата
    :param profiles: список анкет для записи
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n\n".join(profile.raw_text for profile in profiles))
        file.write("\n")
