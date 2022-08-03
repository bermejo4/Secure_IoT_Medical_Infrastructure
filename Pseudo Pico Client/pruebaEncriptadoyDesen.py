import binascii
from Crypto.Cipher import AES



obj = AES.new('1234567890123456'.encode("utf8"), AES.MODE_CBC, 'AAAAAAAAAAAAAAAA'.encode("utf8"))
message = "TextMustBe16Byte"
ciphertext = obj.encrypt(message.encode("utf8"))
print(binascii.b2a_base64(ciphertext))
print(binascii.hexlify(ciphertext))
print(ciphertext)

cifrado="82d64ecbbd14bac936059648e6a19041".encode("utf8")
cifra=binascii.unhexlify(cifrado)
print("cifra"+str(cifra))
obj2 = AES.new('1234567890123456'.encode("utf8"), AES.MODE_CBC, 'AAAAAAAAAAAAAAAA'.encode("utf8"))
print(obj2.decrypt(cifra).decode())