#!/usr/bin/env python3
"""filtered_logger.py
"""

from typing import List
import re
import logging
import sys


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
