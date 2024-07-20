from uuid import UUID
from fastapi import HTTPException, status
from app.database import async_session_maker
from sqlalchemy import select, insert
from fastapi.exceptions import ResponseValidationError


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: UUID):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
         
    
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            object_list = result.scalars().all()
            return object_list
    
    @classmethod
    async def add(cls, object):
        async with async_session_maker() as session:
            new_object = cls.model(**object.dict())
            session.add(new_object)
            await session.commit()
            await session.refresh(new_object)
            return new_object


    @classmethod
    async def delete(cls, object):
        async with async_session_maker() as session:
            await session.delete(object)
            await session.commit()
            