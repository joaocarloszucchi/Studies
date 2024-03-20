import random

#checks if a number is prime
def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as d * 2^r + 1
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    #print(r, d)

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

#gets a random prime number in a given interval
def random_prime_in_interval(start, end):
    count = 0
    while True:
        num = random.randint(start, end)
        count+=1
        if is_prime(num):
            return num

class User:
    def __init__(self, name):
        self.name = name
        self.privateKey = None
        self.publicKey = None
        self.base = None
        self.modulus = None
        self.connPK = None
        self.secretKey = None

    def printInfo(self):
        print("name", self.name, "\n",
              "privateKey", self.privateKey, "\n",
              "publicKey", self.publicKey, "\n",
              "base", self.base, "\n",
              "modulus", self.modulus, "\n",
              "connPK", self.connPK, "\n",
              "secretKey", self.secretKey, "\n",
              )

    def generatePrivateKey(self):
        start = 1000
        end = 10000
        self.privateKey = random_prime_in_interval(start, end)

    def generatePublicKey(self):
        self.publicKey = pow(self.base, self.privateKey, self.modulus)

    def getName(self):
        return self.name

    def getPublicKey(self):
        return self.publicKey
    
    def setBaseAndModulus(self, base, modulus):
        self.base = base
        self.modulus = modulus

    def setConnPK(self, connPK):
        self.connPK = connPK

    def computeSecretKey(self):
        self.secretKey = pow(self.connPK, self.privateKey, self.modulus)