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