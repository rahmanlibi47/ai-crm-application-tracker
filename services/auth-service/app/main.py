from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.models import User

from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    root_path="/api/auth",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://careerledger.libinrahman.cloud",
        "http://docker.libinrahman.cloud",
        "https://docker.libinrahman.cloud",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "auth service running"}
