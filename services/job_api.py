import os
import requests
from typing import List, Dict, Any, Optional
try:
    from config.settings import RAPIDAPI_KEY, RAPIDAPI_HOST, JSEARCH_ENDPOINT
except (ImportError, ValueError):
    from ..config.settings import RAPIDAPI_KEY, RAPIDAPI_HOST, JSEARCH_ENDPOINT

def normalize_job(raw_job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a raw job dictionary from JSearch API into a clean, uniform schema.
    Missing or null fields default to 'Not provided'.
    """
    # Location assembly
    city = raw_job.get("job_city")
    state = raw_job.get("job_state")
    country = raw_job.get("job_country")
    loc_parts = [p for p in [city, state, country] if p]
    location = ", ".join(loc_parts) if loc_parts else raw_job.get("job_location", "Not provided")

    # Salary assembly
    min_sal = raw_job.get("job_min_salary")
    max_sal = raw_job.get("job_max_salary")
    currency = raw_job.get("job_salary_currency", "$")
    if currency == "USD":
        currency = "$"
    elif currency == "INR":
        currency = "₹"
    elif currency == "EUR":
        currency = "€"
    elif currency == "GBP":
        currency = "£"
    period = raw_job.get("job_salary_period", "year")
    
    if min_sal and max_sal:
        salary = f"{currency}{min_sal:,.0f} - {currency}{max_sal:,.0f} / {period}"
    elif min_sal:
        salary = f"From {currency}{min_sal:,.0f} / {period}"
    elif max_sal:
        salary = f"Up to {currency}{max_sal:,.0f} / {period}"
    else:
        salary = "Not provided"

    # Date posted
    posted_raw = raw_job.get("job_posted_at_datetime_utc") or raw_job.get("job_offer_expiration_datetime_utc")
    date_posted = str(posted_raw)[:10] if posted_raw else "Recently"

    # Description
    desc = raw_job.get("job_description", "")
    if not desc:
        desc = "Not provided"

    # Job type
    job_type = raw_job.get("job_employment_type", "Full-time")
    if isinstance(job_type, str):
        job_type = job_type.replace("_", " ").title()

    return {
        "job_id": raw_job.get("job_id", str(hash(raw_job.get("job_title", "") + raw_job.get("employer_name", "")))),
        "title": raw_job.get("job_title", "Untitled Position"),
        "company": raw_job.get("employer_name", "Unknown Employer"),
        "location": location,
        "description": desc,
        "job_type": job_type,
        "salary": salary,
        "date_posted": date_posted,
        "apply_url": raw_job.get("job_apply_link", "#"),
        "source": "JSearch API"
    }

def search_jobs(
    query: str,
    location: Optional[str] = None,
    country: str = "us",
    num_pages: int = 1,
    date_posted: str = "all"
) -> Dict[str, Any]:
    """
    Queries RapidAPI JSearch endpoint and normalizes returned jobs.
    Does NOT run NLP analysis across all jobs. Returns normalized job objects for display.
    """
    api_key = os.getenv("RAPIDAPI_KEY") or RAPIDAPI_KEY
    if not api_key or api_key == "your_rapidapi_key_here":
        return {
            "success": False,
            "error": "RapidAPI key is not configured. Please add RAPIDAPI_KEY to your .env file.",
            "jobs": []
        }

    # Construct complete search query
    full_query = query.strip()
    if location and location.strip():
        full_query = f"{full_query} jobs in {location.strip()}"

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": api_key
    }

    params = {
        "query": full_query,
        "num_pages": str(num_pages),
        "country": country,
        "date_posted": date_posted
    }

    endpoints_to_try = [
        JSEARCH_ENDPOINT,  # Primary endpoint: search-v2
        f"https://{RAPIDAPI_HOST}/search"  # Fallback endpoint: search (v1)
    ]

    last_error = ""

    for endpoint in endpoints_to_try:
        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=60)
            
            if response.status_code == 200:
                resp_json = response.json()
                data = resp_json.get("data", [])
                if isinstance(data, dict):
                    raw_jobs = data.get("jobs", [])
                elif isinstance(data, list):
                    raw_jobs = data
                else:
                    raw_jobs = []

                normalized_jobs = [normalize_job(j) for j in raw_jobs if isinstance(j, dict)]
                return {
                    "success": True,
                    "count": len(normalized_jobs),
                    "query": full_query,
                    "jobs": normalized_jobs
                }
            elif response.status_code == 429:
                return {
                    "success": False,
                    "error": "RapidAPI rate limit exceeded. Please try again later or use the Manual Job Description fallback.",
                    "jobs": []
                }
            elif response.status_code == 403 or response.status_code == 401:
                return {
                    "success": False,
                    "error": "RapidAPI authentication failed. Please verify your RAPIDAPI_KEY in .env.",
                    "jobs": []
                }
            else:
                last_error = f"JSearch API returned status {response.status_code}: {response.text[:200]}"
                continue
        except requests.exceptions.Timeout:
            last_error = "JSearch API request timed out (server took >60s). RapidAPI backend is currently experiencing high load."
            continue
        except requests.exceptions.RequestException as e:
            last_error = f"Network error connecting to JSearch API: {str(e)}"
            continue

    return {
        "success": False,
        "error": last_error if last_error else "Unable to retrieve jobs from JSearch API. Please check internet connection or use offline demo jobs.",
        "jobs": []
    }

def get_mock_jobs() -> List[Dict[str, Any]]:
    """
    Returns curated sample jobs for offline testing, demoing, or fallback when API quota is reached.
    """
    return [
        {
            "job_id": "mock-job-1",
            "title": "Machine Learning Engineer",
            "company": "ABC Technologies",
            "location": "Bengaluru, Karnataka, India",
            "description": (
                "We are seeking an experienced Machine Learning Engineer to design, build, and deploy production ML systems.\n\n"
                "Requirements:\n"
                "- Strong proficiency in Python, Machine Learning, and Deep Learning algorithms.\n"
                "- Hands-on experience with PyTorch, TensorFlow, Scikit-learn, and Pandas.\n"
                "- Solid knowledge of SQL, PostgreSQL, and Data Engineering pipelines.\n"
                "- Experience deploying models with Docker and AWS (ECS, S3, SageMaker).\n"
                "- Bachelor's degree in Computer Science, Data Science, or related engineering discipline.\n"
                "- 2+ years of professional software development or ML experience.\n\n"
                "Responsibilities:\n"
                "- Build end-to-end NLP and classification pipelines.\n"
                "- Collaborate with backend teams to integrate REST APIs.\n"
                "- Optimize model latency and perform unit testing."
            ),
            "job_type": "Full-time",
            "salary": "$85,000 - $120,000 / year",
            "date_posted": "2026-09-08",
            "apply_url": "https://example.com/apply/ml-engineer",
            "source": "Sample Demo Database"
        },
        {
            "job_id": "mock-job-2",
            "title": "Python Data Scientist / NLP Specialist",
            "company": "DataSphere AI Labs",
            "location": "Bengaluru / Remote",
            "description": (
                "Looking for a Data Scientist specializing in Natural Language Processing and Predictive Analytics.\n\n"
                "Key Qualifications:\n"
                "- Minimum 1 to 3 years of hands-on experience in NLP, text processing, and information extraction.\n"
                "- Expert in Python, Pandas, NumPy, Scikit-learn, and spaCy or NLTK.\n"
                "- Familiarity with Git, GitHub, REST APIs, and MongoDB.\n"
                "- Bachelor's or Master's degree in Computer Science or Mathematics.\n"
                "- Nice to have: Experience with Hugging Face transformers, Docker, and Azure."
            ),
            "job_type": "Full-time",
            "salary": "$90,000 - $115,000 / year",
            "date_posted": "2026-09-10",
            "apply_url": "https://example.com/apply/data-scientist",
            "source": "Sample Demo Database"
        },
        {
            "job_id": "mock-job-3",
            "title": "Full Stack Python Developer",
            "company": "CloudPeak Solutions",
            "location": "Hyderabad, Telangana, India",
            "description": (
                "Seeking a Full Stack Python Developer with experience in web frameworks and cloud deployments.\n\n"
                "Requirements:\n"
                "- Core development experience in Python, FastAPI, Django, or Flask.\n"
                "- Frontend knowledge of JavaScript, HTML, CSS, and React.\n"
                "- Strong database skills with MySQL, PostgreSQL, and Redis.\n"
                "- Familiarity with Docker, Kubernetes, CI/CD, and Linux environments.\n"
                "- 3+ years of software development experience required.\n"
                "- B.Tech/B.E. in Computer Science or related degree."
            ),
            "job_type": "Full-time",
            "salary": "$75,000 - $105,000 / year",
            "date_posted": "2026-09-05",
            "apply_url": "https://example.com/apply/python-dev",
            "source": "Sample Demo Database"
        }
    ]
