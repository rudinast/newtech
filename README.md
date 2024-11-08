
# Currency Exchange Rate Projects

## Overview

This repository includes three Python-based projects focusing on currency exchange rate data processing. Each project builds upon the previous one, culminating in a GUI application for user-friendly interaction.

## Labs Summary

### Lab 1: Currency Rate Fetcher
Fetches daily USD exchange rates from the [Russian Central Bank](https://www.cbr-xml-daily.ru) for a specified number of days and saves them into a CSV file.

**Features**:
- Fetches and saves daily exchange rates.
- Handles missing data for non-working days.

### Lab 2: Data Processing Functions
Processes and organizes data collected in Lab 1. It includes scripts for splitting CSV files and retrieving data by date.

**Features**:
- Splits CSV data into `X.csv` (dates) and `Y.csv` (values).
- Creates yearly and weekly CSV files.
- Fetches data for specific dates.

### Lab 3: GUI Application
Adds a GUI using `PySide6` for interacting with data processing functions from Lab 2.

**Features**:
- Selects dataset folders and organizes data.
- Generates annotation files.
- Retrieves data by user-specified dates.

## Installation and Setup

**Requirements**:
- **Python 3.9+**
- **Dependencies**: `pandas`, `requests`, `PySide6`

### Installation
**Local**:
```bash
pip install -r requirements.txt
```

**Docker**:
1. Start the container:
    ```bash
    docker-compose up -d
    ```
2. Access the container:
    ```bash
    docker-compose exec python-app /bin/bash
    ```
3. Run the scripts:
    ```bash
    python <script_name.py>
    ```

## Usage

- **Lab 1**: Run `python main.py` to fetch and save exchange rates.
- **Lab 2**: Run `python main.py` to process CSV data.
- **Lab 3**: Run `python main_window.py` to launch the GUI application.

## Conclusion

These projects demonstrate data fetching, processing, and GUI integration for currency exchange rates, showcasing Python's capabilities in handling CSV data and building interactive applications.
