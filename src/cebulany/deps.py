from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from os import environ

# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# app.config['TOKEN_TIME'] = int(environ.get('CEBULANY_TOKEN_TIME', '600'))
# app.config['TOTP_SUPPORT'] = environ.get('TOTP_SUPPORT', 'yes') == 'yes'
# app.config['APP_NAME'] = environ.get('CEBULANY_APP_NAME', 'cebulany manager')

DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///test.db')
Session = async_sessionmaker(create_async_engine(DATABASE_URI))


async def session() -> AsyncSession:
    async with Session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(session)]