"""Resource format handlers."""

__author__ = 'Herb (herb2sy@google.com)'

import logging
from . import utils


def remove_root(data):
    if isinstance(data, dict) and len(data) == 1:
        return next(iter(data.values()))
    return data


class Error(Exception):
    """Base exception type for this module."""


class Base(object):
    """A base format object for inheritance."""


# class XMLFormat(Base):
#     """Read XML formatted ActiveResource objects."""
#
#     extension = 'xml'
#     mime_type = 'application/xml'
#
#     @staticmethod
#     def decode(resource_string):
#         """Convert a resource string to a dictionary."""
#         log = logging.getLogger('pyactiveresource.format')
#         log.debug('decoding resource: %s', resource_string)
#         try:
#             data = utils.xml_to_dict(resource_string, saveroot=False)
#         except utils.Error as err:
#             raise Error(err)
#         return remove_root(data)


class JSONFormat(Base):
    """Encode and Decode JSON formatted ActiveResource objects."""

    extension = 'json'
    mime_type = 'application/json'

    @staticmethod
    def decode(resource_string):
        """Convert a resource string to a dictionary."""
        log = logging.getLogger('pyactiveresource.format')
        log.debug('decoding resource: %s', resource_string)
        try:
            data = utils.json_to_dict(resource_string.decode('utf-8'))
        except ValueError as err:
            raise Error(err)
        return remove_root(data)

    @staticmethod
    def encode(data):
        """Convert a dictionary to a resource string."""
        log = logging.getLogger('pyactiveresource.format')
        log.debug('encoding resource: %r', data)
        return utils.to_json(data).encode('utf-8')
