import pytest
from fastapi import status
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from car_api.core import database
from car_api.models import Base
from car_api.models.cars import Brand, Car
from car_api.models.users import User


@pytest.mark.asyncio
async def test_database_tables_are_created(session):
    bind = await session.connection()
    tables = await bind.run_sync(
        lambda conn: inspect(conn).get_table_names()
    )

    assert set(tables) == set(Base.metadata.tables)


@pytest.mark.asyncio
async def test_database_saves_and_reads_user(session, user):
    db_user = await session.scalar(
        select(User).where(User.email == user.email)
    )

    assert db_user is not None
    assert db_user.id == user.id
    assert db_user.username == user.username


@pytest.mark.asyncio
async def test_database_rejects_duplicate_user_email(session, user):
    duplicate = User(
        username='duplicated',
        email=user.email,
        password='password',
    )

    session.add(duplicate)

    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_database_relationships_are_consistent(session, car):
    db_car = await session.get(Car, car.id)
    db_user = await session.get(User, car.owner_id)
    db_brand = await session.get(Brand, car.brand_id)

    assert db_car is not None
    assert db_user is not None
    assert db_brand is not None
    assert db_car.owner_id == db_user.id
    assert db_car.brand_id == db_brand.id


def test_health_check(client):
    response = client.get('/health_check')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}


@pytest.mark.asyncio
async def test_get_session_yields_async_session(monkeypatch):
    engine = create_async_engine(
        url='sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    monkeypatch.setattr(database, 'engine', engine)

    session_generator = database.get_session()
    db_session = await anext(session_generator)

    assert isinstance(db_session, AsyncSession)

    await session_generator.aclose()
    await engine.dispose()
