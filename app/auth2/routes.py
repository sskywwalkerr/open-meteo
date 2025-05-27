from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.models.user_model import User
from app.auth2.auth import authenticate_user, create_access_token, get_password_hash
from app.database.database import get_session
from datetime import timedelta
from fastapi.responses import HTMLResponse
from app.templates_config import templates

router = APIRouter(tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/register", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_user(
        username: str = Form(...),
        password: str = Form(...),
        db: AsyncSession = Depends(get_session)
):
    try:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        existing_user = result.scalars().first()

        if existing_user:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Пользователь уже существует"}
            )

        hashed_password = get_password_hash(password)
        new_user = User(username=username, hashed_password=hashed_password)
        db.add(new_user)
        await db.commit()

        return {"success": True, "message": "Пользователь успешно зарегистрирован"}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@router.get("/login", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

