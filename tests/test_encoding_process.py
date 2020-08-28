"""Test encoding process."""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=no-self-use
# pylint: disable=unused-argument
# pylint: disable=attribute-defined-outside-init

from mock import patch, mock_open, MagicMock, call
import pytest

from text_encoder import Cesar, Xor, ScalarEncryptionKey
from text_encoder import Encoder, HeadedEncoder, NullCoder
from text_encoder.__main__ import main
from text_encoder import StringReader, StringWriter, FileReader, FileWriter
from text_encoder._encoding_process import EncodingDoneObservable


class TestEncoder:

    @pytest.fixture()
    def file_read_mock(self):

        with patch('builtins.open', new_callable=mock_open) as self.open_mock:
            file_ = self.open_mock.return_value
            file_.read.side_effect = ['t', 'e', 's', 't', ' ', 'm', 'e', None]
            file_.fileno.return_value = int(1)
            with patch('os.fsync', MagicMock(return_value=None)):
                yield

    def test_not_printable_char_is_not_cesar_encoded(self):

        null = chr(0x01)
        string_writer = StringWriter()

        encoder = Encoder(StringReader('a{}c'.format(null)), string_writer,
                          Cesar(ScalarEncryptionKey(2)))
        encoder.encode()
        result_string = string_writer.get()

        assert result_string == 'c{}e'.format(null)

    def test_string_is_cesar_encoded_to_string(self):

        string_writer = StringWriter()

        encoder = Encoder(StringReader('test me'), string_writer, Cesar(ScalarEncryptionKey(2)))
        encoder.encode()
        result_string = string_writer.get()

        assert result_string == 'vguv"og'

    def test_file_is_cesar_encoded_to_string(self, file_read_mock):

        string_writer = StringWriter()

        encoder = Encoder(FileReader('path'), string_writer, Cesar(ScalarEncryptionKey(2)))
        encoder.encode()
        result_string = string_writer.get()

        assert result_string == 'vguv"og'

    def test_string_is_cesar_encoded_to_file(self, file_read_mock):

        file_writer = FileWriter('path')

        encoder = Encoder(StringReader('test'),
                          file_writer,
                          Cesar(ScalarEncryptionKey(2)))
        encoder.encode()
        file_writer.finish()

        calls = [call('v'), call('g'), call('u'), call('v')]

        self.open_mock.return_value.write.assert_has_calls(calls)
        self.open_mock.return_value.close.assert_called_once()

    def test_string_is_xor_encoded_to_string(self):

        string_writer = StringWriter()

        encoder = Encoder(StringReader('test me'), string_writer, Xor(ScalarEncryptionKey(3)))
        encoder.encode()
        result_string = string_writer.get()

        assert result_string == 'wfpw#nf'

    def test_header_is_not_encoded(self):

        string_reader = StringReader('some header \n test me')
        string_writer = StringWriter()
        coder = Xor(ScalarEncryptionKey(3))
        is_end_of_header = lambda x: x == '\n'

        header_rewriter = NullCoder(string_reader, string_writer)
        body_encoder = Encoder(string_reader, string_writer, coder)

        encoder = HeadedEncoder(header_rewriter, body_encoder, is_end_of_header)
        encoder.encode()
        result_string = string_writer.get()

        assert result_string == 'some header \n#wfpw#nf'

    def test_encoding_stopped_on_header(self):

        string_reader = StringReader('some header \n test me')
        string_writer = StringWriter()
        coder = Xor(ScalarEncryptionKey(3))
        is_end_of_header = lambda x: x == '\n'

        header_rewriter = NullCoder(string_reader, string_writer)
        body_encoder = Encoder(string_reader, string_writer, coder)

        encoder = HeadedEncoder(header_rewriter, body_encoder, is_end_of_header)
        encoder.encode(lambda x: x == 'd')
        result_string = string_writer.get()

        assert result_string == 'some head'

    def test_encoding_is_stopped_on_stop_predicate(self):

        string_reader = StringReader('aaaaabccccc')
        strint_writer = StringWriter()
        coder = Cesar(ScalarEncryptionKey(1))
        is_end_of_encoding = lambda x: x == 'b'

        encoder = Encoder(string_reader, strint_writer, coder)
        encoder.encode(is_end_of_encoding)
        result_string = strint_writer.get()

        assert result_string == 'bbbbbc'


class TestNullEncoder:

    @staticmethod
    def test_null_encoder_does_not_encode():

        string_reader = StringReader('test')
        string_writer = StringWriter()

        null_coder = NullCoder(string_reader, string_writer)
        null_coder.encode(stop_predicate=lambda x: x == '\n')
        result_string = string_writer.get()

        assert result_string == 'test'


