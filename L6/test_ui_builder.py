import pytest
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_builder import UIBuilder


@pytest.fixture
def main_window():
    """Фикстура для создания экземпляра главного окна."""
    app = QApplication([])
    main_window = QMainWindow()
    ui = UIBuilder()
    ui.setup_ui(main_window)
    return main_window


def test_setup_ui_positive(main_window):
    """Проверка, что UI был настроен корректно."""
    central_widget = main_window.centralWidget()
    assert central_widget is not None, "Центральный виджет не установлен."
    assert central_widget.layout() is not None, "Макет центрального виджета отсутствует."


def test_folder_selection_group(main_window):
    """Проверка группы выбора папки."""
    folder_group = main_window.centralWidget().layout().itemAt(0).layout()
    assert folder_group is not None, "Группа выбора папки отсутствует."

    label = folder_group.itemAt(0).widget()
    button = folder_group.itemAt(1).widget()

    assert label.text() == "Выберите папку с датасетом:", "Неверный текст метки выбора папки."
    assert button.text() == "Выбрать папку", "Неверный текст кнопки выбора папки."


def test_date_input_group(main_window):
    """Проверка группы ввода диапазона дат."""
    date_group = main_window.centralWidget().layout().itemAt(1).layout()
    assert date_group is not None, "Группа ввода дат отсутствует."

    start_date_input = date_group.itemAt(0, 1).widget()
    end_date_input = date_group.itemAt(1, 1).widget()

    assert start_date_input.placeholderText() == "Начальная дата (YYYY-MM-DD)", "Неверный текст плейсхолдера для начальной даты."
    assert end_date_input.placeholderText() == "Конечная дата (YYYY-MM-DD)", "Неверный текст плейсхолдера для конечной даты."


def test_action_buttons_group(main_window):
    """Проверка группы кнопок действий."""
    actions_group = main_window.centralWidget().layout().itemAt(2).layout()
    assert actions_group is not None, "Группа действий отсутствует."

    buttons = [
        ("Фильтровать по дате", "filter_date_button"),
        ("Фильтровать по отклонениям", "filter_deviation_button"),
        ("Построить график", "plot_graph_button"),
        ("Построить гистограмму", "plot_histogram_button"),
        ("Рассчитать месячные средние", "calculate_avg_button"),
        ("Показать статистику", "show_statistics_button"),
        ("Показать отклонения", "show_deviations_button"),
    ]

    for index, (label, attr_name) in enumerate(buttons):
        button = actions_group.itemAt(index).widget()
        assert button.text() == label, f"Текст кнопки '{attr_name}' не соответствует ожидаемому."
