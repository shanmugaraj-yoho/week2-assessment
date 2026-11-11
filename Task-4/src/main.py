from fastapi import FastAPI
from dotenv import load_dotenv

from src import webhooks
from src import customers
from src.database import engine, Base

load_dotenv()

app = FastAPI(title="Secured Customer API")

Base.metadata.create_all(bind = engine)

app.include_router(customers.app)
app.include_router(webhooks.app)

@app.get("/health")
def health():
    return {"status": "ok"}
