import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from ui_builder import UIBuilder
from data_manager import DataManager
from visualization import plot_graph, plot_histogram


class Main(QMainWindow, UIBuilder):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USD Analysis Tool")
        self.resize(800, 600)
        self.data_manager = DataManager()
        self.dataset_folder = None

        self.setup_ui(self)
        self._connect_signals()

    def _connect_signals(self):
        """Подключение сигналов кнопок к соответствующим методам."""
        signals = {
            self.select_folder_button: self.select_folder,
            self.filter_date_button: self.filter_by_date,
            self.filter_deviation_button: self.filter_by_deviation,
            self.plot_graph_button: self.plot_graph,
            self.plot_histogram_button: self.plot_histogram,
            self.calculate_avg_button: self.calculate_monthly_avg,
            self.show_statistics_button: self.show_statistics,
            self.show_deviations_button: self.show_deviations,
            self.plot_month_graph_button: self.plot_month_graph,
        }

        for button, method in signals.items():
            button.clicked.connect(method)

    def select_folder(self):
        """Выбор папки с датасетом."""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с датасетом")
        if folder:
            self.dataset_folder = folder
            try:
                self.data_manager.load_csv(folder)
                self._enable_action_buttons()
                QMessageBox.information(self, "Успех", "Данные успешно загружены!")
            except FileNotFoundError as e:
                QMessageBox.critical(self, "Ошибка", str(e))
        else:
            QMessageBox.warning(self, "Ошибка", "Папка не выбрана!")

    def _enable_action_buttons(self):
        """Активирует кнопки действий после загрузки данных."""
        buttons = [
            self.filter_date_button,
            self.filter_deviation_button,
            self.plot_graph_button,
            self.plot_histogram_button,
            self.calculate_avg_button,
            self.show_statistics_button,
            self.show_deviations_button,
            self.plot_month_graph_button,
        ]
        for button in buttons:
            button.setEnabled(True)

    def filter_by_date(self):
        """Фильтрация данных по диапазону дат."""
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        try:
            filtered_data = self.data_manager.filter_by_dates(start_date, end_date)
            if filtered_data.empty:
                QMessageBox.warning(self, "Результат", "Нет данных для указанного диапазона.")
            else:
                QMessageBox.information(self, "Фильтрованные данные", str(filtered_data.head(10)))
        except Exception as e:
            self._show_error("Ошибка фильтрации", e)

    def filter_by_deviation(self):
        """Фильтрация данных по отклонениям."""
        try:
            threshold = 0.5  # Порог отклонения
            filtered_data = self.data_manager.filter_by_deviation(threshold)
            if filtered_data.empty:
                QMessageBox.warning(self, "Результат", "Нет данных с отклонением ≥ 0.5.")
            else:
                QMessageBox.information(self, "Фильтрованные данные", str(filtered_data.head(10)))
        except Exception as e:
            self._show_error("Ошибка фильтрации", e)

    def plot_graph(self):
        """Построение графика изменения курса."""
        try:
            df = self.data_manager.calculate_monthly_average('курс_usd')
            plot_graph(
                x="дата", y="курс_usd", data=self.data_manager.data,
                title="Изменение курса USD", xlabel="Дата", ylabel="Курс USD"
            )
        except Exception as e:
            self._show_error("Ошибка построения графика", e)

    def plot_histogram(self):
        """Построение гистограммы курса."""
        try:
            data = self.data_manager.data.copy()
            plot_histogram(
                data=data, column="курс_usd",
                title="Распределение курса USD", xlabel="Курс USD", ylabel="Частота"
            )
        except Exception as e:
            self._show_error("Ошибка построения гистограммы", e)

    def calculate_monthly_avg(self):
        """Расчет средних значений по месяцам."""
        try:
            avg_data = self.data_manager.group_by_month("курс_usd")
            QMessageBox.information(self, "Средние значения по месяцам", str(avg_data))
        except Exception as e:
            self._show_error("Ошибка расчета", e)

    def show_statistics(self):
        """Отображение общей статистики."""
        try:
            stats = self.data_manager.get_summary()
            if stats.empty:
                QMessageBox.warning(self, "Статистика", "Нет данных для отображения.")
            else:
                QMessageBox.information(self, "Статистика", str(stats))
        except Exception as e:
            self._show_error("Ошибка отображения статистики", e)

    def show_deviations(self):
        """Показ отклонений от медианы и среднего."""
        try:
            if self.data_manager.data is None:
                raise ValueError("Данные не загружены. Пожалуйста, выберите папку с датасетом.")

            data_with_deviations = self.data_manager.add_deviations("курс_usd")

            if data_with_deviations.empty:
                QMessageBox.warning(self, "Результат", "Нет данных для отображения отклонений.")
            else:
                deviations = data_with_deviations[["median_dev", "mean_dev"]]
                QMessageBox.information(self, "Отклонения", str(deviations.head(10)))
        except Exception as e:
            self._show_error("Ошибка отображения отклонений", e)

    def plot_month_graph(self):
        """Построение графика за указанный месяц."""
        try:
            if self.data_manager.data is None:
                raise ValueError("Данные не загружены. Пожалуйста, выберите папку с датасетом.")

            month = self.month_input.text()
            if not month:
                QMessageBox.warning(self, "Результат", "Пожалуйста, введите месяц в формате YYYY-MM.")
                raise ValueError("Пожалуйста, введите месяц в формате YYYY-MM.")

            data = self.data_manager.data.copy()
            data["дата"] = pd.to_datetime(data["дата"], errors="coerce")

            monthly_data = data[data["дата"].dt.to_period("M") == month]

            if monthly_data.empty:
                QMessageBox.warning(self, "Внимание", f"Данных за месяц {month} не найдено.")
                return

            plot_graph(
                x="дата",
                y="курс_usd",
                data=monthly_data,
                title=f"Курс USD за {month}",
                xlabel="Дата",
                ylabel="Курс USD",
                mean=monthly_data["курс_usd"].mean(),
                median=monthly_data["курс_usd"].median()
            )
        except Exception as e:
            self._show_error("Ошибка построения графика за месяц", e)

def main():
    """Точка входа в приложение."""
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
