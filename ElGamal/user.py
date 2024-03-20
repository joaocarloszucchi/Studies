import random

def is_prime(n, k=5):
    """Miller-Rabin primality test"""
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

    # Write n as 2^r * d + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

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

def generate_prime(bits):
    """Generate a random prime number with specified bits"""
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

def fast_modular_exponentiation(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def is_primitive_root(m, n):
    phi_n = n - 1
    prime_factors = [p for p in range(2, phi_n) if phi_n % p == 0]
    
    for p_i in prime_factors:
        power = phi_n // p_i
        result= fast_modular_exponentiation(m, power, n)
        if result == 1:
            return False
    return True

def find_primitive_root(n):
    for m in range(2, n):
        if is_primitive_root(m, n):
            return m
    return -1

class User:
    def __init__(self, name):
        self.name = name
        self.privateKey = None
        self.publicKey = None
        self.p = None
        self.g = None
        self.connPK = None
        self.message = None
        self.encryptedBlocks = None

    def printInfo(self):
        print("name", self.name, "\n",
              "privateKey", self.privateKey, "\n",
              "publicKey", self.publicKey, "\n",
              "p", self.p, "\n",
              "g", self.g, "\n",
              "connPK", self.connPK, "\n",
              "message", self.message, "\n",
              "encryptedBlocks", self.encryptedBlocks, "\n",
              )
        
    def keyGeneration(self):
        self.p = generate_prime(16)
        self.g = find_primitive_root(self.p)
        self.privateKey = generate_prime(16)
        self.publicKey = pow(self.g, self.privateKey, self.p)

    def setP(self, p):
        self.p = p

    def getP(self):
        return self.p

    def setG(self, g):
        self.g = g

    def getG(self):
        return self.g
    
    def setMessage(self, message):
        self.message = message

    def setConnPK(self, connPk):
        """set the public key of the destiny"""
        self.connPK = connPk

    def getPublicKey(self):
        return self.publicKey
    
    def setEncryptedBlocks(self, encryptedBlocks):
        self.encryptedBlocks = encryptedBlocks

    def getEncryptedBlocks(self):
        return self.encryptedBlocks
    
    def encodeMessage(self):
        """Encode a message using ASCII encoding"""
        encoded_message = ""
        for char in self.message:
            encoded_char = str(ord(char))  # Get the ASCII value of the character
            encoded_message += encoded_char
        return int(encoded_message)
    
    def splitMessage(self, encodedMessage):
        """Split a big integer into smaller parts smaller than p"""
        p = self.p
        big_integer_str = str(encodedMessage)
        blocks = []

        start = 0
        end = len(str(p)) - 1  # Maximum length of each block
        while start < len(big_integer_str):
            block = int(big_integer_str[start:end])
            blocks.append(block)
            start = end
            end += len(str(p)) - 1  # Increase the end index for the next block

        return blocks
    
    def encryptMessage(self):
        m = self.encodeMessage()
        blocks = self.splitMessage(m)
        encryptedBlocks = []

        for block in blocks:
            k = random.randint(2, self.p - 2)
            c1 = pow(self.g, k, self.p)
            c2 = block * pow(self.connPK, k, self.p)
            encryptedBlocks.append((c1, c2))

        self.encryptedBlocks = encryptedBlocks