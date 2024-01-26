#!/usr/bin/env python3
'''basci_auth module'''

from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    '''`Basic` Authentication class manager'''

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        '''Extracts the Base64 part of a Basic Authorization header
        '''
        if type(authorization_header) is str\
                and authorization_header.startswith('Basic '):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        '''Decodes the Base64 part of a Basic Authorization header
        '''
        if type(base64_authorization_header) is str:
            if base64_authorization_header.startswith('Basic '):
                b = self.extract_base64_authorization_header(
                    base64_authorization_header)
            else:
                b = base64_authorization_header
            try:
                return base64.b64decode(b).decode()
            except Exception as e:
                return None
        return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        '''Returns the user email and password from the Base64 decoded value
        '''
        if type(decoded_base64_authorization_header) is str\
                and ':' in decoded_base64_authorization_header:
            r = decoded_base64_authorization_header.split(':')
            if len(r) == 2:
                return (r[0], r[1])
            else:
                pwd = ''
                for s in r[1:]:
                    pwd += s + ':'
                return (r[0], pwd[:-1])
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        '''Returns the User instance that match the given email and password.
        '''
        if all(isinstance(var, str) for var in [user_email, user_pwd]):
            try:
                users = User.search({'email': user_email})
                if users:
                    for user in users:
                        if User.is_valid_password(user, user_pwd):
                            return user
                    return None
                return None
            except Exception as e:
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Retrieves the User object for the request
        '''
        if not request:
            return None
        authorization_header = self.authorization_header(request=request)
        if not authorization_header:
            return None
        extracted_b64_auth_header = self.extract_base64_authorization_header(
            authorization_header=authorization_header
        )
        if not extracted_b64_auth_header:
            return None
        decoded_b64_auth_header = self.decode_base64_authorization_header(
            extracted_b64_auth_header
        )
        if not decoded_b64_auth_header:
            return None
        user_credentials = self.extract_user_credentials(
            decoded_b64_auth_header
        )
        if user_credentials == (None, None):
            return None
        user = self.user_object_from_credentials(
            user_email=user_credentials[0], user_pwd=user_credentials[1])
        if not user:
            return None
        return user
