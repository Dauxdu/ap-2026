def read_file(file_path: str) -> str:
    """
    Прочитать содержимое текстового файла.

    :param file_path: путь к файлу
    :return: содержимое файла
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def write_file(file_path: str, text: str) -> None:
    """
    Записать текст в файл.

    :param file_path: путь к файлу
    :param text: текст для записи
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
