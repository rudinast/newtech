# Connect to the database
import sqlite3

def execute_query(db_name, query_name, change_data: bool):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Read the SQL query from file
    with open(query_name, "r", encoding="utf-8") as file:
        query = file.read().strip()

    # Execute the query
    cursor.execute(query)
    if change_data:
        conn.commit()
        print(f"Data Changed for SQL {query_name}!")
    else:
        # Fetch and print the results
        rows = cursor.fetchall()

        print(f"{query_name} SQL Query Result:")
        if len(rows) == 0:
            print("No data was found!")
        else:
            for row in rows:
                print(row)

    # Clean up
    conn.close()