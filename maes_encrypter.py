import sys
import maes
import ubinascii

def add_until_16(word):
    for i in range(16-len(word)):
        word+='&'
    return word

def clean_string_binary_remains(binary_string):
    tmp=binary_string.replace('\'','')
    tmp=tmp.replace('b','')
    return tmp
        

def array_tostring(array_data):
    _string = ""
    for _array in array_data:
        _string = _string + chr(_array)
    return _string

def encrypt_data(key, iv, data):
    retornar=""
    cryptor = maes.new(key, maes.MODE_CBC, IV=iv)
    while len(data)>=16:
        #print('data: '+str(data))
        ciphertext = cryptor.encrypt(data[0:16])
        #print(ubinascii.hexlify(ciphertext))
        cifrado_limpio=clean_string_binary_remains(str(ubinascii.hexlify(ciphertext)))
        retornar+=cifrado_limpio
        retornar+="+"
        data=data[16:len(data)]
    if len(data)<16:
        #print(data)
        #print("data len:"+str(len(data)))
        ciphertext = cryptor.encrypt(add_until_16(data))
        cifrado_limpio=clean_string_binary_remains(str(ubinascii.hexlify(ciphertext)))
        retornar+=cifrado_limpio
        #print(ubinascii.hexlify(ciphertext))
    return retornar

#print(encrypt_data(b'AAAAAAAAAAAAAAAA', b'BBBBBBBBBBBBBBBB', b'hola mi nombre es jaime tengo 23 y programo mucho'))