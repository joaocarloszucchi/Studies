Key exchange algorhytm

at the beggining, 2 prime numbers are agreed between the 2 parts of the communication

(modulus) p = 23
(base) g = 5

then, each members generate a random prime number, which is private

ALICE
a = 4 (Private Key)

BOB
b = 3 (Private Key)

Alice sends Bob (A) (Alice's Public Key)
A = g^a mod p
A = 5^4 mod 23
A = 4

Bob sends Alice (B) (Bob's Public Key)
B = g^b mod p
B = 5^3 mod 23
B = 10

Alice computes (S) (Secret Key)
S = B^a mod p
S = 10^4 mod 23
S = 18

Bob computes (S) (Secret Key)
S = A^b mod p
S = 4^3 mod 23
S = 18

The transmitted values are only the public keys. It is not possible to find(computationally reasonable) the private keys with the public keys.

Discrete Logarithm problem:

Given the following formula G^X = N

-exponentiation: given G and X, its easy to find N
-logarithm: given G and N, its difficult to find X

Given the following formula G^X mod P = N

-discrete exponentiation: given G, X and P its easy to find N
-discrete logarithm: given G, P and N, it is infeasible to find X

bascially, the only solution is a brute force algorithm
