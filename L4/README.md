
# USD Analysis Tool

## Overview

This project analyzes USD exchange rate data, providing tools for preprocessing, visualization, and statistical analysis. The project uses Python, Pandas, and Matplotlib for efficient data handling and visualization.

---

## Features

1. **Data Preprocessing**:
   - Handles missing values by replacing them with the median.
   - Adds deviation columns for more in-depth analysis.

2. **Visualization**:
   - Line plots, histograms, and scatter plots for detailed insights.
   - Highlights mean and median values.

3. **Statistical Analysis**:
   - Monthly averages of the USD exchange rate.
   - Filters data by deviation thresholds and date ranges.

---

## Setup Instructions

### Local Environment (Without Docker)

1. Ensure Python 3.9 or later is installed on your system.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Using Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```
2. Start the container:
   ```bash
   docker-compose up -d
   ```
3. Access the container:
   ```bash
   docker-compose exec python-app /bin/bash
   ```
4. Run the application:
   ```bash
   python main.py
   ```

---

## File Structure

- `analysis.py` - Functions for statistical analysis.
- `visualization.py` - Functions for data visualization.
- `data_processing.py` - Functions for preprocessing and filtering data.
- `main.py` - Entry point for the application.
- `colab/` - Contains a single file with all the code for easy testing in [Google Colab](https://colab.research.google.com/).

---

## Example Usage

### Plot a Graph
Example of visualizing USD exchange rates over time:
```python
from visualization import plot_graph

plot_graph(
    x='дата',
    y='курс_usd',
    data=dataframe,
    title="USD Exchange Rate Over Time",
    xlabel="Date",
    ylabel="Exchange Rate"
)
```

---

## Future Enhancements

1. Integrate with a GUI application for better user experience.
2. Add export options for graphs and filtered datasets.
3. Include more advanced statistical analysis and machine learning models.
