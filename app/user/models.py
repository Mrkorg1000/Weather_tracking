from sqlalchemy import String, Column, Integer, UUID
from app.database import Base
import uuid


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    