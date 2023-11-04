#!/usr/bin/env python3
"""filtered_logger.py
"""

from typing import List
import mysql.connector
import re
import logging
import sys
import os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated.
    """
    joined_fields = "|".join(fields)
    output = re.sub(r'(({}))=[^{}]+'.format(joined_fields,
                    separator), r'\1={}'.format(redaction), message)
    return output


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records.
        """
        msg = super(RedactingFormatter, self).format(record)
        log = filter_datum(self._fields, self.REDACTION, msg, self.SEPARATOR)
        return log


def get_logger() -> logging.Logger:
    """Create logger for users data.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD')
    host = os.environ.get('PERSONAL_DATA_DB_HOST')
    database = os.environ.get('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connection
    cnx = connection.MySQLConnection(user=user, password=password, host=host,
                                     database=database)
    return cnx
