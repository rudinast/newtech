
import pytest
import pandas as pd
from analysis import calculate_monthly_average, add_deviation_columns

# Позитивный сценарий
def test_calculate_monthly_average_positive():
    data = {
        "дата": ["2023-01-01", "2023-01-02", "2023-02-01"],
        "курс_usd": [70, 72, 75],
    }
    df = pd.DataFrame(data)
    df["дата"] = pd.to_datetime(df["дата"])
    result = calculate_monthly_average(df, "курс_usd")
    assert result["2023-01"] == 71
    assert result["2023-02"] == 75

# Негативный сценарий: отсутствует столбец 'дата'
def test_calculate_monthly_average_missing_column():
    data = {"курс_usд": [70, 72]}
    df = pd.DataFrame(data)
    result = calculate_monthly_average(df, "курс_usд")
    assert result.empty

# Исключительный сценарий: некорректные даты
def test_calculate_monthly_average_invalid_dates():
    data = {"дата": ["invalid", "invalid"], "курс_usd": [70, 72]}
    df = pd.DataFrame(data)
    df["дата"] = pd.to_datetime(df["дата"], errors="coerce")
    result = calculate_monthly_average(df, "курс_usd")
    assert result.empty

# Позитивный сценарий
def test_add_deviation_columns_positive():
    data = {"курс_usd": [70, 72, 75]}
    df = pd.DataFrame(data)
    result = add_deviation_columns(df, "курс_usd")
    assert "отклонение_от_медианы" in result
    assert "отклонение_от_среднего" in result

# Негативный сценарий: столбец отсутствует
def test_add_deviation_columns_missing_column():
    data = {"другой_столбец": [70, 72, 75]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError):
        add_deviation_columns(df, "курс_usd")

# Исключительный сценарий: пустой DataFrame
def test_add_deviation_columns_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(ValueError):
        add_deviation_columns(df, "курс_usd")
