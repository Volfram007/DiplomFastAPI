from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base  # Импорт базового класса и моделей

# Создание экземпляра приложения FastAPI
app = FastAPI()

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Импорт маршрутов для добавления их в приложение
import routes  # Импорт вашего модуля с маршрутами

# Подключение маршрутов, если они зарегистрированы через роутинг в routes.py
app.include_router(routes.router)
