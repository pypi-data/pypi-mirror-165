import math
import importlib.util
import sys
import os


def lazy_import(name, package=None):
     spec = importlib.util.find_spec(name, package)
     loader = importlib.util.LazyLoader(spec.loader)
     spec.loader = loader
     module = importlib.util.module_from_spec(spec)
     sys.modules[name] = module
     loader.exec_module(module)
     return module

class BaseXException(Exception):
    """Base class for basex exceptions"""
    pass

class BaseXAlphabetTooLongException(BaseXException):
    """Raised when the input alphabet is too large"""
    def __str__(self):
        return 'Alphabet too long'


class BaseXAlphabetAmbiguousException(BaseXException):
    """Raised when the input alphabet is malformed"""
    def __init__(self, char=''):
        self.char = char

    def __str__(self):
        return 'TypeError: {} is ambiguous'.format(self.char)


class BaseXNotInAlphabetException(BaseXException):
    """Raised when the input contains characters not in alphabet"""
    def __init__(self, base=58):
        self.base = base

    def __str__(self):
        return 'Error: Non-base{} character'.format(self.base)

class BaseXExpectedStringException(BaseXException):
    """Raised when the input is not a string"""
    def __str__(self):
        return 'TypeError: Expected String'

class basex:
    def __init__(self, alphabet):
        if len(alphabet) >= 255:
            raise BaseXAlphabetTooLongException()
        self.base_map = bytearray([255] * 256)
        for i in range(len(alphabet)):
            if self.base_map[ord(alphabet[i])] != 255:
                raise BaseXAlphabetAmbiguousException(alphabet[i])
            self.base_map[ord(alphabet[i])] = i
        self.alphabet = alphabet
        self.base = len(alphabet)
        self.leader = alphabet[0]
        self.factor = math.log(self.base, 256)
        self.ifactor = math.log(256, self.base)

    def encode(self, source):
        if len(source) == 0:
            return ''

        zeroes = 0
        length = 0
        pbegin = 0
        pend = len(source)
        while pbegin != pend and source[pbegin] == 0:
            pbegin += 1
            zeroes += 1

        # Allocate enough space in big-endian base58 representation.
        size = int((pend - pbegin) * self.ifactor + 1)
        b58 = bytearray([0] * size)
        # Process the bytes
        while pbegin != pend:
            carry = source[pbegin]
            # Apply "b58 = b58 * 256 + ch".
            i = 0
            it1 = size - 1
            while (carry != 0 or i < length) and (it1 != -1):
                carry += int(256 * b58[it1])
                b58[it1] = int(carry % self.base)
                carry = int(carry / self.base)
                it1 -= 1
                i += 1

            length = i
            pbegin += 1

        # Skip leading zeroes in base58 result.
        it2 = size - length
        while it2 != size and b58[it2] == 0:
            it2 += 1

        # Translate the result into a string
        res = self.leader * zeroes
        for i in range(it2, size):
            res += self.alphabet[b58[i]]
        return res

    def decode(self, source):
        if not isinstance(source, str):
            raise BaseXExpectedStringException()
        if len(source) == 0:
            return b''

        psz = 0
        zeroes = 0
        length = 0
        while psz < len(source) and source[psz] == self.leader:
            zeroes += 1
            psz += 1

        # Allocate enough space in big-endian base256 representation.
        size = int(((len(source) - psz) * self.factor) + 1)
        b256 = bytearray([0] * size)
        # Process the characters
        while psz < len(source):
            # Decode character
            carry = self.base_map[ord(source[psz])]
            # Invalid character
            if carry == 255:
                raise BaseXNotInAlphabetException()
            i = 0
            it3 = size - 1
            while (carry != 0 or i < length) and (it3 != -1):
                carry += int(self.base * b256[it3])
                b256[it3] = int(carry % 256)
                carry = int(carry / 256)
                it3 -= 1
                i += 1

            length = i
            psz += 1

        # Skip leading zeroes in b256
        it4 = size - length
        while it4 != size and b256[it4] == 0:
            it4 += 1

        vch = bytearray([0] * (zeroes + (size - it4)))
        j = zeroes
        while it4 != size:
            vch[j] = b256[it4]
            j += 1
            it4 += 1
        return vch

alphabet = lazy_import('.alphabet', __name__)

__all__ = ['basex', 'BaseXException', 'BaseXAlphabetTooLongException', 'BaseXAlphabetAmbiguousException', 'BaseXNotInAlphabetException', 'BaseXExpectedStringException', 'alphabet']
