# Text Encoder

Encode text provided in supported formats using one of possible encoding methods.

## Usage Examples

### Console

You can use text encoder as an imported module as well 
as from command line after adding package into ``PYTHONPATH``.

```console
C:\>python -m text_encoder --in_string="this works" --out_console --cesar --key=1 
```

### Scripts

Typical usage.

```python
from text_encoder import Encoder, StringReader, ConsoleWriter, Cesar, ScalarEncryptionKey

encoder = Encoder(StringReader('text to encode'), ConsoleWriter(), Cesar(ScalarEncryptionKey(2)))
encoder.encode()
```

If file is the output, remember about finishing file writing process.

```python
from text_encoder import Encoder, StringReader, FileWriter, Cesar, ScalarEncryptionKey

file_writer = FileWriter(r'C:\Documents\encoding_output.txt')

encoder = Encoder(StringReader('text to encode'), file_writer, Cesar(ScalarEncryptionKey(2)))
encoder.encode()
file_writer.finish()
```

If string is the output, remember to get the encoding result.

```python
from text_encoder import Encoder, StringReader, StringWriter, Cesar, ScalarEncryptionKey

string_writer = StringWriter()

encoder = Encoder(StringReader('text to encode'), string_writer, Cesar(ScalarEncryptionKey(2)))
encoder.encode()
encoded_message = string_writer.get()
```

## Supported encoding methods

* [Cesar code](https://en.wikipedia.org/wiki/Caesar_cipher)
* [Xor code](https://en.wikipedia.org/wiki/XOR_cipher)

## Supported inputs and outputs

* Console
* String
* File

## Design

### Available Encoders

![Class Diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/meeetju/text_encoder/meeetju/start/docs/design_encoders.puml)

### Encoder Structure

![Class Diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/meeetju/text_encoder/meeetju/start/docs/design_encoder.puml)

## Running the tests with coverage check

In order to enable running tests and checking
coverage execute at the command prompt:

    `pip install pytest pytest-cov`
    
To run tests and check coverage execute:

    `.\check_coverage.bat`
    
## Release history

* 1.0.0
    * First functional release
	
## License

* [LICENSE](LICENSE)
