#!/usr/bin/env python3
"""Auth module
"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
