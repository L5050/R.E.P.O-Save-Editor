from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
from Crypto.Hash import HMAC, SHA1
import gzip

def decrypt_es3(file_path, password):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    # Extract the IV (first 16 bytes)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]

    # Derive the key using PBKDF2
    key = PBKDF2(password, iv, dkLen=16, count=100, prf=lambda p, s: HMAC.new(p, s, SHA1).digest())

    # Decrypt the data using AES-128-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Check if the data is GZip compressed
    if decrypted_data[:2] == b'\x1f\x8b':  # GZip magic number
        decrypted_data = gzip.decompress(decrypted_data)
    print(decrypted_data.decode('utf-8'))
    return decrypted_data.decode('utf-8')

# file_path = input("Enter the path to the encrypted file: ")
# password = "Why would you want to cheat?... :o It's no fun. :') :'D"
# try:
#     decrypted_data = decrypt_es3(file_path, password)
#     print(decrypted_data.decode('utf-8'))
# except Exception as e:
#     print(f"Decryption failed: {e}")