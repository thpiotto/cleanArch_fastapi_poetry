from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    user = User(username='thpiotto', email='dev.thpiotto@gmail.com', password='somEpassword.123')

    session.add(user)
    session.commit()
    session.scalar(select(User).where(User.email == 'dev.thpiotto@gmail.com'))

    assert user.username == 'thpiotto'
