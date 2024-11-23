import matplotlib.pyplot as plt
import pandas as pd

def plot_graph(
    x: str, y: str, data: pd.DataFrame, title: str,
    xlabel: str, ylabel: str, kind: str = "line", **kwargs
) -> None:
    """
    Построение графиков.

    :param x: Название столбца для оси X.
    :param y: Название столбца или список столбцов для оси Y.
    :param data: DataFrame с данными.
    :param title: Заголовок графика.
    :param xlabel: Метка оси X.
    :param ylabel: Метка оси Y.
    :param kind: Тип графика ('line', 'bar', 'scatter').
    :param kwargs: Дополнительные параметры для настройки графика.
    """
    plt.figure(figsize=kwargs.get("figsize", (10, 6)))

    if kind == "line":
        plt.plot(data[x], data[y], label=kwargs.get("label", y),
                 linestyle=kwargs.get("linestyle", "-"))
    elif kind == "bar":
        plt.bar(data[x], data[y], label=kwargs.get("label", y))
    elif kind == "scatter":
        plt.scatter(data[x], data[y], label=kwargs.get("label", y))
    else:
        print(f"Unsupported plot kind: {kind}")
        return

    if "mean" in kwargs:
        plt.axhline(kwargs["mean"], color='red', linestyle='--', label="Среднее")
    if "median" in kwargs:
        plt.axhline(kwargs["median"], color='green', linestyle='--', label="Медиана")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_histogram(
    data: pd.DataFrame, column: str, title: str,
    xlabel: str, ylabel: str, bins: int = 30
) -> None:
    """
    Построение гистограммы.

    :param data: DataFrame с данными.
    :param column: Название столбца для построения гистограммы.
    :param title: Заголовок графика.
    :param xlabel: Метка оси X.
    :param ylabel: Метка оси Y.
    :param bins: Количество бинов.
    """
    plt.figure(figsize=(8, 6))
    plt.hist(data[column], bins=bins, color="blue", edgecolor="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()
