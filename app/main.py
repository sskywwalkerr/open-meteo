from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database.database import init_db
from app.endpoints.weather import router as weather_router
from fastapi.responses import RedirectResponse
app = FastAPI(title="API Project")


app.include_router(weather_router, prefix="/api")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/api/")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
