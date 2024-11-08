from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_login import LoginManager
from sqlalchemy.orm import Session
from starlette import status

from models import User, ImageModel
from database import get_db, SessionLocal
from fastapi.templating import Jinja2Templates
from werkzeug.security import check_password_hash, generate_password_hash
import os

# Создание маршрутизатора и подключение шаблонов
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Секретный ключ для токенов
SECRET = os.getenv("SECRET_KEY", "your_secret_key")

# Инициализация менеджера входа
manager = LoginManager(SECRET, token_url="/login", use_cookie=True)
manager.cookie_name = "auth_token"


# Загрузка пользователя с использованием только имени пользователя
@manager.user_loader
def load_user(username: str):
    db = SessionLocal()  # Создание новой сессии базы данных
    user = db.query(User).filter(User.username == username).first()
    db.close()  # Закрытие сессии после запроса
    return user


# Маршрут для корневой страницы с редиректом на /authorization
@router.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/authorization")


# Маршрут для страницы авторизации
@router.get("/authorization", response_class=HTMLResponse)
async def authorization_page(request: Request, form_act: str = "login"):
    return templates.TemplateResponse(
        "authorization.html",
        {
            "request": request,
            "form_act": form_act,
            "btnHomeVisible": True,
            "btnAuthenticatedVisible": False,
            "error": None,
            "message": None,
        },
    )


# Обработка данных для авторизации и регистрации
@router.post("/authorization", response_class=HTMLResponse)
async def authorization(
    request: Request,
    db: Session = Depends(get_db),
    form_act: str = Form("login"),
    username: str = Form(...),
    password1: str = Form(...),
    password2: str = Form(None),
):
    error = None
    message = None

    if form_act == "login":
        print("authorization", form_act)
        user = load_user(username)
        # user = db.query(User).filter(User.username == username).first()
        print("authorization", user.username)
        if user and check_password_hash(user.password, password1):
            response = RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)
            manager.set_cookie(
                response, manager.create_access_token(data={"sub": username})
            )
            print("return response")
            return response
        else:
            error = "Неверный логин или пароль"
        print("authorization end")
    elif form_act == "register":
        if not username or not password1 or not password2:
            error = "Все поля обязательны для заполнения"
        elif password1 != password2:
            error = "Пароли не совпадают"
        elif db.query(User).filter(User.username == username).first():
            error = "Пользователь с таким именем уже существует"
        else:
            hashed_password = generate_password_hash(password1)
            new_user = User(username=username, password=hashed_password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            message = "Регистрация прошла успешно"
            response = RedirectResponse(url="/index", status_code=302)
            manager.set_cookie(
                response, manager.create_access_token(data={"sub": username})
            )
            return response

    return templates.TemplateResponse(
        "authorization.html",
        {
            "request": request,
            "form_act": form_act,
            "btnHomeVisible": True,
            "btnAuthenticatedVisible": False,
            "error": error,
            "message": message,
        },
    )


# Маршрут для выхода из системы
# @router.get("/logout")
# async def logout():
#     response = RedirectResponse(url="/authorization")
#     response.delete_cookie(manager.cookie_name)
#     return response


# Маршрут для отображения главной страницы
@router.get("/index", response_class=HTMLResponse)
async def index(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(manager),
):
    print("index")
    # user = db.query(User).first()  # Для тестирования
    # if not user:
    #     return RedirectResponse(url="/register")
    #
    # images = db.query(ImageModel).filter_by(user_id=user.id).all()
    return "<html><body><h1>Главная страница</h1></body></html>"


# Маршрут для отображения главной страницы
# @router.get("/index", response_class=HTMLResponse)
# async def index_page(
#     request: Request,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(manager),
# ):
#     print("index_page")
#     if current_user:
#         print("current_user")
#         return templates.TemplateResponse(
#             "index.html",
#             {
#                 "request": request,
#                 "current_user": current_user,
#                 "btnHomeVisible": True,
#                 "btnAuthenticatedVisible": True,
#                 "page_obj": [],  # Добавьте данные о фотографиях здесь
#                 "page": 1,
#                 "total_pages": 1,
#                 "has_prev": False,
#                 "has_next": False,
#                 "AnonymousUser": None,
#             },
#         )
#     else:
#         return templates.TemplateResponse(
#             "index.html",
#             {
#                 "request": request,
#                 "current_user": None,
#                 "AnonymousUser": "Пожалуйста, авторизуйтесь для доступа к альбому",
#             },
#         )
