import asyncio
from app.schemas.application import Job
from app.services.adzuna_service import search_adzuna_jobs
from app.services.remotive_service import search_remotive_jobs


async def search_all_jobs(
    what: str,
    where: str = "",
    page: int = 1,
    page_size: int = 40,
) -> list[Job]:
    results = await asyncio.gather(
        search_adzuna_jobs(
            what=what,
            where=where,
            page=page,
            results_per_page=page_size,
        ),
        search_remotive_jobs(what=what),
        return_exceptions=True,
    )

    jobs: list[Job] = []

    for result in results:
        if isinstance(result, Exception):
            print("Job provider failed:", result)
            continue

        jobs.extend(result)

    jobs = deduplicate_jobs(jobs)

    return jobs


def deduplicate_jobs(jobs: list[Job]) -> list[Job]:
    seen = set()
    unique_jobs: list[Job] = []

    for job in jobs:
        key = (
            job.title.lower().strip(),
            job.company.lower().strip(),
            job.location.lower().strip(),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_jobs.append(job)

    return unique_jobs