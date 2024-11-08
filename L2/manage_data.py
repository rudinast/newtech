import os
import pandas as pd

CSV_SEP = ';'
CSV_ENCODING = 'utf-8-sig'

def load_csv(filename: str) -> pd.DataFrame:
    """Загружает CSV файл и возвращает DataFrame."""
    return pd.read_csv(filename, sep=CSV_SEP, encoding=CSV_ENCODING)

def load_currency_data(filename: str) -> dict:
    """
    Загрузка данных о валюте из CSV-файла и преобразование их в словарь.

    :param filename: Имя CSV-файла.
    :return: Словарь с датами и курсами валют.
    """
    df = load_csv(filename)
    df['Дата'] = pd.to_datetime(df['Дата']).dt.strftime('%Y-%m-%d')
    return dict(zip(df['Дата'], df['Курс USD']))

def create_directory(directory_name: str) -> None:
    """Создает директорию, если она не существует."""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)