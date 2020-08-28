"""Set of printable characters."""

from string import ascii_letters, digits, punctuation

ASCII_PRINTABLES_CHARS = r""" {0}{1}{2}""".format(digits, ascii_letters, punctuation)
_ascii_printables_codes = [ord(printable) for printable in ASCII_PRINTABLES_CHARS]

_ascii_printables_codes.sort()
min_ascii_code = _ascii_printables_codes[0]
max_ascii_code = _ascii_printables_codes[-1]

ascii_codes_table_size = len(_ascii_printables_codes)

ascii_printables_codes = _ascii_printables_codes
