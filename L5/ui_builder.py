from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QWidget, QLabel, QFormLayout
)
from PySide6.QtCore import Qt

# Константы
BUTTON_HEIGHT = 40
LINE_EDIT_WIDTH = 200
LABEL_STYLE = "font-size: 16px; font-weight: bold; margin-bottom: 5px;"


class UIBuilder:
    """Класс для настройки интерфейса главного окна."""

    def setup_ui(self, main_window: QWidget) -> None:
        """Настраивает пользовательский интерфейс главного окна."""
        main_window.setCentralWidget(self._create_central_widget())

    def _create_central_widget(self) -> QWidget:
        """Создает центральный виджет с основным макетом."""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignTop)

        groups = [
            ("Выбор папки", self._create_folder_selection),
            ("Диапазон дат", self._create_date_input),
            ("Ввод месяца", self._create_month_input),
            ("Действия", self._create_action_buttons),
        ]

        for title, layout_func in groups:
            main_layout.addLayout(self._create_group(title, layout_func()))

        return central_widget

    def _create_group(self, title: str, layout: QVBoxLayout) -> QVBoxLayout:
        """Создает группу элементов с заголовком."""
        group_layout = QVBoxLayout()
        group_label = QLabel(title)
        group_label.setStyleSheet(LABEL_STYLE)
        group_layout.addWidget(group_label)
        group_layout.addLayout(layout)
        return group_layout

    def _create_folder_selection(self) -> QHBoxLayout:
        """Создает элементы для выбора папки."""
        layout = QHBoxLayout()
        self.select_folder_button = self._create_button("Выбрать папку", enabled=True)
        layout.addWidget(QLabel("Выберите папку с датасетом:"))
        layout.addWidget(self.select_folder_button)
        return layout

    def _create_date_input(self) -> QFormLayout:
        """Создает элементы ввода диапазона дат."""
        self.start_date_input = self._create_line_edit("Начальная дата (YYYY-MM-DD)")
        self.end_date_input = self._create_line_edit("Конечная дата (YYYY-MM-DD)")

        layout = QFormLayout()
        layout.addRow("Начальная дата:", self.start_date_input)
        layout.addRow("Конечная дата:", self.end_date_input)
        return layout

    def _create_month_input(self) -> QFormLayout:
        """Создает элементы для ввода месяца."""
        self.month_input = self._create_line_edit("Месяц (YYYY-MM)")
        layout = QFormLayout()
        layout.addRow("Месяц:", self.month_input)
        return layout

    def _create_action_buttons(self) -> QVBoxLayout:
        """Создает кнопки для выполнения операций."""
        button_configs = [
            ("Фильтровать по дате", "filter_date_button"),
            ("Фильтровать по отклонениям", "filter_deviation_button"),
            ("Построить график", "plot_graph_button"),
            ("Построить гистограмму", "plot_histogram_button"),
            ("Рассчитать месячные средние", "calculate_avg_button"),
            ("Показать статистику", "show_statistics_button"),
            ("Показать отклонения", "show_deviations_button"),
            ("Построить график за месяц", "plot_month_graph_button"),
        ]

        layout = QVBoxLayout()
        for label, attr_name in button_configs:
            button = self._create_button(label)
            setattr(self, attr_name, button)
            layout.addWidget(button)

        return layout

    @staticmethod
    def _create_button(text: str, enabled: bool = False) -> QPushButton:
        """Создает кнопку."""
        button = QPushButton(text)
        button.setMinimumHeight(BUTTON_HEIGHT)
        button.setEnabled(enabled)
        return button

    @staticmethod
    def _create_line_edit(placeholder: str) -> QLineEdit:
        """Создает поле ввода с заданным placeholder."""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setMinimumWidth(LINE_EDIT_WIDTH)
        return line_edit
