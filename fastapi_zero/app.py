from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}


@app.get('/users', response_model=UserList)
def read_users():
    return {'users_total': len(database), 'users': database}


@app.post('/user', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)
    return user_with_id


@app.put('/user/{id}', response_model=UserPublic)
def update_user(id: int, user: UserSchema):
    if id > len(database) or id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(id=id, **user.model_dump())
    database[id - 1] = user_with_id

    return user_with_id


@app.delete('/user/{id}', response_model=Message)
def delete_user(id: int):
    if id > len(database) or id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_deleted = database.pop(id - 1)
    return {'message': f'User [{user_deleted.username}] with id {user_deleted.id} deleted'}
