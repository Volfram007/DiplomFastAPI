from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

import routes
from models import Base, User, ImageModel  # Импорт моделей
from database import engine, SessionLocal, get_db  # Настройка базы данных
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import os
import shutil

# Путь к проекту
BASE_DIR = Path(__file__).parent.parent
# Инициализация приложения FastAPI
app = FastAPI()

# Подключение статических файлов для использования в шаблонах
app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/app/static"), name="static")
# Настройка шаблонов
# templates = Jinja2Templates(directory="app/templates")
# Создание базы данных
Base.metadata.create_all(bind=engine)
app.include_router(routes.router)


# # Зависимость для сессии базы данных
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Модель данных для регистрации пользователя
# class UserCreate(BaseModel):
#     username: str
#     password: str


# @app.post("/register")
# async def register_user(
#     username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
# ):
#     print("register")
#     # Проверка, существует ли пользователь
#     existing_user = db.query(User).filter(User.username == username).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=400, detail="Пользователь с таким именем уже существует!"
#         )
#
#     # Хэширование пароля и сохранение нового пользователя
#     hashed_password = password  # Добавьте хэширование (например, bcrypt)
#     new_user = User(username=username, password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "Пользователь успешно зарегистрирован"}
#
#
# @app.post("/login")
# async def login_user(
#     username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.username == username).first()
#     if (
#         not user or user.password != password
#     ):  # Добавьте проверку пароля с использованием хэширования
#         raise HTTPException(status_code=400, detail="Неверный логин или пароль")
#
#     return {"message": "Успешная авторизация"}
#
#
# @app.get("/index", response_class=HTMLResponse)
# async def index(request: Request, db: Session = Depends(get_db)):
#     user = db.query(User).first()  # Для тестирования
#     if not user:
#         return RedirectResponse(url="/register")
#
#     images = db.query(ImageModel).filter_by(user_id=user.id).all()
#     return "<html><body><h1>Главная страница</h1></body></html>"


#
#
# @app.post("/upload_file")
# async def upload_file(
#     uploaded_files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db),
#     user_id: int = 1,  # Для тестирования, заменить на текущего пользователя
# ):
#     for uploaded_file in uploaded_files:
#         filename = uploaded_file.filename
#         filepath = f"static/images/{user_id}/{filename}"
#         os.makedirs(os.path.dirname(filepath), exist_ok=True)
#         with open(filepath, "wb") as buffer:
#             shutil.copyfileobj(uploaded_file.file, buffer)
#
#         # Сохранение информации в базе данных
#         new_image = ImageModel(
#             user_id=user_id, image_path=filepath, date=datetime.now()
#         )
#         db.add(new_image)
#         db.commit()
#     return {"message": "Файл(ы) успешно загружены"}
#
#
# @app.post("/delete_image/{image_id}")
# async def delete_image(image_id: int, db: Session = Depends(get_db)):
#     image = db.query(ImageModel).filter_by(id=image_id).first()
#     if not image:
#         raise HTTPException(status_code=404, detail="Изображение не найдено")
#
#     # Удаление файла из файловой системы
#     if os.path.exists(image.image_path):
#         os.remove(image.image_path)
#
#     db.delete(image)
#     db.commit()
#     return {"message": "Изображение удалено"}
#
#
# # Выход из системы (пример)
# @app.get("/logout")
# async def logout():
#     response = RedirectResponse(url="/index")
#     response.delete_cookie("session")
#     return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
