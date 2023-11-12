#!/usr/bin/env python3
""" basic_auth.py
"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ Basic authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Returns the Base64 part of the authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_auth_header = base64.b64decode(base64_authorization_header)
        except Exception:
            return None

        return base64_auth_header.decode()
