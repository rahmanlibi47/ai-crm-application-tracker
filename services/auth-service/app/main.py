from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.database import Base, engine
from app.models import User

from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "auth service running"}