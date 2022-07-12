import pyaes
import ubinascii

# A 256 bit (32 byte) key
key_128 = "AAAAAAAAAAAAAAAA"

# For some modes of operation we need a random initialization vector
# of 16 bytes
iv = "BBBBBBBBBBBBBBBB"

aes = pyaes.AESModeOfOperationCBC(key_128, iv = iv)
plaintext = "TextMustBe16Byte"
ciphertext = aes.encrypt(plaintext)

# '\xd6:\x18\xe6\xb1\xb3\xc3\xdc\x87\xdf\xa7|\x08{k\xb6'
print(ciphertext)


# The cipher-block chaining mode of operation maintains state, so
# decryption requires a new instance be created
aes = pyaes.AESModeOfOperationCBC(key_128, iv = iv)
decrypted = aes.decrypt(ciphertext)

# True
print(decrypted == plaintext)
print(ubinascii.hexlify(ciphertext))
print(ubinascii.b2a_base64(ciphertext))
print("--------------------------------")
