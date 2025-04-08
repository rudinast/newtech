import sqlite_db_creation
import mongo_queries
import mongo_db_creation

from test_query import execute_query

CSV_FOLDER_PATH = "./csv_data"

GET_CIRCUIT_FRANCE = "./sql_queries/get_circuits_france.sql"
GET_OLDEST_DRIVERS = "./sql_queries/get_oldest_drivers.sql"
REMOVE_DRIVERS_NULL_CODE = "./sql_queries/remove_drivers_null_code.sql"
GET_FIRST_SEASON = "./sql_queries/get_first_season.sql"
ADD_NEW_SEASON = "./sql_queries/add_new_season.sql"
GET_RACES_EACH_YEAR = "./sql_queries/get_races_each_year.sql"
GET_RACES_RESULTS_FOR_YEAR = "./sql_queries/get_races_results_for_year.sql"
GET_DRIVER_MOST_POINTS = "./sql_queries/get_driver_most_points.sql"
REMOVE_NULL_RESULTS = "./sql_queries/remove_null_results.sql"
GET_FASTEST_PITSTOP = "./sql_queries/get_fastest_pitstop.sql"

def main():
    sqlite_part()
    mongo_part()

def sqlite_part():
    # Comment if DB is already created
    sqlite_db_creation.save_schema()
    sqlite_db_creation.create_database()
    sqlite_db_creation.load_csv_to_db(CSV_FOLDER_PATH)

    print("Database and schema setup complete! ")

    execute_query("formula1.sqlite", GET_CIRCUIT_FRANCE, False)
    execute_query("formula1.sqlite", REMOVE_DRIVERS_NULL_CODE, True)
    execute_query("formula1.sqlite", GET_OLDEST_DRIVERS, False)
    execute_query("formula1.sqlite", GET_FIRST_SEASON, False)
    execute_query("formula1.sqlite", ADD_NEW_SEASON, True)
    execute_query("formula1.sqlite", GET_RACES_EACH_YEAR, False)
    execute_query("formula1.sqlite", GET_RACES_RESULTS_FOR_YEAR, False)
    execute_query("formula1.sqlite", REMOVE_NULL_RESULTS, True)
    execute_query("formula1.sqlite", GET_DRIVER_MOST_POINTS, False)
    execute_query("formula1.sqlite", GET_FASTEST_PITSTOP, False)

def mongo_part():
    # Comment if DB is already created
    mongo_db_creation.create_mongo_db()

    mongo_queries.get_france_circuits(mongo_db_creation.MONGO_CLIENT,mongo_db_creation.DB_NAME)
    mongo_queries.remove_null_code_drivers(mongo_db_creation.MONGO_CLIENT,mongo_db_creation.DB_NAME)
    mongo_queries.get_oldest_drivers(mongo_db_creation.MONGO_CLIENT, mongo_db_creation.DB_NAME)
    mongo_queries.get_first_season(mongo_db_creation.MONGO_CLIENT, mongo_db_creation.DB_NAME)
    mongo_queries.add_new_season(mongo_db_creation.MONGO_CLIENT, mongo_db_creation.DB_NAME)
    mongo_queries.get_race_count_per_year(mongo_db_creation.MONGO_CLIENT, mongo_db_creation.DB_NAME)
    mongo_queries.get_race_results_for_year(mongo_db_creation.MONGO_CLIENT, mongo_db_creation.DB_NAME)
    mongo_queries.remove_null_results(mongo_db_creation.MONGO_CLIENT, mongo_db_creation.DB_NAME)
    mongo_queries.get_driver_with_most_points(mongo_db_creation.MONGO_CLIENT, mongo_db_creation.DB_NAME)
    mongo_queries.get_fastest_pitstop(mongo_db_creation.MONGO_CLIENT, mongo_db_creation.DB_NAME)

if __name__ == "__main__":
    main()