class TestMain:

    @pytest.fixture()
    def sysargv_mock(self):
        with patch('sys.argv',
                   ['main', '--in_string=this works', '--out_console', '--cesar', '--key=1']):
            yield

    def test_string_is_cesar_with_scalar_key_encoded_to_console(self, sysargv_mock, capsys):

        main()
        out, _ = capsys.readouterr()

        assert out == "uijt!xpslt"

    @pytest.fixture()
    def sysargv_int_keys_list_mock(self):
        with patch('sys.argv',
                   ['main', '--in_string=this works', '--out_console',
                    '--cesar', '--keys_int=1,1,1']):
            yield

    def test_string_is_cesar_with_keys_list_encoded_to_console(self, sysargv_int_keys_list_mock,
                                                               capsys):

        main()
        out, _ = capsys.readouterr()

        assert out == "uijt!xpslt"

    @pytest.fixture()
    def sysargv_in_out_consoles_mock(self):
        with patch('sys.argv', ['main', '--in_console', '--out_console', '--cesar', '--key=3']):
            with patch('builtins.input', return_value='abc'):
                yield

    def test_console_input_is_cesar_encoded_to_console(self, sysargv_in_out_consoles_mock, capsys):

        main()
        out, _ = capsys.readouterr()

        assert out == "def"

    @pytest.fixture()
    def sysargv_in_file_mock(self):
        # pylint: disable=line-too-long
        with patch('sys.argv', ['main', '--in_file=c/in_file.txt', '--out_console', '--cesar', '--key_text=abc']):
            with patch('builtins.open', new_callable=mock_open) as self.open_mock:
                _file = self.open_mock.return_value
                _file.read.side_effect = ['a', 'b', 'c', None]
                yield

    def test_file_is_cesar_with_char_keys_encoded_to_console(self, sysargv_in_file_mock, capsys):

        main()
        out, _ = capsys.readouterr()

        assert out == "ceg"

    @pytest.fixture()
    def sysargv_out_file_mock(self):
        # pylint: disable=line-too-long
        with patch('sys.argv', ['main', '--in_string=abc', '--out_file=c/out_file.txt', '--cesar', '--key_text=abc']):
            with patch('builtins.open', new_callable=mock_open) as self.open_mock:
                self.open_mock.return_value.fileno.return_value = int(1)
                with patch('os.fsync', MagicMock(return_value=None)):
                    yield

    def test_string_is_cesar_with_char_keys_encoded_to_file(self, sysargv_out_file_mock):
        main()

        calls = [call('c'), call('e'), call('g')]

        self.open_mock.return_value.write.assert_has_calls(calls)
        self.open_mock.return_value.close.assert_called_once()

    @pytest.fixture()
    def sysargv_headed_input_mock(self):
        # pylint: disable=line-too-long
        with patch('sys.argv', ['main', '--in_string=aaa\naaa', '--out_console', '--xor', '--key=3', '--headed']):
            yield

    def test_string_is_cesar_encoded_except_for_header_to_console(self, sysargv_headed_input_mock,
                                                                  capsys):

        main()
        out, _ = capsys.readouterr()

        assert out == "aaa\nbbb"

    @pytest.fixture()
    def sysargv_no_reader_mock(self):
        with patch('sys.argv',
                   ['main', '--out_console', '--cesar', '--key=1']):
            yield

    def test_runtime_error_raised_if_no_input_provided(self, sysargv_no_reader_mock):

        with pytest.raises(RuntimeError) as error:
            main()

        assert 'No reader provided.' in error.value.args

    @pytest.fixture()
    def sysargv_no_writer_mock(self):
        with patch('sys.argv',
                   ['main', '--in_string=abc', '--cesar', '--key=1']):
            yield

    def test_runtime_error_raised_if_no_output_provided(self, sysargv_no_writer_mock):

        with pytest.raises(RuntimeError) as error:
            main()

        assert 'No writer provided.' in error.value.args

    @pytest.fixture()
    def sysargv_no_coder_mock(self):
        with patch('sys.argv',
                   ['main', '--in_string=abc', '--out_console', '--key=1']):
            yield

    def test_runtime_error_raised_if_no_coder_provided(self, sysargv_no_coder_mock):

        with pytest.raises(RuntimeError) as error:
            main()

        assert 'No coder provided.' in error.value.args

    @pytest.fixture()
    def sysargv_no_key_mock(self):
        with patch('sys.argv',
                   ['main', '--in_string=abc', '--out_console', '--cesar']):
            yield

    def test_runtime_error_raised_if_no_key_provided(self, sysargv_no_key_mock):

        with pytest.raises(RuntimeError) as error:
            main()

        assert 'No key nor key_vector provided.' in error.value.args


class TestObservable:

    """Test Encoding Done Observable"""

    def test_exception_is_raised_if_not_observer_registered(self):

        with pytest.raises(TypeError) as error:
            EncodingDoneObservable().register_observer('observer')

        assert 'Not ProcessDoneObserver type' in error.value.args
