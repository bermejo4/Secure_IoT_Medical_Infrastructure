from Crypto.Cipher import AES
import binascii
obj = AES.new('AAAAAAAAAAAAAAAA'.encode("utf8"), AES.MODE_CBC, 'BBBBBBBBBBBBBBBB'.encode("utf8"))
message = "TextMustBe16Byte"
ciphertext = obj.encrypt(message.encode("utf8"))
print(binascii.b2a_base64(ciphertext))
print(binascii.hexlify(ciphertext))
print(ciphertext)

cifrado="0f1d1d12a6fc85ae06ad25c817d25595".encode("utf8")
cifra=binascii.unhexlify(cifrado)
obj2 = AES.new('AAAAAAAAAAAAAAAA'.encode("utf8"), AES.MODE_CBC, 'BBBBBBBBBBBBBBBB'.encode("utf8"))
print(obj2.decrypt(cifra))