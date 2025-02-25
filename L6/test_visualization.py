
import pytest
import pandas as pd
from visualization import plot_graph, plot_histogram

# Позитивный сценарий
def test_plot_graph_positive():
    data = {
        "дата": ["2023-01-01", "2023-01-02"],
        "курс_usd": [70, 72],
    }
    df = pd.DataFrame(data)
    try:
        plot_graph("дата", "курс_usd", df, "Test Plot", "Date", "USD Rate")
    except Exception:
        pytest.fail("plot_graph raised an unexpected exception!")

# Негативный сценарий: отсутствует столбец
def test_plot_graph_missing_column():
    data = {"другой_столбец": [70, 72]}
    df = pd.DataFrame(data)
    with pytest.raises(KeyError):
        plot_graph("дата", "курс_usd", df, "Test Plot", "Date", "USD Rate")

# Исключительный сценарий: некорректный тип данных
def test_plot_graph_invalid_data():
    data = {"дата": [None, None], "курс_usd": ["invalid", "data"]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError):
        plot_graph("дата", "курс_usd", df, "Test Plot", "Date", "USD Rate")

# Позитивный сценарий
def test_plot_histogram_positive():
    data = {"курс_usd": [70, 72, 75]}
    df = pd.DataFrame(data)
    try:
        plot_histogram(df, "курс_usd", "Test Histogram", "USD Rate", "Frequency")
    except Exception:
        pytest.fail("plot_histogram raised an unexpected exception!")

# Негативный сценарий: отсутствует столбец
def test_plot_histogram_missing_column():
    data = {"другой_столбец": [70, 72, 75]}
    df = pd.DataFrame(data)
    with pytest.raises(KeyError):
        plot_histogram(df, "курс_usd", "Test Histogram", "USD Rate", "Frequency")

# Исключительный сценарий: некорректный тип данных
def test_plot_histogram_invalid_data():
    data = {"курс_usд": ["NaN", None, ""]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError):
        plot_histogram(df, "курс_usд", "Test Histogram", "USD Rate", "Frequency")
