import requests
from bs4 import BeautifulSoup

# 1. Define the URL
PYTHONDEV_URL = (
    "https://builtin.com/jobs?search=python+developer&country=USA&allLocations=true"
)

# 2. Make the HTTP request and get the HTML content as a string
print(f"Fetching HTML from {PYTHONDEV_URL}...")
try:
    response = requests.get(PYTHONDEV_URL)

    response.raise_for_status()

    html_text = response.text
    print("Successfully fetched HTML.")

    soup = BeautifulSoup(html_text, "lxml")
    print("HTML parsed successfully.")

    job_cards = soup.find_all("div", class_="job-bounded-responsive")

    if job_cards:
        print(len(job_cards))

    for card in job_cards:
        print(card)


except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the URL: {e}")
