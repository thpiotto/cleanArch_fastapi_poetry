from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_zero.settings import Settings

app = FastAPI()
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}


@app.get('/users', response_model=UserList)
def read_users():
    return {'users_total': len(database), 'users': database}


@app.post('/user', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(incoming_user: UserSchema):
    engine = create_engine(Settings().DATABASE_URL)

    with Session(engine) as session:
        db_user = session.scalar(
            select(User).where(
                (User.username == incoming_user.username) | (User.email == incoming_user.email)
            )
        )

        if db_user:
            if db_user.username == incoming_user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, detail='This username already exists'
                )
            elif db_user.email == incoming_user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST, detail='This email already exists'
                )

        new_user = User(
            username=incoming_user.username,
            email=incoming_user.email,
            password=incoming_user.password,
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    return new_user


@app.put('/user/{id}', response_model=UserPublic)
def update_user(id: int, user: UserSchema):
    if id > len(database) or id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    user_with_id = UserDB(id=id, **user.model_dump())
    database[id - 1] = user_with_id

    return user_with_id


@app.delete('/user/{id}', response_model=Message)
def delete_user(id: int):
    if id > len(database) or id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    user_deleted = database.pop(id - 1)
    return {'message': f'User [{user_deleted.username}] with id {user_deleted.id} deleted'}
