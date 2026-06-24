from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db.database import Base, engine
from app.db.models import JobApplication

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Application Service",
    root_path="/api/app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://careerledger.libinrahman.cloud",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "application service running"
    }