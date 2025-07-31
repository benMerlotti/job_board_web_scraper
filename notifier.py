import sqlite3


def fetch_new_jobs():
    connection = sqlite3.connect("jobs.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    find_new_jobs = """SELECT * FROM jobs WHERE is_notified = 0"""
    cursor.execute(find_new_jobs)

    new_jobs = cursor.fetchall()
    connection.close()
    return new_jobs


if __name__ == "__main__":
    jobs_to_notify = fetch_new_jobs()

    if jobs_to_notify:
        print(f"Found {len(jobs_to_notify)} new jobs to notify about:")
        for job in jobs_to_notify:
            # Because we used conn.row_factory, we can access columns by name!
            print(f"- {job['title']} at {job['company']}")
    else:
        print("No new jobs found.")
