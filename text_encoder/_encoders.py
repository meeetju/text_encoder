"""Encoders."""
# pylint: disable=too-few-public-methods

from abc import abstractmethod, ABC

from text_encoder._utils import time_it


class BaseEncoder(ABC):

    """Encoder interface."""

    @abstractmethod
    def encode(self, stop_predicate):
        """This method shall be implemented."""


class Encoder(BaseEncoder):

    """Encode input from reader."""

    def __init__(self, reader, writer, coder):
        self._reader = reader
        self._writer = writer
        self._coder = coder

    def _encode(self, char):
        return self._coder.encode_char(char)

    @time_it
    def encode(self, stop_predicate=lambda x: False):
        """Encode input from reader.

        :param stop_predicate: predicate
        :type stop_predicate: function

        """
        for char in self._reader.read():
            encoded_char = self._encode(char)
            self._writer.write(encoded_char)
            if stop_predicate(char):
                return


class NullCoder(BaseEncoder):

    """Rewrite reader input to output."""

    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer

    def encode(self, stop_predicate=lambda x: False):
        """Rewrite reader input to output until stop condition is met.

        :param stop_predicate: predicate
        :type stop_predicate: function

        """
        for char in self._reader.read():
            self._writer.write(char)
            if stop_predicate(char):
                return


class HeadedEncoder(BaseEncoder):

    """Encode body, leaving header not encoded."""

    def __init__(self, header_encoder, body_encoder, is_end_of_header_predicate):
        self._header_encoder = header_encoder
        self._body_encoder = body_encoder
        self._is_end_of_header_predicate = is_end_of_header_predicate
        self._is_end_of_header_reached = False

    def _is_end_of_header(self, char):
        self._is_end_of_header_reached = self._is_end_of_header_predicate(char)
        return self._is_end_of_header_reached

    def encode(self, stop_predicate=lambda x: False):
        """Encode body."""
        self._header_encoder.encode(lambda x: stop_predicate(x) or self._is_end_of_header(x))
        if self._is_end_of_header_reached:
            self._body_encoder.encode(stop_predicate)
