import sqlite3

connection = sqlite3.connect("jobs.db")
cursor = connection.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE,
    experience TEXT,
    date_posted TEXT,
    location TEXT
);
"""

cursor.execute(create_table_sql)
connection.commit()
connection.close()

print("Database and 'jobs' table created successfully (if they didn't already exist).")
