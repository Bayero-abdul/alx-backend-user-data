#!/usr/bin/env python3
"""Auth.py
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Attend to later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Attend to later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Attend to later
        """
        return None
