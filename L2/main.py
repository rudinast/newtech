import os
from split_columns import split_csv_by_columns
from split_by_year import split_dataset_by_years
from split_by_week import split_dataset_by_weeks
from get_data_by_date import get_data_by_date
from datetime import datetime
from http import HTTPStatus

# Константы
DATA_DIR = "/data"
FILENAME = "dataset_v3.csv"
CSV_PATH = os.path.join(DATA_DIR, FILENAME)
CSV_SEP = ';'
CSV_ENCODING = 'utf-8-sig'
DAYS_IN_YEAR = 365  # Количество дней для парсинга
BASE_URL = "https://www.cbr-xml-daily.ru/archive/"
CURRENCY_CODE = 'USD'  # Код валюты

# Словарь основных кодов состояния HTTP
HTTP_STATUS_MESSAGES = {
    HTTPStatus.OK: "Успешно",
    HTTPStatus.BAD_REQUEST: "Неверный запрос",
    HTTPStatus.UNAUTHORIZED: "Не авторизован",
    HTTPStatus.FORBIDDEN: "Запрещено",
    HTTPStatus.NOT_FOUND: "Не найдено",
    HTTPStatus.INTERNAL_SERVER_ERROR: "Внутренняя ошибка сервера",
}


def main() -> None:
    """
    Основная функция, которая запускает выполнение всех этапов.
    """
    # 1. Разбиваем исходный CSV-файл на два файла: X.csv (даты) и Y.csv (данные)
    split_csv_by_columns(CSV_PATH)
    print("Файлы X.csv и Y.csv успешно созданы в директории Lab_2_tmpFiles.")

    # 2. Разбиваем файл на несколько файлов по годам
    split_dataset_by_years(CSV_PATH)
    print("Данные успешно разбиты по годам и сохранены в директории Lab_2_tmpFiles/Year.")

    # 3. Разбиваем файл на несколько файлов по неделям
    split_dataset_by_weeks(CSV_PATH)
    print("Данные успешно разбиты по неделям и сохранены в директории Lab_2_tmpFiles/Week.")

    # 4. Пример использования функции для получения данных по дате
    currency_data = {
        "2023-01-01": 74.5,
        "2023-01-02": None,
        "2023-01-03": 74.7,
        "2023-01-05": 75.0,
    }

    # Пример использования функции для конкретной даты
    example_date = datetime(2023, 1, 3)
    result = get_data_by_date(currency_data, example_date)
    print(f"Данные для {example_date}: {result}")


if __name__ == "__main__":
    main()
