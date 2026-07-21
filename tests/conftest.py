from decimal import Decimal

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from car_api.app import app
from car_api.core.database import get_session
from car_api.core.security import create_access_token, get_password_hash
from car_api.models import Base
from car_api.models.cars import Brand, Car, FuelType, TransmissionType
from car_api.models.users import User


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        url='sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def client(session):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPassword',
    }


@pytest.fixture
def second_user_data():
    return {
        'username': 'otheruser',
        'email': 'other@example.com',
        'password': 'OtherPassword',
    }


@pytest.fixture
def brand_data():
    return {
        'name': 'Toyota',
        'description': 'Japanese automaker',
        'is_active': True,
    }


@pytest.fixture
def second_brand_data():
    return {
        'name': 'Honda',
        'description': 'Second automaker',
        'is_active': False,
    }


@pytest.fixture
def car_data():
    return {
        'model': 'Corolla',
        'factory_year': 2024,
        'model_year': 2025,
        'color': 'Silver',
        'plate': 'ABC1D23',
        'fuel_type': FuelType.FLEX.value,
        'transmission': TransmissionType.AUTOMATIC.value,
        'price': '135000.00',
        'description': 'Sedan',
        'is_available': True,
        'brand_id': 1,
        'owner_id': 1,
    }


@pytest.fixture
def second_car_data():
    return {
        'model': 'Civic',
        'factory_year': 2023,
        'model_year': 2024,
        'color': 'Black',
        'plate': 'XYZ9A88',
        'fuel_type': FuelType.GASOLINE.value,
        'transmission': TransmissionType.CVT.value,
        'price': '155000.00',
        'description': 'Coupe',
        'is_available': False,
        'brand_id': 1,
        'owner_id': 1,
    }


@pytest_asyncio.fixture
async def user(session, user_data):
    db_user = User(
        username=user_data['username'],
        email=user_data['email'],
        password=get_password_hash(user_data['password']),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@pytest_asyncio.fixture
async def second_user(session, second_user_data):
    db_user = User(
        username=second_user_data['username'],
        email=second_user_data['email'],
        password=get_password_hash(second_user_data['password']),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@pytest.fixture
def auth_headers(user):
    token = create_access_token({'sub': str(user.id)})
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def second_auth_headers(second_user):
    token = create_access_token({'sub': str(second_user.id)})
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def brand(session, brand_data):
    db_brand = Brand(**brand_data)

    session.add(db_brand)
    await session.commit()
    await session.refresh(db_brand)

    return db_brand


@pytest_asyncio.fixture
async def second_brand(session, second_brand_data):
    db_brand = Brand(**second_brand_data)

    session.add(db_brand)
    await session.commit()
    await session.refresh(db_brand)

    return db_brand


@pytest_asyncio.fixture
async def car(session, user, brand, car_data):
    db_car = Car(
        model=car_data['model'],
        factory_year=car_data['factory_year'],
        model_year=car_data['model_year'],
        color=car_data['color'],
        plate=car_data['plate'],
        fuel_type=car_data['fuel_type'],
        transmission=car_data['transmission'],
        price=Decimal(car_data['price']),
        description=car_data['description'],
        is_available=car_data['is_available'],
        brand_id=brand.id,
        owner_id=user.id,
    )

    session.add(db_car)
    await session.commit()
    await session.refresh(db_car)

    return db_car


@pytest_asyncio.fixture
async def second_car(session, user, brand, second_car_data):
    db_car = Car(
        model=second_car_data['model'],
        factory_year=second_car_data['factory_year'],
        model_year=second_car_data['model_year'],
        color=second_car_data['color'],
        plate=second_car_data['plate'],
        fuel_type=second_car_data['fuel_type'],
        transmission=second_car_data['transmission'],
        price=Decimal(second_car_data['price']),
        description=second_car_data['description'],
        is_available=second_car_data['is_available'],
        brand_id=brand.id,
        owner_id=user.id,
    )

    session.add(db_car)
    await session.commit()
    await session.refresh(db_car)

    return db_car
