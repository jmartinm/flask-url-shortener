"""Utility functions used in URL Shortener."""

import re
import math


URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
# Extracted from Django URL Validation
# https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45


def is_url_valid(url):
    return bool(URL_REGEX.match(url))


##### Conversion from decimal to base62 and reverse ######

UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61
DIGIT_OFFSET = 48


def true_ord(char):
    """
    Turns a digit in character representation
    from the number system with base 62 into an integer.
    """
    
    if char.isdigit():
        return ord(char) - DIGIT_OFFSET
    elif 'A' <= char <= 'Z':
        return ord(char) - UPPERCASE_OFFSET
    elif 'a' <= char <= 'z':
        return ord(char) - LOWERCASE_OFFSET
    else:
        raise ValueError("%s is not a valid character" % char)


def true_chr(integer):
    """
    Turns an integer into digit in base 62
    as a character representation.
    """
    if integer < 10:
        return chr(integer + DIGIT_OFFSET)
    elif 10 <= integer <= 35:
        return chr(integer + UPPERCASE_OFFSET)
    elif 36 <= integer < 62:
        return chr(integer + LOWERCASE_OFFSET)
    else:
        raise ValueError("%d is not a valid integer in the range of base 62" % integer)


def base62_to_integer(key):
    """
    Turn the base 62 number key into an integer.

    Used to convert the hashed URL into the id in the database
    """
    int_sum = 0
    reversed_key = key[::-1]
    for idx, char in enumerate(reversed_key):
        int_sum += true_ord(char) * int(math.pow(62, idx))
    return int_sum


def integer_to_base62(integer):
    """
    Turn an integer into a base 62 number
    in string representation
    """

    # we won't step into the while if integer is 0
    # so we just solve for that case here
    if integer == 0:
        return '0'

    string = ""
    while integer > 0:
        remainder = integer % 62
        string = true_chr(remainder) + string
        integer /= 62
    return string
