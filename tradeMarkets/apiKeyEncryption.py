
from cryptography.fernet import Fernet

#generate key:
keySet1 = Fernet.generate_key()
cipher_suite=Fernet(keySet1)

#apikey
apikeycode=b'LHN5MGEB7MHY7YJA'
#encodedKey='gAAAAABkkt2dYIvy39W81h57J7__y7cFmuzoT-QNNfGxjmjxF5ERmvGFjPdOsGUbHc0WIXX0_nw02S3I660kFW1cJTnNTy3sBh1Uip6Oj5Ftq-JgOAFepIU='

#encoding
encoded_text= cipher_suite.encrypt(apikeycode)
decoded_text=cipher_suite.decrypt(encoded_text)
seed=str(decoded_text, encoding='utf-8')


