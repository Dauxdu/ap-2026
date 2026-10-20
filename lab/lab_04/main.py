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
    parser.add_argument("--min-height", type=int, required=True, help="минимальная длина")
    parser.add_argument("--max-height", type=int, required=True, help="максимальная длина")
    args = parser.parse_args()

    if args.min_height < 0 or args.min_height > args.max_height:
        parser.error("минимальная и максимальная длина должны быть > 0 и min <= max")
    return args


def main(
    annotation_path: str,
    output_csv_path: str,
    output_plot_path: str,
    min_height: int,
    max_height: int,
) -> None:
    """
    Отсортировать изображения по длине, отфильтровать и сохранить таблицу и гистограмму.

    :param annotation_path: путь к csv-аннотации
    :param output_csv_path: путь для сохранения таблицы
    :param output_plot_path: путь для сохранения графика
    :param min_height: минимальная длина изображения
    :param max_height: максимальная длина изображения
    """
    try:
        df = load_annotation(annotation_path)
        if df.empty:
            print("В аннотации нет ни одного файла.")
            return
        df = add_height_column(df)
        print(f"Загружено изображений: {len(df)}")

        sorted_df = sort_by_height(df)
        filtered_df = filter_by_height(sorted_df, min_height, max_height)
        print(f"Длина от {min_height} до {max_height}: ")
        print(f"{len(filtered_df)} изображений")
        print(filtered_df[["relative_path", "height"]].to_string(index=False))

        sorted_df.to_csv(output_csv_path, index=False)
        print(f"Таблица сохранена: {output_csv_path}")

        plot_histogram(sorted_df, output_plot_path)
        print(f"График сохранён: {output_plot_path}")

    except ValueError as exc:
        print(f"Ошибка: {exc}")
    except OSError as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    args = parse_arguments()
    main(
        annotation_path=args.annotation,
        output_csv_path=args.output_csv,
        output_plot_path=args.output_plot,
        min_height=args.min_height,
        max_height=args.max_height,
    )
