#!/usr/bin/env python3
'''session_auth module'''

from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    '''New authentication mechanism for simulating Users Sessions'''

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Creates a new Session ID for a user_id'''
        if not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4().__str__()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Returns a User ID based on the session_id'''
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        '''Retrieves the User object based on a cookie value'''
        session_id_from_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id_from_cookie)
        return User.get(user_id) if User.get(user_id) else None

    def destroy_session(self, request=None):
        '''Deletes a user session from the request. This implements the logout
        '''
        if not request:
            return False
        session_id_from_cookie = self.session_cookie(request)
        if not session_id_from_cookie:
            return False
        user_id = self.user_id_for_session_id(session_id_from_cookie)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id_from_cookie]
        return True
