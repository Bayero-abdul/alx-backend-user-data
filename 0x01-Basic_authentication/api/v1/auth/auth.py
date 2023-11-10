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
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Attend to later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Attend to later
        """
        return None
