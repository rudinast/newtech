import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO
from usd_analysis import (load_data, rename_columns, handle_invalid_values,
                         add_deviation_columns, filter_by_deviation, filter_by_date_range,
                         monthly_aggregation, plot_usd_distribution, plot_usd_trend,
                         plot_monthly_data)

class TestUSDAnalysis(unittest.TestCase):

    def setUp(self):
        # Пример данных для тестов
        self.data = StringIO("""дата;курс_usd
2024/01/01;75.5
2024/01/02;76.2
2024/01/03;invalid
2024/01/04;74.8
""")
        self.df = pd.read_csv(self.data, sep=';')

    def test_load_data(self):
        # Тестирование функции load_data
        df = load_data(self.data)
        self.assertIn('дата', df.columns)
        self.assertIn('курс_usd', df.columns)

    def test_rename_columns(self):
        # Тестирование переименования столбцов
        df = rename_columns(self.df)
        self.assertIn('дата', df.columns)
        self.assertIn('курс_usd', df.columns)

    def test_handle_invalid_values_correct_data(self):
        # Проверка обработки корректных данных
        df = handle_invalid_values(self.df, 'курс_usd')
        self.assertFalse(df['курс_usd'].isnull().all())
        self.assertEqual(df['курс_usd'].isnull().sum(), 0)

    def test_handle_invalid_values_all_nan(self):
        # Проверка случая, когда все значения NaN
        df = pd.DataFrame({'дата': ['2024/01/01', '2024/01/02'], 'курс_usd': ['invalid', 'invalid']})
        df = handle_invalid_values(df, 'курс_usd')
        self.assertTrue(df.empty)

    def test_add_deviation_columns_with_data(self):
        # Проверка добавления столбцов отклонений при корректных данных
        df = rename_columns(self.df)
        df = handle_invalid_values(df, 'курс_usd')
        df = add_deviation_columns(df, 'курс_usd')
        self.assertIn('отклонение_от_медианы', df.columns)
        self.assertIn('отклонение_от_среднего', df.columns)

    def test_add_deviation_columns_no_data(self):
        # Проверка добавления столбцов отклонений при пустом DataFrame
        df = pd.DataFrame({'дата': [], 'курс_usd': []})
        df = add_deviation_columns(df, 'курс_usd')
        self.assertNotIn('отклонение_от_медианы', df.columns)
        self.assertNotIn('отклонение_от_среднего', df.columns)

    def test_filter_by_deviation_positive(self):
        # Проверка фильтрации по отклонению
        df = rename_columns(self.df)
        df = handle_invalid_values(df, 'курс_usd')
        df = add_deviation_columns(df, 'курс_usd')
        filtered_df = filter_by_deviation(df, 'курс_usd', deviation=0.5)
        self.assertTrue(all(abs(filtered_df['отклонение_от_среднего']) >= 0.5))

    def test_filter_by_deviation_negative(self):
        # Проверка на неправильное значение deviation
        df = rename_columns(self.df)
        df = handle_invalid_values(df, 'курс_usd')
        df = add_deviation_columns(df, 'курс_usd')
        with self.assertRaises(ValueError):
            filter_by_deviation(df, 'курс_usd', deviation=-0.5)

    def test_filter_by_date_range_correct_dates(self):
        # Проверка фильтрации по корректному диапазону дат
        df = rename_columns(self.df)
        filtered_df = filter_by_date_range(df, "2024-01-01", "2024-01-03")
        self.assertEqual(len(filtered_df), 3)

    def test_filter_by_date_range_invalid_dates(self):
        # Проверка фильтрации с некорректными датами
        df = rename_columns(self.df)
        filtered_df = filter_by_date_range(df, "invalid-date", "another-invalid-date")
        self.assertTrue(filtered_df.empty)

    def test_monthly_aggregation_with_data(self):
        # Проверка группировки по месяцу с данными
        df = rename_columns(self.df)
        df = handle_invalid_values(df, 'курс_usd')
        monthly_avg = monthly_aggregation(df, 'курс_usd')
        self.assertIsInstance(monthly_avg, pd.Series)
        self.assertEqual(monthly_avg.index[0], pd.Period("2024-01", freq="M"))

    def test_monthly_aggregation_no_date_column(self):
        # Проверка группировки по месяцу без столбца даты
        df = pd.DataFrame({'курс_usd': [74.5, 75.0, 76.2]})
        monthly_avg = monthly_aggregation(df, 'курс_usd')
        self.assertTrue(monthly_avg.empty)

    def test_plot_functions_no_data(self):
        # Проверка, что функции визуализации не вызывают ошибок при пустом DataFrame
        df = pd.DataFrame({'дата': [], 'курс_usd': []})
        try:
            plot_usd_distribution(df, 'курс_usd')
            plot_usd_trend(df, 'курс_usd')
            plot_monthly_data(df, "2024-01", 'курс_usd')
        except Exception as e:
            self.fail(f"Визуализация вызвала исключение на пустых данных: {e}")

    def test_plot_functions_with_data(self):
        # Проверка, что функции визуализации не вызывают ошибок при корректных данных
        df = rename_columns(self.df)
        df = handle_invalid_values(df, 'курс_usd')
        try:
            plot_usd_distribution(df, 'курс_usd')
            plot_usd_trend(df, 'курс_usd')
            plot_monthly_data(df, "2024-01", 'курс_usd')
        except Exception as e:
            self.fail(f"Визуализация вызвала исключение на корректных данных: {e}")

if __name__ == '__main__':
    unittest.main()
