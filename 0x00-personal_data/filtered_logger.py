#!/usr/bin/env python3
"""filtered_logger.py
"""

from typing import List
import re


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
