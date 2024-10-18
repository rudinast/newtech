import os
import pandas as pd

# Константы
CSV_SEP = ';'
CSV_ENCODING = 'utf-8-sig'

def create_directory(directory_name: str) -> None:
    """Создает директорию, если она не существует."""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def load_csv(filename: str) -> pd.DataFrame:
    """Загружает CSV файл и возвращает DataFrame."""
    return pd.read_csv(filename, sep=CSV_SEP, encoding=CSV_ENCODING)

def split_dataset_by_weeks(input_filename: str, output_directory: str = 'Lab_2_tmpFiles/Week') -> None:
    """
    Разбивает исходный CSV-файл на файлы по неделям. Каждый файл содержит данные за одну неделю.

    :param input_filename: Путь к исходному файлу CSV.
    :param output_directory: Путь к директории для сохранения результатов.
    """
    create_directory(output_directory)

    df = load_csv(input_filename)
    df['Дата'] = pd.to_datetime(df['Дата'], errors='coerce')

    # Убираем строки с некорректными датами
    df = df.dropna(subset=['Дата'])

    df['Неделя'] = df['Дата'].dt.to_period('W').apply(lambda r: r.start_time)

    for week_start in df['Неделя'].unique():
        weekly_data = df[df['Неделя'] == week_start]
        start_date = weekly_data['Дата'].min().strftime('%Y%m%d')
        end_date = weekly_data['Дата'].max().strftime('%Y%m%d')
        output_filename = os.path.join(output_directory, f"week_{start_date}_{end_date}.csv")

        # Сохраняем файл
        weekly_data.to_csv(output_filename, sep=CSV_SEP, index=False, encoding=CSV_ENCODING)
