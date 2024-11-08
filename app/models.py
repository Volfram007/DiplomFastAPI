from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Импорт базового класса для моделей
from flask_login import UserMixin


# Модель пользователя
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    # Связь с моделью изображений
    images = relationship("ImageModel", back_populates="user")


# Модель изображений
class ImageModel(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String(150), nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Обратная связь с моделью пользователя
    user = relationship("User", back_populates="images")
