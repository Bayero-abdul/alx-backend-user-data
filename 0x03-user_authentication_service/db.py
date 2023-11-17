#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates and persists a new user in the database
        """
        if not isinstance(email, str) or not isinstance(hashed_password, str):
            return None

        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Filters and returns a user found by the input arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found")
            return user
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates the users attributes passed in the keyword arguments
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in User.__table__.columns:
                raise ValueError('Attribute not in User object')
            setattr(user, k, v)

        return None
