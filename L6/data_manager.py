import os
import pandas as pd
from typing import Optional
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Константы
DEFAULT_FILE_NAME = "dataset_v3.csv"
CSV_SEPARATOR = ";"
ENCODING = "utf-8-sig"
DATE_COLUMN = "дата"


class DataManager:
    """Класс для работы с данными."""

    def __init__(self, file_name: str = DEFAULT_FILE_NAME):
        self.file_name = file_name
        self.data = None

    def load_csv(self, folder: str) -> Optional[pd.DataFrame]:
        """Загружает данные из CSV-файла."""
        file_path = os.path.join(folder, self.file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")

        self.data = pd.read_csv(file_path, sep=CSV_SEPARATOR, encoding=ENCODING)
        self._normalize_columns()
        return self.data.copy()

    def _normalize_columns(self):
        """Приводит названия колонок к нижнему регистру с разделением слов через `_`."""
        if self.data is not None:
            self.data.columns = [col.lower().replace(" ", "_") for col in self.data.columns]

    def clean_column(self, column: str) -> pd.DataFrame:
        """Обрабатывает невалидные значения в указанном столбце."""
        if self.data is not None:
            df = self.data.copy()
            df[column] = pd.to_numeric(df[column], errors="coerce")
            if df[column].isnull().any():
                print(f"Найдено {df[column].isnull().sum()} невалидных значений в '{column}'.")
                df[column] = df[column].fillna(df[column].median())
            return df
        return pd.DataFrame()

    def add_deviations(self, column: str) -> pd.DataFrame:
        """Добавляет столбцы с отклонениями от медианы и среднего."""
        if self.data is not None and column in self.data:
            df = self.data.copy()
            df["median_dev"] = df[column] - df[column].median()
            df["mean_dev"] = df[column] - df[column].mean()
            return df
        return pd.DataFrame()

    def get_summary(self) -> pd.DataFrame:
        """Возвращает статистику данных."""
        if self.data is not None:
            return self.data.describe()
        return pd.DataFrame()

    def filter_by_deviation(self, threshold: float) -> pd.DataFrame:
        """Фильтрует строки по заданному отклонению от среднего."""
        if self.data is not None and "mean_dev" in self.data:
            df = self.data.copy()
            return df[abs(df["mean_dev"]) >= threshold]
        return pd.DataFrame()

    def filter_by_dates(self, start: str, end: str) -> pd.DataFrame:
        """Фильтрует строки по диапазону дат."""
        if self.data is not None and DATE_COLUMN in self.data:
            df = self.data.copy()
            df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
            start = pd.to_datetime(start)
            end = pd.to_datetime(end)
            return df[(df[DATE_COLUMN] >= start) & (df[DATE_COLUMN] <= end)]
        return pd.DataFrame()

    def group_by_month(self, column: str) -> pd.Series:
        """Группирует данные по месяцам и вычисляет среднее значение."""
        if self.data is not None and DATE_COLUMN in self.data:
            df = self.data.copy()
            df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
            df["month"] = df[DATE_COLUMN].dt.to_period("M")
            return df.groupby("month")[column].mean()
        return pd.Series(dtype=float)

    def calculate_monthly_average(self, column: str) -> pd.Series:
        """Рассчет среднего значения по месяцам."""
        if 'дата' not in self.data:
            print("Столбец 'дата' отсутствует.")
            return pd.Series(dtype=float)

        try:
            self.data['дата'] = pd.to_datetime(self.data['дата'], errors='coerce')
        except Exception as e:
            print(f"Ошибка преобразования столбца 'дата' в datetime: {e}")
            return pd.Series(dtype=float)

        if self.data['дата'].isnull().all():
            print("Все значения в столбце 'дата' некорректны.")
            return pd.Series(dtype=float)

        self.data['месяц'] = self.data['дата'].dt.to_period("M")
        return self.data.groupby('месяц')[column].mean()

    def get_classification_forecasting(self) -> pd.Series:
        try:
            df = self.data.copy()
            df['дата'] = pd.to_datetime(df['дата'])
            df.set_index('дата', inplace=True)
            df = df.sort_index()

            print("Разделяем на обучение и тест (80% / 20%)")
            split_index = int(len(df) * 0.8)
            train_df = df.iloc[:split_index]
            test_df = df.iloc[split_index:]

            model = SARIMAX(train_df['курс_usd'], order=(0, 0, 0), seasonal_order=(1, 1, 1, 30))
            result = model.fit()
            print(result.summary())

            forecast_test = result.forecast(steps=len(test_df))
            forecast_df = pd.DataFrame({'дата': test_df.index, 'прогноз': forecast_test})
            forecast_df.set_index('дата', inplace=True)

            mae = mean_absolute_error(test_df['курс_usd'], forecast_test)
            print(f'MAE: {mae:.2f}')
        except Exception as e:
            print(f"Ошибка прогноза: {e}")
            return pd.Series(dtype=float)
        return mae