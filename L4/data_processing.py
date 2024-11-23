import pandas as pd

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
