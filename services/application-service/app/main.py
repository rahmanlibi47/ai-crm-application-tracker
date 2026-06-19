from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, engine
from app.db.models import JobApplication

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Application Service")

app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "application service running"
    }