from http import HTTPStatus


def test_read_root_return_OK_and_message(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Hello World!'}  # Assert


def test_create_user(client):
    response = client.post(
        '/user',
        json={
            'username': 'testname',
            'email': 'email@test.com',
            'password': 'senha.123',
        },
    )  # Act

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testname',
        'email': 'email@test.com',
    }


def test_read_users(client):
    response = client.get('/users')  # Act

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users_total': 1,
        'users': [
            {
                'id': 1,
                'username': 'testname',
                'email': 'email@test.com',
            }
        ],
    }


def test_update_user_OK(client):
    response = client.put(
        '/user/1',
        json={
            'username': 'testname',
            'email': 'email@test.com',
            'password': 'senha.123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testname',
        'email': 'email@test.com',
    }


def test_update_user_NOT_FOUND(client):
    response = client.put(
        '/user/10000',
        json={
            'username': 'testname',
            'email': 'email@test.com',
            'password': 'senha.123',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
