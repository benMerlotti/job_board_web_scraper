# Automated Job Scraper & Notifier

## Project Overview

This is a Python-based application designed to automate the job search process. It periodically scrapes job listings from a target website, [builtin.com](https://builtin.com), stores them in a local SQLite database, and sends an email notification containing only the new, un-notified job opportunities that match a predefined search query.

This project demonstrates a full data pipeline:

- **Data Collection**: Scraping live data from a website.
- **Data Storage**: Persisting and managing data in a structured SQL database.
- **Data Processing**: Identifying new vs. existing data entries.
- **Application & Automation**: Triggering an action (email notification) based on the processed data.

---

## Key Features

- **Multi-Page Scraping**: Navigates through paginated search results to collect a comprehensive list of jobs.
- **Robust HTML Parsing**: Uses BeautifulSoup to extract job details by targeting structural elements and attributes.
- **Persistent Storage with SQLite**: Stores jobs in a local database to maintain a permanent record and prevent data loss.
- **Stateful Notification Logic**: Tracks notification status to ensure no repeat alerts.
- **Automated Email Alerts**: Formats job listings into a clean HTML email and sends using `smtplib` and Gmail App Password.
- **Duplicate Prevention**: Enforces a `UNIQUE` constraint on job links in the database schema to prevent duplicates.

---

## Tech Stack

- **Language**: Python 3
- **Libraries**:
  - `requests`: HTTP requests to download web content
  - `beautifulsoup4`: Parse and extract HTML data
  - `lxml`: Efficient HTML parser for BeautifulSoup
  - `sqlite3`: Built-in database management
  - `smtplib`, `email`: Built-in modules for sending emails

---
