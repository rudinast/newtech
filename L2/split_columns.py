import os
import pandas as pd

# Константы
CSV_SEP = ';'
CSV_ENCODING = 'utf-8-sig'
OUTPUT_DIRECTORY = 'Lab_2_tmpFiles'

def create_directory(directory_name: str) -> None:
    """Создает директорию, если она не существует."""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def load_csv(filename: str) -> pd.DataFrame:
    """Загружает CSV файл и возвращает DataFrame."""
    return pd.read_csv(filename, sep=CSV_SEP, encoding=CSV_ENCODING)

def split_csv_by_columns(input_filename: str, output_directory: str = OUTPUT_DIRECTORY) -> None:
    """
    Разбивает CSV-файл на два файла: X.csv (содержит даты) и Y.csv (содержит данные).

    :param input_filename: Путь к исходному файлу CSV.
    :param output_directory: Путь к директории для сохранения результатов.
    """
    create_directory(output_directory)

    df = load_csv(input_filename)

    if 'Дата' not in df.columns or len(df.columns) != 2:
        raise ValueError("Файл должен содержать ровно две колонки: 'Дата' и 'Курс USD'.")

    output_dates = os.path.join(output_directory, 'X.csv')
    df[['Дата']].to_csv(output_dates, sep=CSV_SEP, index=False, encoding=CSV_ENCODING)

    output_values = os.path.join(output_directory, 'Y.csv')
    df[['Курс USD']].to_csv(output_values, sep=CSV_SEP, index=False, encoding=CSV_ENCODING)
