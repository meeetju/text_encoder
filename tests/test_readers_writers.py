"""Test readers and writers."""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=no-self-use
# pylint: disable=unused-argument
# pylint: disable=attribute-defined-outside-init

from mock import patch, mock_open, MagicMock
import pytest

from text_encoder import (StringReader, StringWriter, FileReader,
                          FileWriter, ConsoleReader, ConsoleWriter)


class TestStringReader:

    def test_string_read_returns_correct_content(self):

        _string = StringReader('test')
        read_text = ''.join(_string.read())

        assert read_text == 'test'


class TestStringWriter:

    def test_string_get_returns_correct_content(self):

        writer = StringWriter()
        writer.write('a')
        wrote_text = writer.get()

        assert wrote_text == 'a'


class TestFileReader:

    @pytest.fixture()
    def file_mock_set(self):

        with patch('builtins.open', new_callable=mock_open) as self.open_mock:
            file_ = self.open_mock.return_value
            file_.read.side_effect = ['t', 'e', 's', 't', None]
            yield

    def test_file_read_returns_correct_content(self, file_mock_set):

        _file = FileReader('path')
        read_text = ''.join(_file.read())

        assert read_text == 'test'


class TestFileWriter:

    @pytest.fixture()
    def file_mock_set(self):

        with patch('builtins.open', new_callable=mock_open) as self.open_mock:
            _file = self.open_mock.return_value
            _file.fileno.return_value = int(1)
            with patch('os.fsync', MagicMock(return_value=None)):
                yield

    def test_file_write_is_called_with_correct_content(self, file_mock_set):

        _file = FileWriter('path')
        _file.write('a')

        self.open_mock.return_value.write.assert_called_once_with('a')


class TestConsoleReader:

    @pytest.fixture()
    def console_mock_set(self):
        with patch('builtins.input', return_value='test'):
            yield

    def test_console_reader_returns_correct_content(self, console_mock_set):

        _console = ConsoleReader()
        read_console = ''.join(_console.read())

        assert read_console == 'test'


class TestConsoleWriter:

    def test_console_write_prints_out_correct_content(self, capsys):

        _console_out = ConsoleWriter()
        _console_out.write('A')

        out, _ = capsys.readouterr()

        assert out == 'A'
