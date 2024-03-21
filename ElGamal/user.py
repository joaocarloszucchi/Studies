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
        self.decryptedBlocks = None

    def printInfo(self):
        print("name", self.name, "\n",
              "privateKey", self.privateKey, "\n",
              "publicKey", self.publicKey, "\n",
              "p", self.p, "\n",
              "g", self.g, "\n",
              "connPK", self.connPK, "\n",
              "message", self.message, "\n",
              "encryptedBlocks", self.encryptedBlocks, "\n",
              "decryptedBlocks", self.decryptedBlocks, "\n",
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
    
    def getAdditional(self, char):
        encoded_char = str(ord(char))
        if int(encoded_char) < 10:
            return '00'
        elif int(encoded_char) < 100:
            return '0'
        return ''

    def encodeMessage(self):
        """Encode a message using ASCII encoding"""
        additional = self.getAdditional(self.message[0])

        encoded_message = ""
        for char in self.message:
            encoded_char = str(ord(char))  # Get the ASCII value of the character
            if int(encoded_char) < 10:
                encoded_message += '00'
            elif int(encoded_char) < 100:
                encoded_message += '0'
            encoded_message += encoded_char
        return int(encoded_message), additional
    
    def decodeMessage(self, encoded_integer):
        """Decode an integer into the corresponding text (ASCII representation)."""
        encoded_str = str(encoded_integer)
        decoded_message = ""

        i = 0
        while i < len(encoded_str):
            # Take each two-digit substring and convert it to its corresponding character
            char_code = int(encoded_str[i:i+3])
            decoded_message += chr(char_code)
            # Move to the next two digits
            i += 3

        self.message = decoded_message

    def splitMessage(self, encodedMessage, firstAdd):
        """Split a big integer into smaller parts smaller than p"""
        p = self.p
        big_integer_str = str(encodedMessage)
        blocks = []

        start = 0
        end = len(str(p)) - 1  # Maximum length of each block
        total = len(big_integer_str)
        while start < total:
            block = int(big_integer_str[start:end])
            start = end
            end += len(str(p)) - 1  # Increase the end index for the next block
            add = self.computeAdditional(len(str(block)), end - start, start, total)
            blocks.append((block, add))

        blocks[0] = (blocks[0][0], firstAdd)

        return blocks
    
    def computeAdditional(self, length, step, start, total):
        if length < step:
            if start >= total :
                if total - start != length:
                    return '0'* ((total - start) - length)
                return ''
            return '0'*(step - length)
        return ''

    def encryptMessage(self):
        m, firstAdd = self.encodeMessage()
        blocks = self.splitMessage(m, firstAdd)
        encryptedBlocks = []

        for blockTuple in blocks:
            block, add = blockTuple
            k = random.randint(2, self.p - 2)
            c1 = pow(self.g, k, self.p)
            c2 = block * pow(self.connPK, k, self.p)
            encryptedBlocks.append((c1, c2, add))

        self.encryptedBlocks = encryptedBlocks

    def decryptMessage(self):
        """Decrypts a list of ciphertext blocks using the private key."""
        decryptedMessage = ""

        for c1, c2, add in self.encryptedBlocks:
            # Compute s = c1^private_key mod p
            s = pow(c1, self.privateKey, self.p)
            # Compute m = c2 * (s^-1 mod p) mod p
            inverse_s = pow(s, -1, self.p)
            m = (c2 * inverse_s) % self.p
            decryptedMessage += add
            decryptedMessage += str(m)

        self.decodeMessage(decryptedMessage)
        self.encryptedBlocks = None