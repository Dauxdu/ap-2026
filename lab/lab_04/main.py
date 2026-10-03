import argparse

from src.dataframe import (
    add_height_column,
    filter_by_height,
    load_annotation,
    sort_by_height,
)
from src.plot import plot_histogram


def parse_arguments() -> argparse.Namespace:
    """
    Разобрать и проверить аргументы командной строки.

    :return: пути к файлам и границы фильтрации
    """
    parser = argparse.ArgumentParser(description="Анализ длины изображений.")
    parser.add_argument("annotation", type=str, help="csv-аннотация")
    parser.add_argument("output_csv", type=str, help="файл для таблицы")
    parser.add_argument("output_plot", type=str, help="файл для графика")
    parser.add_argument(
        "--min-height", type=int, required=True, help="минимальная длина"
    )
    parser.add_argument(
        "--max-height", type=int, required=True, help="максимальная длина"
    )
    args = parser.parse_args()

    if args.min_height < 0 or args.min_height > args.max_height:
        parser.error("минимальная и максимальная длина должны быть > 0 и min <= max")
    return args


def main() -> None:
    args = parse_arguments()

    try:
        df = load_annotation(args.annotation)
        if df.empty:
            print("В аннотации нет ни одного файла.")
            return
        df = add_height_column(df)
        print(f"Загружено изображений: {len(df)}")

        sorted_df = sort_by_height(df)
        filtered_df = filter_by_height(sorted_df, args.min_height, args.max_height)
        print(f"Длина от {args.min_height} до {args.max_height}: ")
        print(f"{len(filtered_df)} изображений")
        print(filtered_df[["relative_path", "height"]].to_string(index=False))

        sorted_df.to_csv(args.output_csv, index=False)
        print(f"Таблица сохранена: {args.output_csv}")

        plot_histogram(sorted_df, args.output_plot)
        print(f"График сохранён: {args.output_plot}")

    except ValueError as exc:
        print(f"Ошибка: {exc}")
    except OSError as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
