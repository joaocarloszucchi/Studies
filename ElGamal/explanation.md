ElGamal consists on 3 steps:

-Key Generation

-Encryption

-Decryption

---

Key Generation

This step is similitar to diffieHelman. It generates a prime number(p), a generator(g)(that is p's primitive root) and a random prime number(private key)



Encryption

This step envolves the following steps:

-Encoding message: turns the text message into a encoded one. It can be done using ASCII or Unicode and concatenating it into a big integer

-Splitting message into blocks: Split the message into blocks where each block(its actually a integer) is smaller than p(the modulus)

-Calculating ciphertext(c1, c2) for each block of the message

    -Computes k(a random integer in the range(2, p-2))

    -Computes c1(g^k mod p)

    -Computes c2(block * connPK^k mod p) 

-Sends the list of ciphertext to the receiver



Decryption

Bob starts decrypting each block sent by Alice

decryption contains:

-Compute s = c1^private_key mod p

-Compute m = c2 * (s^-1 mod p) mod p

Then you just need to decode the message(turns ASCII into characters)



ADDITIONAL INFO:

Notice that some features were not explained. Well, this extra ones are just basic implementations so the total process would work. This features were necessary because some problems were found.

Since the ASCII range is 0-127, some characters can be represented by 1, 2, or 3 digits. In this case, the decoder was not able to properly split the digits in the corrected characters. To fix this, adding additional zeros is a solution.

if carac < 10 then add '00'
if carac < 100 then add '0'

But this still does not fully solves the problem. Since the ASCII text will be casted to a big integer, any left zeros will be disconsidered, so, if the first character of the message is any ASCII character above 100, all the text will be messed. Plus, since the integer is divided into blocks, in case of any block integer starts with a '0', it will also be lost.

To keep track of this missed '0', the solution is to add an additional variable to all ciphertexts, indicating how many '0' must be placed in that block. computeAdditional() takes care of this task.