from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL для подключения к базе данных (например, SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Создание движка для подключения к базе данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создание сессии для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Декларативный базовый класс, от которого наследуются модели
Base = declarative_base()


# Функция зависимости для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
