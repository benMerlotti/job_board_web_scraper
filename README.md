# Automated Job Scraper & Notifier

## Project Overview

This is a Python-based application designed to streamline the job search process. It allows a user to manually trigger a process that scrapes job listings from a target website ([builtin.com](https://builtin.com)), stores them in a local SQLite database, and sends an email notification containing only the new, un-notified job opportunities found since the last run.

This project demonstrates a full data pipeline, covering:

- **Data Collection**: Scraping live data from a website on demand.  
- **Data Storage**: Persisting and managing data in a structured SQL database.  
- **Data Processing**: Identifying new vs. existing data entries.  
- **Application Logic**: Triggering an action (email notification) based on the processed data.  

The system is designed to be run periodically by a user or an external scheduling tool (like `cron`) to achieve full automation.

## Key Features

- **Multi-Page Scraping**: The scraper is capable of navigating through paginated search results to collect a comprehensive list of jobs.
- **Robust HTML Parsing**: Uses the BeautifulSoup library to navigate the HTML DOM, extracting specific job details by targeting structural elements and attributes rather than brittle text content.
- **Persistent Storage with SQLite**: All scraped jobs are saved to a local SQLite database, creating a permanent record and preventing data loss between runs.
- **Stateful Notification Logic**: The application maintains the notification status for each job. It only queries and sends jobs that have not been previously notified, preventing repeat alerts on subsequent runs.
- **Consolidated Email Alerts**: Formats all new job listings found in a single run into a clean HTML email and sends it to a specified recipient using `smtplib` and a secure App Password for authentication.
- **Duplicate Prevention**: The database schema enforces a `UNIQUE` constraint on job links to ensure data integrity and prevent duplicate entries.

## Tech Stack

**Language**: Python 3

**Libraries**:

- `requests`: For making HTTP requests to download web page content.
- `beautifulsoup4`: For parsing HTML and extracting data.
- `lxml`: An efficient parser for BeautifulSoup.
- `sqlite3`: (Built-in) For database interaction and storage.
- `smtplib`, `email`: (Built-in) For constructing and sending email notifications.