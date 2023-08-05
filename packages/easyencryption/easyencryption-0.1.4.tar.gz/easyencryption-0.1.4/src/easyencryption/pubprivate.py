from Crypto.PublicKey import RSA as rsa
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os

async def genkeys():
    key = rsa.generate(2048)
    publickey = key.publickey().export_key()
    privatekey = key.export_key()
    with open("pubeasyencryption.key", "wb") as pub_key_file:
        pub_key_file.write(publickey)
    with open("priveasyencryption.key", "wb") as priv_key_file:
        priv_key_file.write(privatekey)
    keys = [publickey, privatekey]
    return keys

async def regenkeys():
    if os.path.exists("pubeasyencryption.key"):
        os.remove("pubeasyencryption.key")
    if os.path.exists("priveasyencryption.key"):
        os.remove("priveasyencryption.key")
    await genkeys()

async def callpubkey():
  try:
    key = open("pubeasyencryption.key", "rb").read()
    if str(key) == "b''":
      await genkeys()
      key = open("pubeasyencryption.key", "rb").read()
    key = rsa.import_key(key)
    return key
  except:
    await genkeys()
    key = open("pubeasyencryption.key", "rb").read()
    key = rsa.import_key(key)
    return key

async def callprivkey():
  try:
    key = open("priveasyencryption.key", "rb").read()
    if str(key) == "b''":
      await genkeys()
      key = open("priveasyencryption.key", "rb").read()
    key = rsa.import_key(key)
    return key
  except:
    await genkeys()
    key = open("priveasyencryption.key", "rb").read()
    key = rsa.import_key(key)
    return key

async def pubprivencrypt(slogan):
    key = await callpubkey()
    encryptor = PKCS1_OAEP.new(key)
    coded_slogan = encryptor.encrypt(slogan.encode("utf-8"))
    return coded_slogan

async def pubprivdecrypt(coded_slogan):
    key = await callprivkey()
    decryptor = PKCS1_OAEP.new(key)
    decoded_slogan = decryptor.decrypt(coded_slogan)
    decoded_slogan = str(decoded_slogan)
    decoded_slogan = decoded_slogan[2:]
    decoded_slogan = decoded_slogan[:-1]
    return decoded_slogan

