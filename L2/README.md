# Lab 2: Implementing Data Processing Functions After Parsing

## General Information

This lab focuses on handling parsed data and working with CSV files using the `pandas` library. The goal is to process data from Lab 1 by splitting CSV files based on various criteria and retrieving data by date.

## Steps:

1. **Prepare CSV File**: If no CSV file with a file list and date was created in Lab 1, add it.
2. **Split into X.csv and Y.csv**: Write a script to split the original CSV file into two: `X.csv` (dates) and `Y.csv` (data).
3. **Split by Year**: Write a script to divide the CSV into yearly files, naming them by the first and last date they contain (e.g., `20010101_20011231.csv`).
4. **Split by Week**: Write a script to divide the CSV into weekly files, naming them similarly to the year-based files.
5. **Data by Date**: Implement a function that accepts a `datetime` object and returns the data for that date or `None` if the data is not available.

## Project Structure

- `main.py` — The main script that runs the entire workflow.
- `split_columns.py` — Splits the CSV into X.csv (dates) and Y.csv (data).
- `split_by_year.py` — Splits the CSV into yearly files.
- `split_by_week.py` — Splits the CSV into weekly files.
- `get_data_by_date.py` — Retrieves data for a specific date.
- `requirements.txt` — Specifies the required library versions.

## System Requirements

- **Python Version**: The project is designed for Python 3.9. You can adjust the Python version in Docker settings if necessary.
- **Dependencies**: The project uses the `requests` library for HTTP requests and `pandas` for data handling and CSV export.

### Without Docker

To run the project locally, ensure the following are installed on your system:

- **Python 3.9** or newer
- **Pip**: Python package installer
- **Required libraries**:
    - `requests`: For handling HTTP requests
    - `pandas`: For data processing and CSV export

You can install the required packages using:

```bash
pip install -r requirements.txt
```

### With Docker

If you prefer to use Docker, ensure the following are installed:

- **Docker**: Installed and properly configured
- **Docker Compose**: For managing multi-container Docker applications

To run the script using Docker Compose:

1. Start the application:

    ```bash
    docker-compose up -d
    ```

2. Access the running container:

    ```bash
    docker-compose exec python-app /bin/bash
    ```

3. Inside the container, run the script:

    ```bash
    python main.py
    ```

## Example Usage

```python
from datetime import datetime
from get_data_by_date import get_data_by_date

currency_data = {
    "2023-01-01": 74.5,
    "2023-01-02": None,
    "2023-01-03": 74.7,
    "2023-01-05": 75.0,
}

example_date = datetime(2023, 1, 3)
result = get_data_by_date(currency_data, example_date)
print(f"Data for {example_date}: {result}")
```

## Conclusion

This lab demonstrates how to implement data processing functions to handle large datasets and efficiently work with CSV files using `pandas`. It also reinforces skills in splitting and analyzing CSV data.
