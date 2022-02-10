from datetime import datetime
import json
import requests
from helper import pushify
from helper import gmail_sender


def jobs_scraper(URL):
    keys = ["date", "company", "position", "tags", "location", "url"]
    tags_needed = ["python", "javascript", "remote", "web"]

    response = requests.get(URL)
    jobs_results = response.json()

    jobs = []

    for job_result in jobs_results:
        job = {key: value for key, value in job_result.items() if key in keys}

        if job:
            tags = job.get("tags")
            tags = {tag.lower() for tag in tags}
            if tags.intersection(tags_needed):
                jobs.append(job)

    if jobs:
        jobs_file = f"jobs_on_{current_date}.txt"

        with open(jobs_file, "a") as file_obj:
            for idx, job in enumerate(jobs, start=1):
                post_on = job["date"]
                company = job["company"]
                position = job["position"]
                tags = job["tags"]
                location = job["location"]
                url = job["url"]

                file_obj.write(f"- {idx} -\nCompany: {company}\nPosition: {position}\nLocation: {location}\nPost on: {post_on}\nTags: {tags}\nApply on: {url}\n\n")

    return jobs_file


if __name__ == "__main__":
    API_KEY = "your-api-key-for-pushbullet"  # pushbullet.com
    URL = "https://remoteok.io/api"

    now = datetime.now()
    current_date = now.strftime("%m-%d-%Y")

    title = "Remote Python Jobs!"
    text = "Check your mail/phone for new Jobs to apply."
    icon = "apply.ico"

    jobs_file = jobs_scraper(URL)

    with open(jobs_file) as file_obj:
        jobs = file_obj.read()

    pushify(API_KEY, jobs)
    gmail_sender(jobs)

    # Schedule a Cron Job everyday at 05:00AM.
    """
    In terminal, enter the following commands:
    `crontab -e`
    `0 17 * * * python3 ~/full-path/to/my/program.py`
    """
