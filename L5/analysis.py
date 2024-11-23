import pandas as pd


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
