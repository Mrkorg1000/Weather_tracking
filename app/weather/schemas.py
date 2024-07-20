from pydantic import BaseModel
from uuid import UUID
import datetime


class SchemaWeatherBase(BaseModel):
    city: str

    class Config:
        orm_mode = True


class SchemaWeatherCreate(SchemaWeatherBase):
    user_id: UUID
    temperature: float
    wind_speed: float


class SchemaWeatherDB(SchemaWeatherCreate):
    id: UUID
    created_at: datetime.datetime
