import httpx
from app.core.config import settings
from app.schemas.application import Job

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api"


async def search_adzuna_jobs(
    what: str,
    where: str = "",
    page: int = 1,
    results_per_page: int = 120,
) -> list[Job]:
    url = f"{ADZUNA_BASE_URL}/jobs/{settings.ADZUNA_COUNTRY}/search/{page}"

    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": what,
        "where": where,
        "content-type": "application/json",
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()

    data = response.json()

    jobs: list[Job] = []

    for item in data.get("results", []):
        jobs.append(
            Job(
                id=str(item.get("id")),
                source="adzuna",
                title=item.get("title") or "",
                company=item.get("company", {}).get("display_name") or "Unknown",
                location=item.get("location", {}).get("display_name") or "",
                description=item.get("description") or "",
                salary=format_adzuna_salary(item),
                apply_url=item.get("redirect_url") or "",
                company_logo=None,
                tags=[],
                posted_at=item.get("created"),
            )
        )

    return jobs


def format_adzuna_salary(item: dict) -> str | None:
    salary_min = item.get("salary_min")
    salary_max = item.get("salary_max")

    if salary_min and salary_max:
        return f"{int(salary_min)} - {int(salary_max)}"

    if salary_min:
        return f"From {int(salary_min)}"

    if salary_max:
        return f"Up to {int(salary_max)}"

    return None