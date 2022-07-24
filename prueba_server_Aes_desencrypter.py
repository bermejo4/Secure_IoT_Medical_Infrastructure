from Crypto.Cipher import AES
import binascii

def sementate_in_ciphered_strings(cadena):
    first=''
    for letter in cadena:
        if letter == '+':
            cadena=cadena.replace('+','',1)
            print('cadena:'+cadena)
            break
        else:
            first+=letter
    return first, cadena.replace(first,'')

def clean_string_binary_remains(binary_string):
    tmp=binary_string.replace('\'','')
    tmp=tmp.replace('b','',1)
    return tmp

def data_from_pico_desencrypter(text):
    segundo=text
    data_decrypted = ''
    obj2 = AES.new('1234567890123456'.encode("utf8"), AES.MODE_CBC, 'AAAAAAAAAAAAAAAA'.encode("utf8"))
    for i in range(segundo.count('+') + 1):
        primer, segundo = sementate_in_ciphered_strings(segundo)
        print('primer: ' + primer)
        print('segundo: ' + segundo)
        cifrado = primer.encode("utf8")
        cifra = binascii.unhexlify(cifrado)
        data_decrypted += clean_string_binary_remains(str(obj2.decrypt(cifra)))
        print(obj2.decrypt(cifra))
    return data_decrypted


# obj = AES.new('1234567890123456'.encode("utf8"), AES.MODE_CBC, 'AAAAAAAAAAAAAAAA'.encode("utf8"))
# message = "TextMustBe16Byte"
# ciphertext = obj.encrypt(message.encode("utf8"))
# print(binascii.b2a_base64(ciphertext))
# print(binascii.hexlify(ciphertext))
# print(ciphertext)

cifrado="0f1d1d12a6fc85ae06ad25c817d25595".encode("utf8")
cifra=binascii.unhexlify(cifrado)
obj2 = AES.new('1234567890123456'.encode("utf8"), AES.MODE_CBC, 'AAAAAAAAAAAAAAAA'.encode("utf8"))
print(obj2.decrypt(cifra))

segundo = "b102ea0ad185e800792364c204a18248+9951608489b119e828c605255c3e43df+99fe1e0ee93d0d2a1b923007cde56e44+5671ced14769a3b583c9e3763e698013+1be78fae5af0756919c8a6d1f4c16f97+06a6d0527149f72ceb81c341c5a1cf83+90f5d35e775edc9d0adc235dcd9ac226+6ccf368036620eb053122f14dc48a923+053f2bc6e3e78b4fbe0e4f679121fbe9"
data_decrypted=''
obj2 = AES.new('1234567890123456'.encode("utf8"), AES.MODE_CBC, 'AAAAAAAAAAAAAAAA'.encode("utf8"))

for i in range(segundo.count('+')+1):
    primer, segundo = sementate_in_ciphered_strings(segundo)
    print('primer: '+primer)
    print('segundo: '+segundo)
    cifrado=primer.encode("utf8")
    cifra=binascii.unhexlify(cifrado)
    #obj2 = AES.new('1234567890123456'.encode("utf8"), AES.MODE_CBC, 'AAAAAAAAAAAAAAAA'.encode("utf8"))
    data_decrypted += clean_string_binary_remains(str(obj2.decrypt(cifra)))
    print(obj2.decrypt(cifra))

print(data_decrypted)

print('-----------------------------')
text= "b102ea0ad185e800792364c204a18248+899bb316388e8ecadffaba6ec444aff8+0acc0fbee5f4d34a817ebec3274f3809+eeac468bd440860236cccbc20839077f+359acdaadca5fe4525df209f8612576f+685ab32bb4a06671f18b621114e6c93a+9aef30d18f1daa4c161a57d9f402c86b+280e25e1a5f44f1b94534d8f15d25086+9ff3efa26680a606e70ce1b1e1d52630+f1ad6eb975c70272658321ab25f145bd"
print(data_from_pico_desencrypter(text))