from fastapi import status


def car_payload(car_data, brand, user, **overrides):
    payload = {
        **car_data,
        'brand_id': brand.id,
        'owner_id': user.id,
    }
    payload.update(overrides)
    return payload


def test_create_car_success(client, auth_headers, car_data, brand, user):
    response = client.post(
        '/api/v1/cars/',
        headers=auth_headers,
        json=car_payload(car_data, brand, user),
    )

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data['model'] == car_data['model']
    assert data['plate'] == car_data['plate']
    assert data['brand']['id'] == brand.id
    assert data['owner']['id'] == user.id


def test_create_car_error_400_duplicate_plate(
    client, auth_headers, car, car_data, brand, user
):
    response = client.post(
        '/api/v1/cars/',
        headers=auth_headers,
        json=car_payload(car_data, brand, user),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Placa já está em uso'


def test_create_car_error_400_missing_brand(
    client, auth_headers, car_data, user
):
    response = client.post(
        '/api/v1/cars/',
        headers=auth_headers,
        json={**car_data, 'brand_id': 999, 'owner_id': user.id},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Marca não encontrada'


def test_create_car_error_400_missing_owner(
    client, auth_headers, car_data, brand
):
    response = client.post(
        '/api/v1/cars/',
        headers=auth_headers,
        json={**car_data, 'brand_id': brand.id, 'owner_id': 999},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Proprietario não encontrada'


def test_create_car_error_422_invalid_payload(
    client, auth_headers, car_data, brand, user
):
    response = client.post(
        '/api/v1/cars/',
        headers=auth_headers,
        json=car_payload(
            car_data,
            brand,
            user,
            model='A',
            plate='ABC',
            price='0',
            factory_year=1700,
        ),
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_car_error_422_invalid_color(
    client, auth_headers, car_data, brand, user
):
    response = client.post(
        '/api/v1/cars/',
        headers=auth_headers,
        json=car_payload(car_data, brand, user, color='A'),
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_car_without_authentication(client, car_data, brand, user):
    response = client.post(
        '/api/v1/cars/',
        json=car_payload(car_data, brand, user),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_cars_success_with_filters(
    client, auth_headers, car, second_car, brand
):
    response = client.get(
        '/api/v1/cars/',
        headers=auth_headers,
        params={
            'search': 'cor',
            'brand_id': brand.id,
            'fuel_type': car.fuel_type,
            'transmission': car.transmission,
            'is_available': True,
            'min_price': 100000,
            'max_price': 140000,
            'limit': 10,
        },
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['offset'] == 0
    assert data['limit'] == 10
    assert len(data['cars']) == 1
    assert data['cars'][0]['id'] == car.id


def test_list_cars_filters_by_owner(
    client, auth_headers, car, second_user
):
    response = client.get(
        '/api/v1/cars/',
        headers=auth_headers,
        params={'owner_id': second_user.id},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['cars'] == []


def test_list_cars_only_returns_current_user_cars(
    client,
    auth_headers,
    second_auth_headers,
    car,
    car_data,
    brand,
    second_user,
):
    client.post(
        '/api/v1/cars/',
        headers=second_auth_headers,
        json=car_payload(
            car_data,
            brand,
            second_user,
            model='Fit',
            plate='DEF2G34',
        ),
    )

    response = client.get('/api/v1/cars/', headers=auth_headers)

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert [item['id'] for item in data['cars']] == [car.id]


def test_get_car_success(client, auth_headers, car):
    response = client.get(f'/api/v1/cars/{car.id}', headers=auth_headers)

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['id'] == car.id
    assert data['brand']['id'] == car.brand_id
    assert data['owner']['id'] == car.owner_id


def test_get_car_error_404(client, auth_headers):
    response = client.get('/api/v1/cars/999', headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Carro não encontrado'


def test_get_car_error_403_for_non_owner(
    client, second_auth_headers, car
):
    response = client.get(
        f'/api/v1/cars/{car.id}',
        headers=second_auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == (
        'Not enough permissions to access this car'
    )


def test_update_car_success(
    client, auth_headers, car, second_brand, second_user
):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers=auth_headers,
        json={
            'model': 'Corolla Cross',
            'factory_year': 2025,
            'model_year': 2026,
            'color': 'Gray',
            'plate': 'NEW1A23',
            'transmission': 'cvt',
            'price': '160000.00',
            'description': 'SUV',
            'is_available': False,
            'brand_id': second_brand.id,
            'owner_id': second_user.id,
        },
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['model'] == 'Corolla Cross'
    assert data['plate'] == 'NEW1A23'
    assert data['brand_id'] == second_brand.id
    assert data['owner_id'] == second_user.id
    assert data['is_available'] is False


def test_update_car_error_400_duplicate_plate(
    client, auth_headers, car, second_car
):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers=auth_headers,
        json={'plate': second_car.plate},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Placa já está em uso'


def test_update_car_error_400_missing_brand(
    client, auth_headers, car
):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers=auth_headers,
        json={'brand_id': 999},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Marca não encontrada'


def test_update_car_error_400_missing_owner(
    client, auth_headers, car
):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers=auth_headers,
        json={'owner_id': 999},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Proprietário não encontrado'


def test_update_car_error_403_for_non_owner(
    client, second_auth_headers, car
):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers=second_auth_headers,
        json={'model': 'Blocked Update'},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == (
        'Not enough permissions to access this car'
    )


def test_update_car_error_404(client, auth_headers):
    response = client.put(
        '/api/v1/cars/999',
        headers=auth_headers,
        json={'model': 'Missing'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Carro não encontrado'


def test_update_car_error_422_invalid_payload(
    client, auth_headers, car
):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers=auth_headers,
        json={'price': '0'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_car_error_422_invalid_fields(
    client, auth_headers, car
):
    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers=auth_headers,
        json={
            'model': 'A',
            'color': 'B',
            'plate': 'ABC',
            'factory_year': 1700,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_car_success(client, auth_headers, car):
    response = client.delete(f'/api/v1/cars/{car.id}', headers=auth_headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b''


def test_delete_car_error_403_for_non_owner(
    client, second_auth_headers, car
):
    response = client.delete(
        f'/api/v1/cars/{car.id}',
        headers=second_auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == (
        'Not enough permissions to access this car'
    )


def test_delete_car_error_404(client, auth_headers):
    response = client.delete('/api/v1/cars/999', headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Carro não encontrado'
