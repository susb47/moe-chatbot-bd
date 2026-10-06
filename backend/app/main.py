from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # ADD THIS IMPORT
from fastapi.responses import HTMLResponse  # ADD THIS IMPORT

from app.core.config import settings
from app.api.routes import router as api_router
from app.database.connection import engine, Base
import app.database.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ADD THESE LINES TO SERVE THE UI ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()
# ---------------------------------------

app.include_router(api_router, prefix="/api")