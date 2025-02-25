
# Currency Exchange Rate Projects

## Overview

This repository includes five Python-based projects that progressively build a comprehensive pipeline for currency exchange rate data processing, analysis, visualization, testing, deployment, and user-friendly interaction through a GUI application.

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

### Lab 4: USD Analysis Tool
Analyzes USD exchange rate data, providing tools for preprocessing, visualization, and statistical analysis.

**Features**:
1. **Data Preprocessing**:
   - Handles missing values by replacing them with the median.
   - Adds deviation columns for more in-depth analysis.
2. **Visualization**:
   - Line plots, histograms, and scatter plots for detailed insights.
   - Highlights mean and median values.
3. **Statistical Analysis**:
   - Monthly averages of the USD exchange rate.
   - Filters data by deviation thresholds and date ranges.

### Lab 5: Testing, Deployment, and Documentation
Extends the USD analysis application with unit testing, multiple deployment options, and comprehensive documentation.

**Features**:
1. **Unit Testing**:
   - Positive, negative, and exceptional scenarios using `pytest`.
2. **Deployment**:
   - Local execution with Python or Docker.
   - `exe` generation for Windows using `pyqtdeploy`.
   - Easy execution with `.bat` scripts.
3. **Documentation**:
   - Detailed README and inline docstrings.
   - User guide and setup instructions.

### Lab 6: Data Analysis. Working with Model Download. Classification and Forecasting Task
Extends the USD analysis application with unit testing, multiple deployment options, and comprehensive documentation.

**Features**:
1. **Model training**:
   - Deviding data on forecast and test.
   - Training model.
2. **Using SARIMAX**
   - Using SARIMAX model for forecasting.
3. **Documantation**
   - Documenting results of changing SARIMAX hyperparameters.
   - Analyzing results for the best set of parameters.

## Installation and Setup

**Requirements**:
- **Python 3.9+**
- **Dependencies**: `pandas`, `requests`, `PySide6`, `matplotlib`, `statsmodels.tsa.statespace.sarimax`

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
- **Lab 4**: Run `python main.py` to analyze exchange rates, generate statistics, and visualize data.
- **Lab 5**: Execute `pytest` for unit tests, and use .bat scripts or Docker for deployment.

## Conclusion

These projects showcase Python's capabilities in data collection, processing, analysis, visualization, GUI integration, testing, and deployment providing a complete pipeline from raw exchange rate data to actionable insights and interactive tools.
