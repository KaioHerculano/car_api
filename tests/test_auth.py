from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException, status

from car_api.core.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_car_ownership,
    verify_password,
    verify_token,
)
from car_api.core.security import settings as security_settings


def test_token_success(client, user, user_data):
    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': user_data['email'],
            'password': user_data['password'],
        },
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['token_type'] == 'bearer'
    assert isinstance(data['access_token'], str)
    assert verify_token(data['access_token'])['sub'] == str(user.id)


def test_token_error_401_invalid_email(client, user_data):
    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': 'missing@example.com',
            'password': user_data['password'],
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'
    assert response.headers['WWW-Authenticate'] == 'Bearer'


def test_token_error_401_invalid_password(client, user, user_data):
    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': user_data['email'],
            'password': 'WrongPassword',
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_token_error_422_invalid_payload(client):
    response = client.post(
        '/api/v1/auth/token',
        json={'email': 'invalid', 'password': '123'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_refresh_token_success(client, auth_headers):
    response = client.post('/api/v1/auth/refresh_token', headers=auth_headers)

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['token_type'] == 'bearer'
    assert 'access_token' in data


def test_refresh_token_without_header(client):
    response = client.post('/api/v1/auth/refresh_token')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_route_rejects_invalid_token(client):
    response = client.get(
        '/api/v1/users/',
        headers={'Authorization': 'Bearer invalid-token'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_protected_route_rejects_token_without_sub(client):
    token = create_access_token({'username': 'testuser'})

    response = client.get(
        '/api/v1/users/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_protected_route_rejects_token_with_invalid_sub(client):
    token = create_access_token({'sub': 'abc'})

    response = client.get(
        '/api/v1/users/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_protected_route_rejects_token_for_missing_user(client):
    token = create_access_token({'sub': '999'})

    response = client.get(
        '/api/v1/users/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_verify_token_rejects_expired_token():
    token = jwt.encode(
        {
            'sub': '1',
            'exp': datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        security_settings.JWT_SECRET_KEY,
        algorithm=security_settings.JWT_ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        verify_token(token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Token has expired'


def test_password_hash_and_verify_password():
    hashed_password = get_password_hash('TestPassword')

    assert hashed_password != 'TestPassword'
    assert verify_password('TestPassword', hashed_password)
    assert not verify_password('WrongPassword', hashed_password)


@pytest.mark.asyncio
async def test_authenticate_user_success(session, user, user_data):
    authenticated_user = await authenticate_user(
        user_data['email'],
        user_data['password'],
        session,
    )

    assert authenticated_user == user


@pytest.mark.asyncio
async def test_authenticate_user_returns_none_for_invalid_password(
    session, user, user_data
):
    authenticated_user = await authenticate_user(
        user_data['email'],
        'WrongPassword',
        session,
    )

    assert authenticated_user is None


def test_verify_car_ownership_accepts_owner(user):
    assert verify_car_ownership(user, user.id) is None


def test_verify_car_ownership_rejects_non_owner(user):
    with pytest.raises(HTTPException) as exc_info:
        verify_car_ownership(user, user.id + 1)

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == 'Not enough permissions to access this car'
