from fastapi import FastAPI

from app.database import Base, engine
from app.models import User

from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "auth service running"}