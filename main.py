from fastapi import FastAPI
from app.database import Base, engine
from app.user.router import router as router_user
from app.weather.router import router as router_weather


app = FastAPI()


app.include_router(router_user)
app.include_router(router_weather)


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
