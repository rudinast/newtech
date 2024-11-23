import pandas as pd
from analysis import calculate_monthly_average, add_deviation_columns
from visualization import plot_graph, plot_histogram
from data_processing import preprocess_column, filter_by_date_range, filter_by_deviation

def main(csv_path: str):
    """
    Основная функция анализа данных.

    :param csv_path: Путь к CSV-файлу с данными.
    """
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig')
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    df = preprocess_column(df, 'курс_usd')
    df = add_deviation_columns(df, 'курс_usd')

    # Вывод общей статистики
    print(df.describe())

    # Построение гистограммы
    plot_histogram(df, 'курс_usd', "Распределение курса USD", "Курс USD", "Частота")

    # Фильтрация и группировка
    filtered_df = filter_by_deviation(df, deviation=0.5)
    monthly_avg = calculate_monthly_average(df, 'курс_usd')

    # Построение графика изменения курса
    plot_graph(x='дата', y='курс_usd', data=df, title="Изменение курса USD", xlabel="Дата", ylabel="Курс USD")
    print(f"Средние значения по месяцам:\n{monthly_avg}")

    # График за конкретный месяц
    month_df = df[df['дата'].dt.to_period("M") == "2024-04"]
    plot_graph(x='дата', y='курс_usd', data=month_df, title="Курс USD за апрель 2024", xlabel="Дата", ylabel="Курс USD", mean=month_df['курс_usd'].mean(), median=month_df['курс_usd'].median())

if __name__ == "__main__":
    main("dataset_v3.csv")
