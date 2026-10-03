import numpy as np
import matplotlib.pyplot as plt


def show_images(images: dict[str, np.ndarray]) -> None:
    """Показать изображения в одном окне, в ряд и сохранить в файл.

    :param images: словарь [подпись, массив изображения]
    :return: None
    """
    plt.figure(figsize=(3 * len(images), len(images)))

    for i, (title, image) in enumerate(images.items(), start=1):
        plt.subplot(1, len(images), i)
        plt.imshow(image)
        plt.title(f"{title}\n{image.shape[1]}x{image.shape[0]}")
        plt.axis("off")

    plt.savefig("output.png")
    # plt.show()
