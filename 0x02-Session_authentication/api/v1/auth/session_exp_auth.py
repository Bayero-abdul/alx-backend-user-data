#!/usr/bin/env python3
'''session_exp_auth module'''
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''Representation of an expiration session authentication class
    '''

    def __init__(self):
        '''Initializes a new SessionExpAuth object
        '''
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''Creates a session and returns the session ID'''

        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''Returns a user_id based on the session_id
        '''
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id, None)
        if not session_dictionary or type(session_dictionary) is not dict:
            return None
        user_id = session_dictionary.get('user_id', None)
        created_at = session_dictionary.get('created_at', None)
        if not user_id:
            return None
        if self.session_duration <= 0:
            return user_id
        if not created_at:
            return None
        time_delta = timedelta(seconds=self.session_duration)
        time_passed = time_delta + created_at
        if time_passed < datetime.now():
            return None
        return user_id
