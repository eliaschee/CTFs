from Crypto.Cipher import AES
import binascii

# AES key
key = b'Prestidigitation'

# Ciphertext from the PCAP
block = binascii.unhexlify(
    'e1dbfd6826a14f279fafe76982333070'
    'a0595e10eec5ffd64cf3569eac102451'
)

# AES decryption (ECB mode)
aes = AES.new(key, AES.MODE_ECB)
decrypted = aes.decrypt(block)

string = ""
size = len(decrypted) - 1

# Undo the XOR layer
for i in range(0, size):
    string = (chr(decrypted[size - i] ^ decrypted[size - 1 - i])) + string

print(string)
