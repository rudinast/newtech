# Lab 5: Testing, Deployment, and Documentation

## General Information

This lab extends the USD analysis application with unit testing.

---

## Features

1. **Data Processing**:
   - Handling missing values.
   - Calculating deviations from median and mean.

2. **Visualization**:
   - Line graphs, histograms, and scatter plots.
   - Visual representation of statistical insights.

3. **Statistical Analysis**:
   - Monthly average calculations.
   - Filtering by deviation thresholds and date ranges.

4. **Testing**:
   - Positive, negative, and exceptional scenarios using `pytest`.

5. **Deployment**:
   - Local execution with Python or Docker.
   - `exe` generation for Windows using `pyqtdeploy`.

---

## System Requirements

- **Python Version**: 3.9 or newer.
- **Dependencies**:
  - `pandas`
  - `matplotlib`
  - `pytest`

---

## Installation and Usage

### Local Setup (Without Docker)

1. Ensure Python 3.9 or newer is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Docker Setup

1. Build and start the container:
   ```bash
   docker-compose up --build
   ```
2. Access the container:
   ```bash
   docker-compose exec python-app /bin/bash
   ```
3. Run the application inside the container:
   ```bash
   python main.py
   ```

---

### Deployment Options

#### 1. Local Execution with `.bat` Script
- Create a `run_app.bat` file with the following content:
  ```bat
  @echo off
  pip install -r requirements.txt
  python main.py
  pause
  ```
- Double-click `run_app.bat` to execute the application.

#### 2. Using `poetry`
1. Initialize and install dependencies:
   ```bash
   poetry init
   poetry add pandas matplotlib pytest
   ```
2. Create a `.bat` script for execution:
   ```bat
   @echo off
   poetry run python main.py
   pause
   ```

#### 3. Building an Executable with `pyqtdeploy`
1. Install `pyqtdeploy`:
   ```bash
   pip install pyqtdeploy
   ```
2. Create a spec file for `pyinstaller`:
   ```python
   from PyInstaller.__main__ import run

   options = [
       'main.py',
       '--onefile',
       '--noconsole',
       '--name=USDAnalysis',
   ]

   run(options)
   ```
3. Build the executable:
   ```bash
   pyinstaller main.spec
   ```

---

## Testing

Unit tests are provided for all major functionalities. The tests cover:

1. **Positive Scenarios**:
   - Expected inputs return correct results.
2. **Negative Scenarios**:
   - Invalid inputs (e.g., missing columns, wrong types) are handled gracefully.
3. **Exceptional Scenarios**:
   - Application provides meaningful error messages for unexpected errors.

### Running Tests
To execute the test suite, use:
```bash
pytest
```

---

## File Structure

- `analysis.py` — Functions for statistical analysis.
- `data_processing.py` — Data preprocessing and filtering.
- `visualization.py` — Data visualization.
- `main.py` — Entry point for the application.
- `tests/` — Contains unit tests.
- `requirements.txt` — Lists required dependencies.
- `Dockerfile` — Defines the Docker image.
- `docker-compose.yml` — Orchestrates Docker containers.
- `dataset.csv` — Sample dataset for testing.

---

## User Guide

1. **Input Data**:
   - The application works with CSV files containing at least two columns: `дата` and `курс_usd`.

2. **Functional Flow**:
   - Load the dataset.
   - Preprocess and calculate deviations.
   - Visualize trends and filter data based on user-defined criteria.

3. **Output**:
   - Graphs and filtered datasets.

4. **Limitations**:
   - Only supports CSV files with UTF-8 encoding.
   - Requires Python 3.9+ or Docker for execution.

---

## Conclusion

This project demonstrates:
- Robust data analysis and visualization.
- Comprehensive testing with `pytest`.
- Multiple deployment options, including Docker and standalone executables.

It serves as a practical example of combining Python’s capabilities with modern development practices.