import sqlite3


def view_all_jobs():
    """Queries and prints all jobs from the database."""
    try:
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()

        # The SQL command to select all columns (*) from the jobs table
        select_all_sql = "SELECT * FROM jobs;"

        cursor.execute(select_all_sql)

        # Fetch all the results from the executed query
        all_rows = cursor.fetchall()

        print(f"--- Found {len(all_rows)} jobs in the database ---")

        # Loop through the list of rows (each row is a tuple) and print them
        for row in all_rows:
            print(row)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


# Run the function when the script is executed
if __name__ == "__main__":
    view_all_jobs()
