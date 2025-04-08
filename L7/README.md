
# 🏎️ Formula 1 Data Analysis Project

## 📌 Description

This project is designed to analyze historical Formula 1 data using two database systems — SQLite and MongoDB. The system automatically creates databases, imports data from CSV/JSON, and runs a series of analytical queries using both SQL and MongoDB's Aggregation Framework.

## 🗂️ Project Structure

```
.
├── main.py                      # Main entry point: executes all project functions
├── sqlite_db_creation.py       # Creates schema and imports data into SQLite
├── mongo_db_creation.py        # Imports JSON data into MongoDB
├── mongo_queries.py            # MongoDB data analysis queries
├── test_query.py               # Executes SQL queries from files
├── sql_queries/                # SQL query files
│   ├── get_circuits_france.sql
│   ├── get_oldest_drivers.sql
│   ├── remove_drivers_null_code.sql
│   ├── get_first_season.sql
│   ├── add_new_season.sql
│   ├── get_races_each_year.sql
│   ├── get_races_results_for_year.sql
│   ├── get_driver_most_points.sql
│   ├── remove_null_results.sql
│   └── get_fastest_pitstop.sql
├── csv_data/                   # CSV files with data for SQLite
├── mongo_data.json             # JSON data for MongoDB
└── formula1_schema.sql         # SQL database schema
```

## ⚙️ Functionality

### 📄 SQLite Part
- Automatically creates the database schema (`formula1.sqlite`)
- Loads data from the `csv_data/` folder into corresponding tables
- Executes SQL queries:
  - Get circuits in France
  - Remove drivers without code
  - List oldest drivers
  - Get first season
  - Add new season
  - Count races per year
  - Get race results for a specific year
  - Remove null records in results
  - Driver with the most points
  - Fastest pit stop

### 🍃 MongoDB Part
- Imports data from `mongo_data.json` into MongoDB
- Mongo queries similar to SQL ones:
  - Find circuits in France
  - Remove drivers with null code
  - Find the oldest driver
  - Get the first season
  - Add a new season
  - Count races per year
  - Get race results for 2010
  - Remove null results
  - Find driver with the most points
  - Fastest pit stop

## 📊 Database Diagram
You can view the full database schema (SQLite) here:  
👉 [Formula 1 Schema on dbdiagram.io](https://dbdiagram.io/d/67eb3ba44f7afba184df7972)

## 🚀 How to Run

1. Install dependencies (if needed):
```bash
pip install pandas pymongo
```

2. Make sure:
   - **MongoDB** is installed and running locally (`localhost:27017`)
   - The `csv_data/` folder contains required `.csv` files
   - The `mongo_data.json` file is present in the project root

3. Run the main script:
```bash
python main.py
```

## 🧠 Notes

- You can comment out database creation in SQLite and Mongo if they are already created.
- All SQL and Mongo aggregation queries are organized in separate files and executed from `main.py`.
