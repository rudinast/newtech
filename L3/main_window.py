# main_window.py
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMainWindow, QFileDialog, QPushButton, QLineEdit, QLabel
import sys
import os

from split_columns import split_csv_by_columns
from split_by_year import split_dataset_by_years
from split_by_week import split_dataset_by_weeks
from get_data_by_date import get_data_by_date
from datetime import datetime
from manage_data import load_currency_data

CSV_SEP = ';'
CSV_ENCODING = 'utf-8-sig'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dataset Manager")
        self.setGeometry(300, 300, 400, 300)

        # Кнопка выбора папки исходного датасета
        self.select_folder_button = QPushButton("Выбрать папку датасета", self)
        self.select_folder_button.clicked.connect(self.select_folder)
        self.select_folder_button.setGeometry(50, 50, 300, 30)

        # Кнопка для создания файла аннотации исходного датасета
        self.create_annotation_button = QPushButton("Создать файл аннотации", self)
        self.create_annotation_button.clicked.connect(self.create_annotation)
        self.create_annotation_button.setGeometry(50, 90, 300, 30)

        # Кнопка для создания датасета с новой организацией
        self.organize_dataset_button = QPushButton("Организовать датасет и аннотацию", self)
        self.organize_dataset_button.clicked.connect(self.organize_dataset)
        self.organize_dataset_button.setGeometry(50, 130, 300, 30)

        # Поле ввода и кнопка для получения данных по дате
        self.date_label = QLabel("Введите дату (DD.MM.YYYY):", self)
        self.date_label.setGeometry(50, 180, 200, 20)
        self.date_input = QLineEdit(self)
        self.date_input.setGeometry(50, 200, 200, 30)

        self.get_data_button = QPushButton("Получить данные", self)
        self.get_data_button.clicked.connect(self.fetch_data_by_date)
        self.get_data_button.setGeometry(260, 200, 90, 30)

    def select_folder(self):
        self.dataset_folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if self.dataset_folder:
            print(f"Selected folder: {self.dataset_folder}")

    def create_annotation(self):
        if not hasattr(self, 'dataset_folder'):
            print("Please select a dataset folder first.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Annotation File")
        if file_path:
            # Вызов функции split_csv_by_columns и сохранение
            split_csv_by_columns(os.path.join(self.dataset_folder, "dataset_v3.csv"))
            print(f"Annotation file saved at: {file_path}")

    def organize_dataset(self):
        if not hasattr(self, 'dataset_folder'):
            print("Please select a dataset folder first.")
            return

        destination_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if destination_folder:
            # Вызов функций для организации датасета
            split_dataset_by_years(os.path.join(self.dataset_folder, "dataset_v3.csv"), destination_folder)
            split_dataset_by_weeks(os.path.join(self.dataset_folder, "dataset_v3.csv"), destination_folder)
            print(f"Dataset organized in folder: {destination_folder}")

    def fetch_data_by_date(self):
        if not hasattr(self, 'dataset_folder') or not self.dataset_folder:
            print("Please select a dataset folder first.")
            return

        date_str = self.date_input.text()
        try:
            target_date = datetime.strptime(date_str, '%d.%m.%Y')
            # Загрузим данные из уже разделенных файлов или словаря
            currency_data = load_currency_data(os.path.join(self.dataset_folder, "dataset_v3.csv"))
            result = get_data_by_date(currency_data, target_date)
            if result is not None:
                print(f"Data for {date_str}: {result}")
            else:
                print(f"No data for {date_str}")
        except ValueError:
            print("Please enter a valid date in DD.MM.YYYY format.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
