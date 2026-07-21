from fastapi import status


def test_create_brand_success(client, auth_headers, brand_data):
    response = client.post(
        '/api/v1/brands/',
        headers=auth_headers,
        json=brand_data,
    )

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data['name'] == brand_data['name']
    assert data['description'] == brand_data['description']
    assert data['is_active'] is True


def test_create_brand_error_400_duplicate_name(
    client, auth_headers, brand, brand_data
):
    response = client.post(
        '/api/v1/brands/',
        headers=auth_headers,
        json=brand_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Nome da marca já está em uso'


def test_create_brand_error_422_invalid_payload(client, auth_headers):
    response = client.post(
        '/api/v1/brands/',
        headers=auth_headers,
        json={'name': 'a'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_brand_without_authentication(client, brand_data):
    response = client.post('/api/v1/brands/', json=brand_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_brands_success(
    client, auth_headers, brand, second_brand
):
    response = client.get(
        '/api/v1/brands/',
        headers=auth_headers,
        params={'search': 'hon', 'is_active': False, 'limit': 10},
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['offset'] == 0
    assert data['limit'] == 10
    assert len(data['brands']) == 1
    assert data['brands'][0]['id'] == second_brand.id


def test_get_brand_success(client, auth_headers, brand):
    response = client.get(
        f'/api/v1/brands/{brand.id}',
        headers=auth_headers,
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['id'] == brand.id
    assert data['name'] == brand.name


def test_get_brand_error_404(client, auth_headers):
    response = client.get('/api/v1/brands/999', headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Marca não encontrada'


def test_update_brand_success(client, auth_headers, brand):
    response = client.put(
        f'/api/v1/brands/{brand.id}',
        headers=auth_headers,
        json={
            'name': 'Toyota Updated',
            'description': 'Updated description',
            'is_active': False,
        },
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['name'] == 'Toyota Updated'
    assert data['description'] == 'Updated description'
    assert data['is_active'] is False


def test_update_brand_error_400_duplicate_name(
    client, auth_headers, brand, second_brand
):
    response = client.put(
        f'/api/v1/brands/{brand.id}',
        headers=auth_headers,
        json={'name': second_brand.name},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Nome da marca já está em uso'


def test_update_brand_error_404(client, auth_headers):
    response = client.put(
        '/api/v1/brands/999',
        headers=auth_headers,
        json={'name': 'Missing'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Marca não encontrada'


def test_update_brand_error_422_invalid_payload(
    client, auth_headers, brand
):
    response = client.put(
        f'/api/v1/brands/{brand.id}',
        headers=auth_headers,
        json={'name': 'a'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_brand_success(client, auth_headers, brand):
    response = client.delete(
        f'/api/v1/brands/{brand.id}',
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b''


def test_delete_brand_error_404(client, auth_headers):
    response = client.delete('/api/v1/brands/999', headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Marca não encontrada'


def test_delete_brand_error_400_with_associated_cars(
    client, auth_headers, car
):
    response = client.delete(
        f'/api/v1/brands/{car.brand_id}',
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Essa marca possui carros associados'
