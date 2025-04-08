import sqlite3
import os
import pandas as pd

# Database file
DB_FILE = "formula1.sqlite"
SCHEMA_FILE = "formula1_schema.sql"

# SQL schema
SCHEMA_SQL = """
CREATE TABLE circuits (
    circuitId INTEGER PRIMARY KEY AUTOINCREMENT,
    circuitRef TEXT,
    name TEXT,
    location TEXT,
    country TEXT,
    lat REAL,
    lng REAL,
    alt INTEGER,
    url TEXT
);

CREATE TABLE races (
    raceId INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    round INTEGER,
    circuitId INTEGER,
    name TEXT,
    date TEXT,
    time TEXT,
    url TEXT,
    FOREIGN KEY (circuitId) REFERENCES circuits(circuitId) ON DELETE CASCADE
);

CREATE TABLE drivers (
    driverId INTEGER PRIMARY KEY AUTOINCREMENT,
    driverRef TEXT,
    number INTEGER,
    code TEXT,
    forename TEXT,
    surname TEXT,
    dob TEXT,
    nationality TEXT,
    url TEXT
);

CREATE TABLE constructors (
    constructorId INTEGER PRIMARY KEY AUTOINCREMENT,
    constructorRef TEXT,
    name TEXT,
    nationality TEXT,
    url TEXT
);

CREATE TABLE results (
    resultId INTEGER PRIMARY KEY AUTOINCREMENT,
    raceId INTEGER,
    driverId INTEGER,
    constructorId INTEGER,
    number INTEGER,
    grid INTEGER,
    position INTEGER,
    positionText TEXT,
    positionOrder INTEGER,
    points REAL,
    laps INTEGER,
    time TEXT,
    milliseconds INTEGER,
    fastestLap INTEGER,
    rank INTEGER,
    fastestLapTime TEXT,
    fastestLapSpeed REAL,
    statusId INTEGER,
    FOREIGN KEY (raceId) REFERENCES races(raceId) ON DELETE CASCADE,
    FOREIGN KEY (driverId) REFERENCES drivers(driverId) ON DELETE CASCADE,
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId) ON DELETE CASCADE
);

CREATE TABLE pitstops (
    raceId INTEGER,
    driverId INTEGER,
    stop INTEGER,
    lap INTEGER,
    time TEXT,
    duration REAL,
    milliseconds INTEGER,
    PRIMARY KEY (raceId, driverId, stop),
    FOREIGN KEY (raceId) REFERENCES races(raceId) ON DELETE CASCADE,
    FOREIGN KEY (driverId) REFERENCES drivers(driverId) ON DELETE CASCADE
);

CREATE TABLE laptimes (
    raceId INTEGER,
    driverId INTEGER,
    lap INTEGER,
    position INTEGER,
    time TEXT,
    milliseconds INTEGER,
    PRIMARY KEY (raceId, driverId, lap),
    FOREIGN KEY (raceId) REFERENCES races(raceId) ON DELETE CASCADE,
    FOREIGN KEY (driverId) REFERENCES drivers(driverId) ON DELETE CASCADE
);

CREATE TABLE qualifying (
    qualifyId INTEGER PRIMARY KEY AUTOINCREMENT,
    raceId INTEGER,
    driverId INTEGER,
    constructorId INTEGER,
    number INTEGER,
    position INTEGER,
    q1 TEXT,
    q2 TEXT,
    q3 TEXT,
    FOREIGN KEY (raceId) REFERENCES races(raceId) ON DELETE CASCADE,
    FOREIGN KEY (driverId) REFERENCES drivers(driverId) ON DELETE CASCADE,
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId) ON DELETE CASCADE
);

CREATE TABLE constructor_standings (
    constructorStandingsId INTEGER PRIMARY KEY AUTOINCREMENT,
    raceId INTEGER,
    constructorId INTEGER,
    points REAL,
    position INTEGER,
    positionText TEXT,
    wins INTEGER,
    FOREIGN KEY (raceId) REFERENCES races(raceId) ON DELETE CASCADE,
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId) ON DELETE CASCADE
);

CREATE TABLE driver_standings (
    driverStandingsId INTEGER PRIMARY KEY AUTOINCREMENT,
    raceId INTEGER,
    driverId INTEGER,
    points REAL,
    position INTEGER,
    positionText TEXT,
    wins INTEGER,
    FOREIGN KEY (raceId) REFERENCES races(raceId) ON DELETE CASCADE,
    FOREIGN KEY (driverId) REFERENCES drivers(driverId) ON DELETE CASCADE
);

CREATE TABLE constructor_results (
    constructorResultsId INTEGER PRIMARY KEY AUTOINCREMENT,
    raceId INTEGER,
    constructorId INTEGER,
    points REAL,
    status TEXT,
    FOREIGN KEY (raceId) REFERENCES races(raceId) ON DELETE CASCADE,
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId) ON DELETE CASCADE
);

CREATE TABLE status (
    statusId INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT
);

CREATE TABLE seasons (
    year INTEGER PRIMARY KEY,
    url TEXT
);
"""


def save_schema():
    with open(SCHEMA_FILE, "w") as file:
        file.write(SCHEMA_SQL)
    print(f" Schema saved to '{SCHEMA_FILE}'.")


def create_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        cursor.executescript(schema_sql)
        conn.commit()
        conn.close()
        print(f" SQLite database '{DB_FILE}' created successfully!")
    except Exception as e:
        print(f" Error: {e}")


def load_csv_to_db(csv_folder):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for file in os.listdir(csv_folder):
        if file.endswith(".csv"):
            table_name = os.path.splitext(file)[0]
            file_path = os.path.join(csv_folder, file)

            try:
                df = pd.read_csv(file_path)
                df.to_sql(table_name, conn, if_exists="append", index=False)
                print(f" Data loaded into '{table_name}' from {file}")
            except Exception as e:
                print(f" Failed to load {file}: {e}")

    conn.close()
