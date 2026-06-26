import httpx
from app.schemas.application import Job


async def search_remotive_jobs(
    what: str,
) -> list[Job]:
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            "https://remotive.com/api/remote-jobs",
            params={"search": what},
        )
        response.raise_for_status()

    data = response.json()

    jobs: list[Job] = []

    for item in data.get("jobs", []):
        jobs.append(
            Job(
                id=str(item.get("id")),
                source="remotive",
                title=item.get("title") or "",
                company=item.get("company_name") or "Unknown",
                location=item.get("candidate_required_location") or "Remote",
                description=item.get("description") or "",
                salary=item.get("salary") or None,
                apply_url=item.get("url") or "",
                company_logo=item.get("company_logo_url") or item.get("company_logo"),
                tags=item.get("tags") or [],
                posted_at=item.get("publication_date"),
            )
        )

    return jobs