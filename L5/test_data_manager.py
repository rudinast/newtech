import pytest
import pandas as pd
from data_manager import DataManager


@pytest.fixture
def data_manager():
    """Фикстура для создания экземпляра DataManager."""
    return DataManager()


def test_load_csv_positive(data_manager, tmp_path):
    """Проверка успешной загрузки CSV-файла."""
    file_path = tmp_path / "dataset_v3.csv"
    file_path.write_text("дата;курс_usd\n2023-01-01;70\n2023-01-02;72", encoding="utf-8-sig")

    df = data_manager.load_csv(str(tmp_path))
    assert not df.empty, "Данные из CSV-файла не были загружены."
    assert "дата" in df.columns, "Столбец 'дата' отсутствует."
    assert "курс_usd" in df.columns, "Столбец 'курс_usd' отсутствует."


def test_load_csv_missing_file(data_manager):
    """Проверка обработки ошибки при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        data_manager.load_csv("/nonexistent/path")


def test_clean_column(data_manager):
    """Проверка очистки и заполнения данных в столбце."""
    data_manager.data = pd.DataFrame({"курс_usd": ["70", "invalid", None]})
    cleaned_data = data_manager.clean_column("курс_usd")

    assert cleaned_data["курс_usd"].isnull().sum() == 0, "Пропущенные значения не были заполнены."
    assert cleaned_data["курс_usd"].dtype.kind in "fi", "Столбец не преобразован в числовой тип."


def test_add_deviations(data_manager):
    """Проверка добавления отклонений от медианы и среднего."""
    data_manager.data = pd.DataFrame({"курс_usd": [70, 72, 75]})
    deviations = data_manager.add_deviations("курс_usd")

    assert "median_dev" in deviations.columns, "Столбец 'median_dev' отсутствует."
    assert "mean_dev" in deviations.columns, "Столбец 'mean_dev' отсутствует."


def test_filter_by_deviation(data_manager):
    """Проверка фильтрации по отклонению."""
    data_manager.data = pd.DataFrame({"mean_dev": [0.5, 1.5, -0.2]})
    filtered_data = data_manager.filter_by_deviation(1.0)

    assert len(filtered_data) == 1, "Фильтрация по отклонению выполнена неверно."
    assert filtered_data.iloc[0]["mean_dev"] == 1.5, "Неверная строка после фильтрации."


def test_filter_by_dates(data_manager):
    """Проверка фильтрации по диапазону дат."""
    data_manager.data = pd.DataFrame({"дата": ["2023-01-01", "2023-01-02", "2023-02-01"]})
    filtered_data = data_manager.filter_by_dates("2023-01-01", "2023-01-31")

    assert len(filtered_data) == 2, "Фильтрация по диапазону дат выполнена неверно."


def test_group_by_month(data_manager):
    """Проверка группировки данных по месяцам."""
    data_manager.data = pd.DataFrame({"дата": ["2023-01-01", "2023-01-15", "2023-02-01"], "курс_usd": [70, 72, 75]})
    grouped_data = data_manager.group_by_month("курс_usd")

    assert grouped_data.loc["2023-01"] == 71.0, "Среднее значение за январь неверно."
    assert grouped_data.loc["2023-02"] == 75.0, "Среднее значение за февраль неверно."

def test_calculate_monthly_average_positive(data_manager):
    """Тест корректного расчета среднего значения по месяцам."""
    data = {
        "дата": ["2023-01-01", "2023-01-02", "2023-02-01"],
        "курс_usd": [70, 72, 75],
    }
    data_manager.data = pd.DataFrame(data)
    data_manager.data["дата"] = pd.to_datetime(data_manager.data["дата"])
    result = data_manager.group_by_month("курс_usd")
    assert result["2023-01"] == 71
    assert result["2023-02"] == 75

def test_calculate_monthly_average_missing_column(data_manager):
    """Тест на отсутствие необходимого столбца."""
    data = {"курс_usд": [70, 72]}
    data_manager.data = pd.DataFrame(data)
    result = data_manager.group_by_month("курс_usд")
    assert result.empty

def test_calculate_monthly_average_invalid_dates(data_manager):
    """Тест на некорректные даты в данных."""
    data = {"дата": ["invalid", "invalid"], "курс_usd": [70, 72]}
    data_manager.data = pd.DataFrame(data)
    data_manager.data["дата"] = pd.to_datetime(data_manager.data["дата"], errors="coerce")
    result = data_manager.group_by_month("курс_usd")
    assert result.empty
