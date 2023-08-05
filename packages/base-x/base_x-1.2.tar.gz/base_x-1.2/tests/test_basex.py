from basex import basex, BaseXAlphabetAmbiguousException, BaseXExpectedStringException, BaseXException
import json
import os
from pathlib import Path
import pytest
import re


FIXTURES_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures.json')

fixtures = json.loads(Path(FIXTURES_JSON_PATH).read_text())
alphabets = fixtures['alphabets']
valid = fixtures['valid']
invalid = fixtures['invalid']

def test_valid():
    for fixture in valid:
        alphabet = alphabets[fixture['alphabet']]
        hex = bytes(bytearray.fromhex(fixture['hex']))
        string = fixture['string']
        base = basex(alphabet)
        decoded = base.decode(string)
        encoded = base.encode(hex)
        assert decoded == hex, 'decoded from string not equals to hex'
        assert encoded == string, 'encoded from hex not equals to string'

def test_invalid():
    for fixture in invalid:
        alphabet = fixture['alphabet']
        description = fixture['description']
        exception = fixture['exception']
        regex = re.compile(exception)
        if 'string' in fixture:
            string = fixture['string']
        else:
            string = None

        if string is None:
            try:
                base = basex(alphabet)
            except BaseXAlphabetAmbiguousException as e:
                assert regex.match(str(e)), 'wrong exception raised for "{}"'.format(description)
                continue
            assert False, 'exception not raised for "{}"'.format(description)
        elif not isinstance(string, str):
            try:
                base = basex(alphabet)
                base.decode(string)
            except BaseXExpectedStringException as e:
                assert regex.match(str(e)), 'wrong exception raised for "{}"'.format(description)
                continue
            assert False, 'exception not raised for "{}"'.format(description)

        try:
            base = basex(alphabet)
            base.decode(string)
        except BaseXException as e:
            assert regex.match(str(e)), 'wrong exception raised for "{}", should be "{}", but get "{}"'.format(description, exception, str(e))
            continue
        assert False, 'exception not raised for "{}"'.format(description)
