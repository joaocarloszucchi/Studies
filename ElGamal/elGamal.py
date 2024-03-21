from user import User
from connection import Connection

def main():
    alice = User("Alice")
    bob = User("Bob")
    conn = Connection(alice, bob)

    #send message from Alice to Bob
    bob.keyGeneration()

    conn.sendPublicKey()

    alice.setMessage("This is a secret message!")

    alice.encryptMessage()

    conn.sendEncryptedMessage()

    bob.decryptMessage()

    alice.printInfo()
    bob.printInfo()

main()
