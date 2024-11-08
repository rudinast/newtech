
# Lab 3: GUI Application for Data Processing

## General Information

This lab extends the functionality from Lab 2 by adding a graphical user interface (GUI) using PySide6. The application allows users to interact with data processing functions through a user-friendly interface.

## Features

1. **Select Dataset Folder**: Allows the user to select the source folder for the dataset.
2. **Create Annotation File**: Generates an annotation file from the source dataset and saves it to a specified location.
3. **Organize Dataset**: Splits the dataset by years and weeks, and saves the organized files to a user-specified folder.
4. **Retrieve Data by Date**: Allows the user to input a date and display the data for that date if available.

## Project Structure

- `main_window.py` — The main script that implements the GUI interface.
- `split_columns.py` — Splits the CSV into `X.csv` (dates) and `Y.csv` (data).
- `split_by_year.py` — Splits the CSV into yearly files.
- `split_by_week.py` — Splits the CSV into weekly files.
- `get_data_by_date.py` — Retrieves data for a specific date.
- `manage_data.py` — Contains helper functions for loading and managing CSV data.
- `requirements.txt` — Specifies required library versions.

## System Requirements

- **Python Version**: This project is designed for Python 3.9 or newer.
- **Dependencies**:
  - `PySide6`: For building the GUI.
  - `pandas`: For data manipulation and CSV processing.

### Installation

**Without Docker**:

Ensure that Python 3.9 or newer and `pip` are installed on your system. Install the required libraries with:

```bash
pip install -r requirements.txt
```

**With Docker**:

Ensure `Docker` and `Docker Compose` are installed and properly configured.

To run the project using Docker Compose:

1. Build and start the container:

    ```bash
    docker-compose up -d
    ```

2. Access the running container:

    ```bash
    docker-compose exec python-app /bin/bash
    ```

3. Run the GUI application inside the container:

    ```bash
    python main_window.py
    ```

## Example Usage

1. **Select a folder** containing your dataset using the "Выбрать папку датасета" button.
2. **Create an annotation file** by clicking "Создать файл аннотации" and specifying the save location.
3. **Organize the dataset** by clicking "Организовать датасет и аннотацию" and choosing a destination folder.
4. **Retrieve data by date**:
   - Enter a date in `DD.MM.YYYY` format.
   - Click "Получить данные" to see the data for that date.

## Conclusion

This lab demonstrates how to integrate data processing functions into a GUI application using PySide6, enhancing the usability and interactivity of data handling tasks.
