from user import User
from connection import Connection

def main():
    alice = User("Alice")
    bob = User("Bob")

    conn = Connection(alice, bob)

    conn.handshake()

    alice.generatePrivateKey()
    bob.generatePrivateKey()

    alice.generatePublicKey()
    bob.generatePublicKey()

    conn.tradePublicKeys()

    alice.computeSecretKey()
    bob.computeSecretKey()

    alice.printInfo()
    bob.printInfo()

main()
