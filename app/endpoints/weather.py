import logging
from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth2.auth import get_current_user
from app.models import User
from app.services.weather_service import get_weather_data
from app.database.database import get_session
from app.models.history_models import SearchHistory
from fastapi.responses import HTMLResponse
from app.templates_config import templates

router = APIRouter(tags=["Weather"])


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/weather/", response_class=HTMLResponse)
async def get_weather(
    request: Request,
    city: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    try:
        data = await get_weather_data(city, db, user)
        print(f"Data passed to template: {data}")

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "current": data["current"],
                "hourly": data["hourly"],
                "history": data["history"]
            }
        )
    except ValueError as ve:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": str(ve)}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": f"Произошла ошибка: {str(e)}"}
        )

@router.get("/history", response_class=HTMLResponse)
async def get_search_history(
    request: Request,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    try:
        query = select(SearchHistory).where(SearchHistory.user_id == user.id)
        result = await db.execute(query)
        history = result.scalars().all()

        print(f"Search history for user {user.id}: {history}")

        return templates.TemplateResponse(
            "history.html",
            {"request": request, "history": history}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": f"Ошибка загрузки истории: {str(e)}"}
        )
