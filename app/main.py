




from fastapi import FastAPI
from contextlib import asynccontextmanager
from lifecycle import run_startup_tasks
from db.planned_routes import table
from db.connection import engine
from alerts.alerts_system import vehicle_alerts_table
from sqlalchemy import select
from fastapi.middleware.cors import CORSMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run everything on startup
    await run_startup_tasks()
    yield

app = FastAPI(title="VRP API", lifespan=lifespan)


origins = [
    "http://localhost:8080",  # frontend dev server
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # or ["*"] for all origins (not for production!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "VRP server running"}

@app.get("/routes")
def get_routes():
    with engine.connect() as conn:
        result = conn.execute(table.select())
        return [dict(row._mapping) for row in result]
@app.get("/alerts")
def get_alerts():
    with engine.connect() as conn:
        result = conn.execute(select(vehicle_alerts_table))
        return [dict(row._mapping) for row in result]
