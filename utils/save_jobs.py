import csv
from browser_use import ActionResult
from pydantic import BaseModel

class Job(BaseModel):
    title: str
    link: str
    company: str
    fit_score: float
    location: str | None = None
    salary: str | None = None

def save_jobs_to_csv(job: Job):
    try:
        with open("jobs.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([job.title, job.company, job.link, job.salary, job.location])
            print(f"[DEBUG] Writing job to CSV: {job.title}")
        return ActionResult(extracted_content="Saved job to file.")
    except Exception as e:
        return ActionResult(error=str(e))
