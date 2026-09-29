# Пользователь вводит список целых чисел. Напишите функцию подсчёта количества
# положительных чисел в списке.


def count_positive(numbers: list[int]) -> int:
    return len(list(filter(lambda n: n > 0, numbers)))


if __name__ == "__main__":
    numbers = list(map(int, input("Введите целые числа через пробел: ").split()))
    print(f"Положительных чисел: {count_positive(numbers)}")
