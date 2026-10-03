import matplotlib.pyplot as plt
import pandas as pd

DARK_THEME = {
    "figure.facecolor": "#0d1117",
    "savefig.facecolor": "#0d1117",
    "axes.facecolor": "#161b22",
    "axes.edgecolor": "#30363d",
    "axes.labelcolor": "#c9d1d9",
    "axes.titlecolor": "#e6edf3",
    "xtick.color": "#c9d1d9",
    "ytick.color": "#c9d1d9",
    "grid.alpha": 0.3,
}


def plot_histogram(df: pd.DataFrame, plot_file: str) -> None:
    """
    Построить гистограмму длины изображений, сохранить и показать её.

    :param df: таблица с колонкой height
    :param plot_file: путь для сохранения графика
    """
    with plt.rc_context(DARK_THEME):
        plt.figure(figsize=(8, 5))
        plt.hist(df["height"], color="#3d7ef2")
        plt.title("Распределение длины изображений")
        plt.xlabel("Длина изображения, пикселей")
        plt.ylabel("Количество изображений")
        plt.grid(axis="y", linestyle="--")
        plt.tight_layout()
        plt.savefig(plot_file, dpi=300)
        plt.show()
