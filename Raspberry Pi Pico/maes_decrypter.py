import sys
import maes
import ubinascii

def array_tostring(array_data):
    _string = ""
    for _array in array_data:
        _string = _string + chr(_array)
    return _string

def decrypt_cipher_data(cif):
    cif=ubinascii.unhexlify(cif)
    # A 128 bit (16 byte) key
    key = b"AAAAAAAAAAAAAAAA"
    #initialization vector of 16 bytes
    iv = b"BBBBBBBBBBBBBBBB"
    decryptor = maes.new(key, maes.MODE_CBC, IV=iv)
    clean_result=array_tostring(decryptor.decrypt(cif))
    clean_result=clean_result.replace('#','')
    return clean_result