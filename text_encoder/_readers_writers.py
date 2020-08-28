"""Set of text readers and writers."""
# pylint: disable=too-few-public-methods

from abc import abstractmethod, ABC
from os import fsync
import sys


from text_encoder._encoding_process import EncodingDoneObserver


class Reader(ABC):

    """Reader interface."""

    @abstractmethod
    def read(self):
        """This method shall be implemented."""


class StringReader(Reader):

    """Read string."""

    def __init__(self, input_string):
        self._char_iterator = self._get_char(input_string)

    def read(self):
        """Read string one byte at a time.

        :return: char_iterator
        :rtype: iterator
        """
        return self._char_iterator

    @staticmethod
    def _get_char(string):
        for char in string:
            yield char


class FileReader(Reader):

    """Read file one byte at a time."""

    def __init__(self, path):
        self._char_iterator = self._get_char_from_file(path)

    @staticmethod
    def _get_char_from_file(path):
        with open(path, 'rb') as file:
            while True:
                char = file.read(1)
                if char:
                    yield char
                else:
                    break  # pragma no cover

    def read(self):
        """Read file one byte at a time.

        :return: char_iterator
        :rtype: iterator
        """
        return self._char_iterator


class ConsoleReader(Reader):

    """Read console."""

    def __init__(self):
        self._char_iterator = self._get_char(input("Provide text to encode: "))

    def read(self):
        """Read console input one byte at a time.

        :return: char_iterator
        :rtype: iterator
        """
        return self._char_iterator

    @staticmethod
    def _get_char(string):
        for char in string:
            yield char


class Writer(ABC):

    """Writer interface."""

    @abstractmethod
    def write(self, _input):
        """This method shall be implemented."""


class StringWriter(Writer):

    """Write text to string output."""

    def __init__(self):
        self._output = []

    def write(self, _input):
        """Write letter to string"""
        self._output.append(_input)

    def get(self):
        """Get full string output.

        :return: string output
        :rtype: str
        """
        return ''.join(self._output)


class FileWriter(Writer, EncodingDoneObserver):

    """Write text to file output."""

    def __init__(self, path):
        self._file = open(path, 'w')

    def write(self, _input):
        """Write letter to file."""
        self._file.write(_input)
        self._file.flush()
        fsync(self._file.fileno())

    def finish(self):
        """Finish file operations."""
        self._file.close()


class ConsoleWriter(Writer):

    """Write text to console output."""

    def write(self, _input):
        """Write letter to console."""
        sys.stdout.write(_input)
        sys.stdout.flush()
