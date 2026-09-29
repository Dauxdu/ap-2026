# Пользователь вводит строку. Проверьте, является ли введённая строка палиндромом
# (регистр и пробелы игнорировать).
#
# Пример данных:
# "А роза упала на лапу Азора"


def is_palindrome(text: str) -> bool:
    cleaned = "".join(text.split()).lower()
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    print(is_palindrome(input("Введите строку: ")))
