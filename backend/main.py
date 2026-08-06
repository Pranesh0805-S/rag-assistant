from fastapi import FastAPI
from app.routers import auth, documents

app = FastAPI()

app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}