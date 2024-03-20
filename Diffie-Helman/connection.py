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
        
def is_primitive_root(g, p):
    """
    Checks if g is a primitive root modulo p.
    """
    residues = set()
    for i in range(1, p):
        residue = pow(g, i, p)
        if residue in residues:
            return False
        residues.add(residue)
    return True

def find_primitive_root(p):
    """
    Finds a primitive root modulo p.
    """
    for g in range(2, p):
        if is_primitive_root(g, p):
            return g
    return None

class Connection:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2 

    #defines modulus and base
    def handshake(self):
        interval1 = 1000000
        interval2 = 10000000
        p = random_prime_in_interval(interval1, interval2)
        g = find_primitive_root(p)

        self.user1.setBaseAndModulus(g, p)
        self.user2.setBaseAndModulus(g, p)

    def tradePublicKeys(self):
        self.user1.setConnPK(self.user2.getPublicKey())
        self.user2.setConnPK(self.user1.getPublicKey())