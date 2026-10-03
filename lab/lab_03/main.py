import argparse

from src.io import read_image, write_image
from src.plot import show_images
from src.transforms import crop, overlay, rotate


def parse_arguments() -> argparse.Namespace:
    """Разобрать и проверить аргументы командной строки.

    :return: объект с валидированными путями к файлам и параметрами
    """
    parser = argparse.ArgumentParser(description="Преобразование изображения.")
    parser.add_argument("image", type=str, help="исходное изображение")
    parser.add_argument("overlay", type=str, help="накладываемое изображение")
    parser.add_argument("output", type=str, help="файл для результата")
    parser.add_argument("--width", type=int, required=True, help="ширина")
    parser.add_argument("--height", type=int, required=True, help="высота")
    parser.add_argument(
        "--angle",
        type=float,
        required=True,
        help="угол поворота в градусах, против часовой стрелки",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.5,
        help="непрозрачность накладываемого изображения, от 0 до 1",
    )
    args = parser.parse_args()

    if args.width < 1 or args.height < 1:
        parser.error("ширина и высота должны быть не меньше 1")
    if not 0.0 <= args.alpha <= 1.0:
        parser.error("непрозрачность должна быть от 0 до 1")

    return args


def main() -> None:
    args = parse_arguments()

    try:
        image = read_image(args.image)
        overlay_image = read_image(args.overlay)
        height, width, channels = image.shape
        ov_height, ov_width, ov_channels = overlay_image.shape

        print(f"Исходное изображение: {args.image}")
        print(f"Размер изображения: {width}x{height}, каналов: {channels}")
        print(f"Накладываемое изображение: {args.overlay}")
        print(f"Размер наложения: {ov_width}x{ov_height}, каналов: {ov_channels}")

        cropped = crop(image, args.width, args.height)
        rotated = rotate(cropped, args.angle)
        result = overlay(rotated, overlay_image, args.alpha)

        write_image(args.output, result)
        print(f"Результат сохранён: {args.output}")

        images_to_plot = {
            "Исходное": image,
            "Обрезка": cropped,
            "Поворот": rotated,
            "Наложение": result,
        }

        show_images(images_to_plot)

    except ValueError as exc:
        print(f"Ошибка: {exc}")
    except OSError as exc:
        print(f"Ошибка при работе с файлом: {exc}")


if __name__ == "__main__":
    main()
