#!/usr/bin/env python3
"""encrypt_password.py
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypts passwords.
    """
    hashed = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks for valid password.
    """
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password
    )
