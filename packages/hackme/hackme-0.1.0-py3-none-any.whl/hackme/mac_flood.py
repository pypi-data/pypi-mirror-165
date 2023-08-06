import socket
import struct
import random


def generate_mac():
    bt = []
    for i in range(0, 6):
        bt.append(random.randint(0x00, 0xFF))
    return "\\x" + "\\x".join(map(lambda x: "%02x" % x, bt))


def main():
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    s.bind(("eth0", socket.htons(0x0800)))
    # destMAC = b"\x50\x03\x00\x04\x00\x03"
    destMAC = "\x50\x03\x00\x04\x00\x03"
    protocol = b"\x88\xb5"
    payload = "Hi".encode()
    while True:
        srcMAC = generate_mac().decode("string-escape")
        s.sendall(destMAC + srcMAC + protocol + payload)


if __name__ == "__main__":
    main()
