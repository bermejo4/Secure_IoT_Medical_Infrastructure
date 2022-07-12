# encoding: utf-8
import sys
import maes
import ubinascii

def array_tostring(array_data):
    _string = ""
    for _array in array_data:
        _string = _string + chr(_array)
    return _string

key = b"AAAAAAAAAAAAAAAA"
iv = b"BBBBBBBBBBBBBBBB"

cryptor = maes.new(key, maes.MODE_CBC, IV=iv)
ciphertext = cryptor.encrypt(b'TextMustBe16Byte')
print(ubinascii.b2a_base64(array_tostring(ciphertext)))
print(ubinascii.hexlify(ciphertext))
print(ubinascii.b2a_base64(ciphertext))
print(ciphertext)

decryptor = maes.new(key, maes.MODE_CBC, IV=iv)
print(array_tostring(decryptor.decrypt(ciphertext)))