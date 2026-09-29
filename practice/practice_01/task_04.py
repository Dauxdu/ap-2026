# Дана строка (любая). Посчитайте количество каждого символа в этой строке
# и выведите на экран в порядке убывания количества.
#
# Пример данных:
# "abcaabbbcccc"
#
# Пример вывода:
# c: 5
# b: 4
# a: 3

from collections import Counter
from itertools import starmap

text = input("Введите строку: ")
print(*starmap("{}: {}".format, Counter(text).most_common()), sep="\n")
