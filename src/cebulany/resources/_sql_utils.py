from cebulany.models import Base as SQLBase
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert


def unpack(T: type[BaseModel], obj: object) -> T:
    raw = {
        key: getattr(obj, key)
        for key, field in T.model_fields.items()
    }
    return T(**raw)


async def get_all(O: type[SQLBase], T: type[BaseModel], session: AsyncSession) -> list[T]:
    stmt = select(O)
    result = await session.execute(stmt)
    return [unpack[T](obj) for obj in result]


async def get_by_id(O: type[SQLBase], T: type[BaseModel], id: int, session: AsyncSession) -> T:
    stmt = select(O).filter_by(id=id)
    obj = await session.execute(stmt).first()
    return unpack[T](obj)


async def create(O: type[SQLBase], T: type[BaseModel], , session: AsyncSession) -> T:
    stmt = select(O).filter_by(id=id)
    obj = await session.execute(stmt).first()
    return unpack[T](obj)