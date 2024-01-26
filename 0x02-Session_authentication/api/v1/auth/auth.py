#!/usr/bin/env python3
'''auth module'''

import os
from flask import request
from typing import List, TypeVar


class Auth:
    '''API Authentication class manager'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''A path requires authorization if it is not in the list of excluded
        paths. All paths that are in the excluded paths don't need
        authorization to be accessed.
        '''

        if not path or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and \
                    path.startswith(excluded_path[:-1]) or \
                    excluded_path in [path, path + '/']:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''authorization_header method'''
        if not request:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''current_user method'''
        return None

    def session_cookie(self, request=None):
        '''Returns a session cookie value from a request'''
        if not request:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME', None), None)
