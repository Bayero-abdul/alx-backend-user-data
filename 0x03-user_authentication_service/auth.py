#!/usr/bin/env python3
"""Auth module
"""

import bcrypt
import uuid
from db import DB
from typing import Union
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _generate_uuid() -> str:
    """Generates a new UUID string
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Instantiate an auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user in the database
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            new_user = User(
                email=email,
                hashed_password=_hash_password(password))
            self._db._session.add(new_user)
            self._db._session.commit()
            return new_user

        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates the password if the email exists in the database
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
        except NoResultFound:
            return False

        return False

    def create_session(self, email: str) -> str:
        """find the user corresponding to the email, generate a new
        UUID and store it in the database as the user’s session_id
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                setattr(user, 'session_id', session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Finds user by session ID
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None

        return user if user else None

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user’s session ID to None
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        if user and hasattr(user, 'session_id'):
            setattr(user, 'session_id', None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                setattr(user, 'reset_token', reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_password = _hash_password(password)
                setattr(user, 'hashed_password', hashed_password)
                setattr(user, 'reset_token', None)
        except (NoResultFound, InvalidRequestError):
            raise ValueError()
