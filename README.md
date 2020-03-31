# CTF-Padding-Oracle-Attack
Padding Oracle Attack tool used for CTF (specific for AES-128 CBC mode) 

## How to use
Please download all the files and put in the same repository. </br>
You should change some setting, which is highlighted, in main.py if needed to achieve the requirement in your CTF task. </br>
Then, simply run with: </br>
<code>
$python3 main.py -I ip_to_connect -P port -C the_ciphertext
</code>

## Padding Oracle Attack
Utilizing the output of server to conduct padding oracle attack. </br>
Usually, server will first check if padding is correct or not then decode the ciphertext. With this feature, one can change ciphertext n-1 block to affect the the next block n after its decryption. Starting from the last 2 bytes in n-1 block, one could try to enumerate all possible 256 choice and change. Only the change which fulfill the padding would be warned with other decode error. So you can get the least character in plaintext: correct_changing xor padding xor ciphertext. </br>
You can search for more detail to understand this implement. </br>
