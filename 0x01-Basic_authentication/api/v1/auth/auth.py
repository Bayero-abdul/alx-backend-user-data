#!/usr/bin/env python3
""" Auth.py
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Defines which routes don't need authentication
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Validates all requests to secure the AP
        """
        if request is None:
            return None

        if request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Attend to later
        """
        return None
