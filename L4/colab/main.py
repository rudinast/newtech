import pandas as pd
import matplotlib.pyplot as plt


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
    plt.hist(data[column], bins=bins, color='blue', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


def filter_by_deviation(df: pd.DataFrame, deviation: float) -> pd.DataFrame:
    """
    Фильтрация строк DataFrame по отклонению от среднего значения.

    :param df: Исходный DataFrame.
    :param deviation: Минимальное отклонение для фильтрации.
    :return: Отфильтрованный DataFrame.
    """
    if 'отклонение_от_среднего' not in df:
        print("Столбец 'отклонение_от_среднего' отсутствует.")
        return pd.DataFrame()
    return df[abs(df['отклонение_от_среднего']) >= deviation]


def filter_by_date_range(
    df: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Фильтрация строк DataFrame по диапазону дат.

    :param df: Исходный DataFrame.
    :param start_date: Начальная дата (YYYY-MM-DD).
    :param end_date: Конечная дата (YYYY-MM-DD).
    :return: Отфильтрованный DataFrame.
    """
    try:
        df['дата'] = pd.to_datetime(df['дата'], format='%Y/%m/%d')
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    except Exception as e:
        print(f"Ошибка преобразования даты: {e}")
        return pd.DataFrame()

    return df[(df['дата'] >= start_date) & (df['дата'] <= end_date)]


def calculate_monthly_average(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Рассчет среднего значения по месяцам.

    :param df: Исходный DataFrame.
    :param column: Название столбца для расчета.
    :return: Series со средними значениями по месяцам.
    """
    if 'дата' not in df:
        print("Столбец 'дата' отсутствует.")
        return pd.Series(dtype=float)

    try:
        df['дата'] = pd.to_datetime(df['дата'], errors='coerce')
    except Exception as e:
        print(f"Ошибка преобразования столбца 'дата' в datetime: {e}")
        return pd.Series(dtype=float)

    if df['дата'].isnull().all():
        print("Все значения в столбце 'дата' некорректны.")
        return pd.Series(dtype=float)

    df['месяц'] = df['дата'].dt.to_period("M")
    return df.groupby('месяц')[column].mean()


def preprocess_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Преобразование и заполнение пропущенных значений в столбце.

    :param df: Исходный DataFrame.
    :param column: Название столбца для обработки.
    :return: Обработанный DataFrame.
    """
    df[column] = pd.to_numeric(df[column], errors='coerce')
    if df[column].isnull().all():
        print(f"Все значения в столбце '{column}' некорректны.")
        return df
    df[column] = df[column].fillna(df[column].median())
    return df


def add_deviation_columns(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Добавление столбцов с отклонениями от медианы и среднего.

    :param df: Исходный DataFrame.
    :param column: Название столбца для расчетов.
    :return: DataFrame с добавленными столбцами.
    """
    if column not in df or df[column].isnull().all():
        print(f"Столбец '{column}' пуст или отсутствует.")
        return df
    df['отклонение_от_медианы'] = df[column] - df[column].median()
    df['отклонение_от_среднего'] = df[column] - df[column].mean()
    return df


def main(csv_path: str) -> None:
    """
    Основная функция для анализа данных и визуализации.

    :param csv_path: Путь к CSV файлу.
    """
    # Загрузка данных
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig')

    # Переименование столбцов
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    # Обработка данных
    df = preprocess_column(df, 'курс_usd')
    df = add_deviation_columns(df, 'курс_usd')

    # Вывод описательной статистики и гистограмма
    print(df.describe())
    plot_histogram(df, 'курс_usd', "Распределение курса USD", "Курс USD", "Частота")

    # Фильтрация данных
    filtered_df = filter_by_deviation(df, deviation=0.5)
    filtered_date_df = filter_by_date_range(df, "2023-01-01", "2023-12-31")

    # Группировка данных
    monthly_avg = calculate_monthly_average(df, 'курс_usd')

    # Построение графиков
    plot_graph(
        x='дата',
        y='курс_usd',
        data=df,
        title="Изменение курса USD за весь период",
        xlabel="Дата",
        ylabel="Курс USD"
    )

    # График за конкретный месяц
    month_df = df[df['дата'].dt.to_period("M") == "2024-04"]
    plot_graph(
        x='дата',
        y='курс_usd',
        data=month_df,
        title="Курс USD за апрель 2024",
        xlabel="Дата",
        ylabel="Курс USD",
        mean=month_df['курс_usd'].mean(),
        median=month_df['курс_usd'].median()
    )


if __name__ == "__main__":
    main("../dataset_v3.csv")