# app/services/adzuna_service.py

import httpx
from app.core.config import settings

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api"


async def search_adzuna_jobs(
    what: str,
    where: str = "",
    page: int = 1,
    results_per_page: int = 20,
):
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

    return response.json()