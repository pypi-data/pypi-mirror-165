import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto import Random

async def genkey():
    generated_key = Random.new().read(AES.block_size)
    key = hashlib.sha256(generated_key).digest()
    with open("aeseasyencryption.key", "wb") as key_file:
        key_file.write(key)
    return key

async def callkey():
  try:
    key = open("aeseasyencryption.key", "rb").read()
    if str(key) == "b''":
      await genkey()
      key = open("aeseasyencryption.key", "rb").read()
    return key
  except:
    await genkey()
    key = open("aeseasyencryption.key", "rb").read()
    return key


async def aesencrypt(slogan):
    key = await callkey()
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    slogan = base64.b64encode(pad(slogan).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key=key, mode= AES.MODE_CFB,iv= iv)
    return base64.b64encode(iv + cipher.encrypt(slogan))

async def aesdecrypt(coded_slogan):
    key = await callkey()
    unpad = lambda s: s[:-ord(s[-1:])]

    coded_slogan = base64.b64decode(coded_slogan)
    iv = coded_slogan[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return unpad(base64.b64decode(cipher.decrypt(coded_slogan[AES.block_size:])).decode('utf8'))