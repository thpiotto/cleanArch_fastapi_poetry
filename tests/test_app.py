from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


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


def test_delete_user_OK(client):
    response = client.delete('/user/1')  # Act

    user_deleted = UserPublic(id=1, username='testname', email='testemail@email.com')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': f'User [{user_deleted.username}] with id {user_deleted.id} deleted'
    }


def test_delete_user_NOT_FOUND(client):
    response = client.delete('/user/2')  # Act

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
