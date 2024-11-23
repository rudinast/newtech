
import pytest
from main import main

# Позитивный сценарий
def test_main_positive(monkeypatch):
    # Mock input and test file setup
    def mock_input(_):
        return "test.csv"
    monkeypatch.setattr("builtins.input", mock_input)

    try:
        main("test.csv")
    except Exception:
        pytest.fail("main raised an unexpected exception!")

# Негативный сценарий: отсутствует файл
def test_main_missing_file():
    with pytest.raises(FileNotFoundError):
        main("non_existent_file.csv")

# Исключительный сценарий: некорректный формат файла
def test_main_invalid_file():
    with pytest.raises(ValueError):
        main("invalid_file.csv")
