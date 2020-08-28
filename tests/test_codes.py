"""Test codes and codes' keys."""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=no-self-use


from text_encoder import Cesar, Xor, IterableEncryptionKey, ScalarEncryptionKey
from text_encoder._printables import ascii_codes_table_size


class TestCesar:

    def test_cesar_encodes_printables_properly_with_positive_key(self):
        cesar = Cesar(ScalarEncryptionKey(3))
        result = cesar.encode_char('a')
        assert result == 'd'

    def test_cesar_encodes_printables_properly_with_negative_key(self):
        cesar = Cesar(ScalarEncryptionKey(-3))
        result = cesar.encode_char('a')
        assert result == '^'

    def test_cesar_encodes_printables_properly_with_positive_rollover(self):
        cesar = Cesar(ScalarEncryptionKey(7))
        result = cesar.encode_char('z')
        assert result == '"'

    def test_cesar_encodes_printables_properly_with_positive_multiple_rollover(self):
        cesar = Cesar(ScalarEncryptionKey(2 * ascii_codes_table_size + 7))
        result = cesar.encode_char('z')
        assert result == '"'

    def test_cesar_encodes_printables_properly_with_negative_rollover(self):
        cesar = Cesar(ScalarEncryptionKey(-7))
        result = cesar.encode_char('&')
        assert result == '~'

    def test_cesar_encodes_printables_properly_with_negative_multiple_rollover(self):
        cesar = Cesar(ScalarEncryptionKey(-2 * ascii_codes_table_size - 7))
        result = cesar.encode_char('&')
        assert result == '~'


class TestXor:

    def test_xor_encodes_printable_properly(self):
        xor = Xor(ScalarEncryptionKey(3))
        result = xor.encode_char('a')
        assert result == 'b'


class TestIterableEncryptionKey:

    def test_iterator_is_looped(self):
        i = IterableEncryptionKey([1, 2, 3])
        assert i.get() == 1
        assert i.get() == 2
        assert i.get() == 3
        assert i.get() == 1


class TestScalarEncryptionKey:

    def test_key_is_converted_to_int(self):
        k = ScalarEncryptionKey('1')
        assert k.get() == 49

    def test_key_stays_int(self):
        k = ScalarEncryptionKey(1)
        assert k.get() == 1
