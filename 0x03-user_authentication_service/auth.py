#!/usr/bin/env python3
"""Auth module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
            return self._db.add_user(email, _hash_password(password))

        raise ValueError("User {} already exists".format(email))
