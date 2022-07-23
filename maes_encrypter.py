import sys
import maes
import ubinascii

def array_tostring(array_data):
    _string = ""
    for _array in array_data:
        _string = _string + chr(_array)
    return _string

def encrypt_data(key, iv, data):
    retornar=""
    cryptor = maes.new(key, maes.MODE_CBC, IV=iv)
    while len(data)>=16:
        print('data: '+str(data))
        ciphertext = cryptor.encrypt(data[0:16])
        print(ubinascii.hexlify(ciphertext))
        retornar+="+"
        retornar+=str(ubinascii.hexlify(ciphertext))
        data=data[16:len(data)]
    if len(data)<16:
        ciphertext = cryptor.encrypt(data[0:16])
        retornar+="+"
        retornar+=str(ubinascii.hexlify(ciphertext))
    return retornar

encrypt_data(b'AAAAAAAAAAAAAAAA', b'BBBBBBBBBBBBBBBB', b'hola mi nombre es jaime tengo 23 y programo mucho')