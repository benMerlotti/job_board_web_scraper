import requests
from bs4 import BeautifulSoup

MAX_PAGES_TO_SCRAPE = 3
scraped_jobs_data = []
BASE_URL = "https://builtin.com"

# ---------------------------------#

for page_num in range(1, MAX_PAGES_TO_SCRAPE + 1):
    PYTHONDEV_URL = f"https://builtin.com/jobs?search=python+developer&country=USA&allLocations=true&page={page_num}"

    # 2. Make the HTTP request and get the HTML content as a string
    print(f"Fetching page {page_num}...")
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
            # --- Extract Title, Company, Link ---
            job_title_tag = card.find("a", attrs={"data-id": "job-card-title"})
            job_company_name_tag = card.find("a", attrs={"data-id": "company-title"})

            if job_title_tag:
                job_title = job_title_tag.text.strip()
                # Use .get() for safety in case 'href' attribute is missing
                relative_link = job_title_tag.get("href")
                if relative_link:
                    full_job_link = BASE_URL + relative_link
                else:
                    full_job_link = "Link Not Found"
            else:
                job_title = "Title Not Found"
                full_job_link = "Link Not Found"

            if job_company_name_tag:
                job_company_name = job_company_name_tag.text.strip()
            else:
                # You had "Title Not Found" here, should be "Company Not Found" for clarity
                job_company_name = "Company Not Found"

            # --- Extract Experience Level ---
            experience_level = "Not specified"  # 1. Initialize with a default value

            trophy_icon = card.find("i", class_="fa-trophy")

            if trophy_icon:
                parent_div = trophy_icon.find_parent("div")
                span_tag = parent_div.find_next_sibling("span")
                if span_tag:
                    experience_level = span_tag.text.strip()

            # --- Extract Date Posted ---
            date_posted = "Not specified"

            clock_icon = card.find("i", class_="fa-clock")

            if clock_icon:
                span_tag = clock_icon.find_parent("span")
                if span_tag:
                    date_posted = span_tag.text.strip()

            # --- Extract Location ---
            job_location = "Not specified"

            gps_icon = card.find("i", class_="fa-location-dot")

            if gps_icon:
                parent_div = gps_icon.find_parent("div")
                sibling_div = parent_div.find_next_sibling("div")
                span_tag = sibling_div.find_next("span")
                if span_tag:
                    job_location = span_tag.text.strip()

            # --- Assemble the job data dictionary ---
            job_data = {
                "title": job_title,
                "company": job_company_name,
                "link": full_job_link,
                "experience": experience_level,
                "date posted": date_posted,
                "location": job_location,
            }

            scraped_jobs_data.append(job_data)

        # --- After the loop is finished ---
        if scraped_jobs_data:
            print(f"\nSuccessfully scraped {len(scraped_jobs_data)} jobs.")
            print("--- First 3 jobs scraped (with experience level) ---")
            # Let's import pprint for a cleaner print of dictionaries
            import pprint

            pp = pprint.PrettyPrinter(indent=2)
            for job in scraped_jobs_data[:3]:
                pp.pprint(job)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")

print("--- Scraping Complete ---")
