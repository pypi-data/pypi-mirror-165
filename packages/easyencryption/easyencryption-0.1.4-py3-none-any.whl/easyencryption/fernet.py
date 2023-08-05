from cryptography.fernet import Fernet
import os

async def genkey():
  key = Fernet.generate_key()
  with open("symeasyencryption.key", "wb") as key_file:
    key_file.write(key)
  return key

async def regenkey():
  if os.path.exists("symeasyencryption.key"):
    os.remove("symeasyencryption.key")
  await genkey()
  
async def callkey():
  try:
    key = open("symeasyencryption.key", "rb").read()
    if str(key) == "b''":
      await genkey()
      key = open("symeasyencryption.key", "rb").read()
    return key
  except:
    await genkey()
    key = open("symeasyencryption.key", "rb").read()
    return key

async def fernetencrypt(slogan):
  key = await callkey()
  slogan = slogan.encode()
  a = Fernet(key)
  coded_slogan = a.encrypt(slogan)
  return coded_slogan

async def fernetdecrypt(coded_slogan):
  key = await callkey()
  b = Fernet(key)
  decoded_slogan = b.decrypt(coded_slogan)
  decoded_slogan = str(decoded_slogan)
  decoded_slogan = decoded_slogan[2:]
  decoded_slogan = decoded_slogan[:-1]
  return(decoded_slogan)

  