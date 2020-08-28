"""Set of letter coders"""
# pylint: disable=too-few-public-methods

from abc import abstractmethod, ABC

from text_encoder._printables import (min_ascii_code, max_ascii_code, ascii_printables_codes,
                                      ascii_codes_table_size, ASCII_PRINTABLES_CHARS)


def _get_in_int_format(key):
    if isinstance(key, int):
        return key
    return ord(key)


class Coder(ABC):

    """Coder interface."""

    @abstractmethod
    def encode_char(self, char):
        """This method shall be implemented."""


class Cesar(Coder):

    """Encode letter with Cesar code."""

    def __init__(self, key):
        self._cesar_key = key

    def encode_char(self, _char):
        if _char in ASCII_PRINTABLES_CHARS:
            return chr(self._get_new_ascii_code(_char))
        return _char

    def _get_new_ascii_code(self, _char):
        current_code = ord(_char)
        cesar_key = self._normalize_key(self._cesar_key.get())
        new_index = ascii_printables_codes.index(current_code) + cesar_key
        if new_index > ascii_printables_codes.index(max_ascii_code):
            return ascii_printables_codes[new_index - ascii_codes_table_size]
        if new_index < ascii_printables_codes.index(min_ascii_code):
            return ascii_printables_codes[ascii_codes_table_size + new_index]
        return ascii_printables_codes[new_index]

    @staticmethod
    def _normalize_key(key):
        if abs(key) >= ascii_codes_table_size:
            return (abs(key) % ascii_codes_table_size) * int(abs(key) / key)
        return key


class Xor(Coder):

    """Encode letter with Xor code."""

    def __init__(self, key):
        self._xor_key = key

    def encode_char(self, _char):
        return self._change_char_by_xor_key(_char)

    def _change_char_by_xor_key(self, _char):
        return chr(ord(_char) ^ self._xor_key.get())


class EncryptionKey(ABC):

    """Encryption Key Interface."""

    @abstractmethod
    def get(self):
        """This method shall be implemented."""


class ScalarEncryptionKey(EncryptionKey):

    """Scalar encryption key."""

    def __init__(self, key):
        self._initial_key = key

    def get(self):
        """Get encryption key in int format."""
        return _get_in_int_format(self._initial_key)


class IterableEncryptionKey(EncryptionKey):

    """Iterable Encryption Key."""

    def __init__(self, key):
        self._initial_key = key
        self._key_iterator = self._get_next_key()

    def _get_next_key(self):
        for k in self._initial_key:
            yield _get_in_int_format(k)

    def get(self):
        """Get encryption key in int format."""
        try:
            return self._key_iterator.__next__()
        except StopIteration:
            self._key_iterator = self._get_next_key()
            return self._key_iterator.__next__()
