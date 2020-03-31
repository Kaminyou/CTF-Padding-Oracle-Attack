import binascii
import os
from pwn import *
from utils import *
from argparse import ArgumentParser
def one_block_padding_oracle_attack(cipher):
    middles = []
    cipher_pre = cipher[:-64]
    cipher_post = cipher[-32:]
    cipher_target = cipher[-64:-32]
    
    # try every word (totally 16)
    for i in range(16):
        target_hex = hex(i+1)
        post = ""
        for middle in middles:
            to_add = hex(int(middle, 16) ^ int(target_hex, 16))[2:] #middle: "0x??" #target_hex: "0x??"
            if len(to_add) == 1:
                to_add = "0" + to_add
            post += to_add
        pre = "00" * (15-i)
        for trying in generate_all_bite():
            try_token = pre + trying + post
            try_token = cipher_pre + try_token + cipher_post
            ####################### Please revise this part as your need #######################
            r.recv()
            r.sendline("2")
            r.recv()
            ####################################################################################
            r.sendline(try_token)
            if r.recvline(keepends=False).decode() == 'Unicode Decode Error':
                middles.insert(0,hex(int("0x"+trying,16) ^ int(target_hex, 16)))
                break
    return middles

parser = ArgumentParser()
parser.add_argument("-I", "--ip", help="the ip to connect", dest="input_ip")
parser.add_argument("-P", "--port", help="the port to connect", dest="input_port")
parser.add_argument("-C", "--cipher", help="the cipher text", dest="input_cipher")

args = parser.parse_args()
ip = args.input_ip
port = int(args.input_port)
token = args.input_cipher

# Padding Oracle Attack
if __name__ == "__main__":
    
    r=remote(ip, port)
    ####################### Please revise this part as your need #######################
    r.recv()
    r.sendline("1")
    ####################################################################################

    if (len(token) % 32) != 0:
        print("Please check your ciphertext! It doesn't meet requirement of 128 bits block")
    else: 
        attack_times = len(token) // 32 - 2
        plaintext = ""
        middletext = []
        for i in range(attack_times):
            middle_sub = one_block_padding_oracle_attack(token[:(-32*i)])
            middletext.insert(0, middle_sub)

        for i in range(attack_times):
            plaintext += token_to_plain_text(token[(-32 * (attack_times + 1 - i)):(-32 * (attack_times- i))], middletext[i])
        print("=============== Plaintext ===============")
        print(plaintext)