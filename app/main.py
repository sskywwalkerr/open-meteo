from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.auth2.routes import router as signup_router
from app.database.database import init_db
from app.endpoints.weather import router as weather_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="API Project")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(weather_router, prefix="/api")
app.include_router(signup_router, prefix="/api/auth")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/api/")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
