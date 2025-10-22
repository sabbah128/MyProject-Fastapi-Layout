from sqlalchemy import Column, String, Integer, Boolean, func, DateTime
from core.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from passlib.context import CryptContext
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, autoincrement=True)
    # username = Column(String(150), nullable=False)
    # password = Column(String, nullable=False)

    # is_active = Column(Boolean, default=True)
    
    # created_date = Column(DateTime, server_default=func.now())
    # updated_date= Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())


    tasks = relationship("TaskModel", back_populates="user")

    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)