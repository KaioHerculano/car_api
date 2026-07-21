from fastapi import status


def test_create_user_success(client, user_data):
    response = client.post('/api/v1/users/', json=user_data)

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data['username'] == user_data['username']
    assert data['email'] == user_data['email']
    assert 'password' not in data


def test_create_user_error_400_duplicate_username(client, user, user_data):
    response = client.post(
        '/api/v1/users/',
        json={
            'username': user_data['username'],
            'email': 'new@example.com',
            'password': user_data['password'],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Username já está em uso'


def test_create_user_error_400_duplicate_email(client, user, user_data):
    response = client.post(
        '/api/v1/users/',
        json={
            'username': 'newuser',
            'email': user_data['email'],
            'password': user_data['password'],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Email já está em uso'


def test_create_user_error_422_invalid_payload(client):
    response = client.post(
        '/api/v1/users/',
        json={'username': 'ab', 'email': 'invalid', 'password': '123'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_users_success(client, user, second_user, auth_headers):
    response = client.get(
        '/api/v1/users/',
        headers=auth_headers,
        params={'search': 'other', 'offset': 0, 'limit': 10},
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['offset'] == 0
    assert data['limit'] == 10
    assert len(data['users']) == 1
    assert data['users'][0]['id'] == second_user.id


def test_list_users_without_authentication(client):
    response = client.get('/api/v1/users/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user_success(client, user, auth_headers):
    response = client.get(f'/api/v1/users/{user.id}', headers=auth_headers)

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['id'] == user.id
    assert data['email'] == user.email


def test_get_user_error_404(client, auth_headers):
    response = client.get('/api/v1/users/999', headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Usuário não encontrado'


def test_update_user_success(client, user, auth_headers):
    response = client.put(
        f'/api/v1/users/{user.id}',
        headers=auth_headers,
        json={
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password': 'UpdatedPassword',
        },
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['username'] == 'updateduser'
    assert data['email'] == 'updated@example.com'
    assert 'password' not in data


def test_update_user_error_400_duplicate_username(
    client, user, second_user, auth_headers
):
    response = client.put(
        f'/api/v1/users/{user.id}',
        headers=auth_headers,
        json={'username': second_user.username},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Username já está em uso'


def test_update_user_error_400_duplicate_email(
    client, user, second_user, auth_headers
):
    response = client.put(
        f'/api/v1/users/{user.id}',
        headers=auth_headers,
        json={'email': second_user.email},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Email já está em uso'


def test_update_user_error_404(client, auth_headers):
    response = client.put(
        '/api/v1/users/999',
        headers=auth_headers,
        json={'username': 'missinguser'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Usuário não encontrado'


def test_update_user_error_422_invalid_payload(client, user, auth_headers):
    response = client.put(
        f'/api/v1/users/{user.id}',
        headers=auth_headers,
        json={'username': 'ab', 'password': '123'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_user_success(client, user, auth_headers):
    response = client.delete(
        f'/api/v1/users/{user.id}',
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b''


def test_delete_user_error_404(client, auth_headers):
    response = client.delete('/api/v1/users/999', headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Usuário não encontrado'
