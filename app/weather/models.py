import datetime
from sqlalchemy import DateTime, Float, Column, UUID, ForeignKey, String
from app.database import Base
import uuid


class Weather(Base):
    __tablename__ = "weather"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    city = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())
