import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def fetch_new_jobs():
    connection = sqlite3.connect("jobs.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    find_new_jobs = """SELECT * FROM jobs WHERE is_notified = 0"""
    cursor.execute(find_new_jobs)

    new_jobs = cursor.fetchall()
    connection.close()
    return new_jobs


def format_jobs_for_email(jobs):
    """Formats a list of job objects into an HTML string for an email body."""
    if not jobs:
        return "<p>No new jobs found today.</p>"

    # Start the HTML string
    html_body = """
    <html>
    <head>
        <style>
            body { font-family: sans-serif; }
            li { margin-bottom: 12px; }
            a { color: #0066cc; }
        </style>
    </head>
    <body>
        <h2>New Job Listings Found!</h2>
        <ul>
    """

    # Add each job as a list item
    for job in jobs:
        # job['link'], job['title'], etc. are available because of our conn.row_factory
        html_body += f"""
        <li>
            <strong><a href="{job['link']}">{job['title']}</a></strong> at {job['company']}<br>
            <strong>Location:</strong> {job['location']}<br>
            <strong>Experience:</strong> {job['experience']}<br>
            <strong>Posted:</strong> {job['date_posted']}
        </li>
        """

    # Close the HTML tags
    html_body += """
        </ul>
    </body>
    </html>
    """

    return html_body


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, html_body, sender_email, receiver_email, sender_password):
    """Sends an email using Gmail's SMTP server."""

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the HTML body. We use MIMEText to specify it's HTML.
    message.attach(MIMEText(html_body, "html"))

    try:
        # Connect to the Gmail SMTP server
        # The server address is 'smtp.gmail.com' and the port for TLS is 587
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection

        # Log in to the server
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(message)

        # Close the connection
        server.quit()

        print(f"Email sent successfully to {receiver_email}!")
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        return False


def update_jobs_status(job_ids):
    """Updates the is_notified status for a list of job IDs."""
    if not job_ids:
        return

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    # The query to update the status for a given ID
    update_query = "UPDATE jobs SET is_notified = 1 WHERE id = ?;"

    # We need to format our list of IDs into a list of tuples for executemany
    # e.g., if job_ids is [1, 2, 3], we need [(1,), (2,), (3,)]
    ids_to_update = [(job_id,) for job_id in job_ids]

    try:
        cursor.executemany(update_query, ids_to_update)
        conn.commit()
        print(f"Successfully updated notification status for {len(job_ids)} jobs.")
    except sqlite3.Error as e:
        print(f"Database error during update: {e}")
        conn.rollback()  # Rollback changes if an error occurs
    finally:
        conn.close()


if __name__ == "__main__":
    # --- CONFIGURATION (Move to a config file or env variables later) ---
    SENDER_EMAIL = "benmerlotti@gmail.com"  # Your Gmail address
    SENDER_PASSWORD = "xoei uzmk blyc pugl"  # Your App Password
    RECEIVER_EMAIL = "benmerlotti@gmail.com"  # Where to send the notification
    # ---------------------------------------------------------------------

    jobs_to_notify = fetch_new_jobs()

    if jobs_to_notify:
        print(f"Found {len(jobs_to_notify)} new jobs to notify about.")

        email_subject = f"{len(jobs_to_notify)} New Python Job Listings!"
        email_body = format_jobs_for_email(jobs_to_notify)

        # Send the email
        email_sent = send_email(
            email_subject, email_body, SENDER_EMAIL, RECEIVER_EMAIL, SENDER_PASSWORD
        )

        # --- ADD THIS LOGIC ---
        # Only update the database IF the email was sent successfully
        if email_sent:
            # Get the IDs of the jobs we just notified about
            notified_job_ids = [job["id"] for job in jobs_to_notify]

            # Call the update function
            update_jobs_status(notified_job_ids)
        else:
            print("Email failed to send. Database status will not be updated.")
        # --- END OF ADDED LOGIC ---

        # We will add the database UPDATE logic here in the next step
    else:
        print("No new jobs found. No email sent.")
