import binascii
import os
from pwn import *

def generate_all_bite():
    for i in range(256):
        if i < 16:
            yield "0" + hex(i)[2:]
        else:
            yield hex(i)[2:]

def token_to_plain_text(cipher, middles): # ex cipher[-64:-32] ~ middle1
    plaintext = ""
    for i in range(len(middles)):
        text = hex(int(middles[i], 16) ^ int("0x" + str(cipher[i*2:2*(i+1)]), 16))[2:]
        if len(text) == 1:
            text = "0" + text
        plaintext += binascii.unhexlify(text).decode()
    return plaintext