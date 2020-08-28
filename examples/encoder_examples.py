"""Examples"""

from text_encoder import Encoder
from text_encoder import StringReader, FileWriter, ConsoleWriter, StringWriter
from text_encoder import Cesar, ScalarEncryptionKey

# Typical usage

encoder = Encoder(StringReader('test me'), ConsoleWriter(), Cesar(ScalarEncryptionKey(2)))
encoder.encode()

# File as an output

file_writer = FileWriter(r'C:\Documents\encoding_output.txt')

encoder = Encoder(StringReader('test me'), file_writer, Cesar(ScalarEncryptionKey(2)))
encoder.encode()
file_writer.finish()

# String as an output

string_writer = StringWriter()

encoder = Encoder(StringReader('test me'), string_writer, Cesar(ScalarEncryptionKey(2)))
encoder.encode()
print(string_writer.get())
