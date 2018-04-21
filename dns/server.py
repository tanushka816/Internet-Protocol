import hexdump
import time
import socket
from cache import in_cache
from pasres import parse_asked_package, parse_answer_package
from pack_builder import build_answer, create_rrecord

PORT = 53
SERVER = '8.8.8.8'

CACHE_A = []
CACHE_NS = []
GLOBAL_CACHE = {1:CACHE_A, 2:CACHE_NS}

def start(server=SERVER):
    print("started")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', PORT))
    while True:
        data, sender = sock.recvfrom(512)
        # [print(line) for line in hexdump.dumpgen(data)]
        resolve_data(data, server)



def resolve_data(data, server=SERVER):
    global GLOBAL_CACHE
    id, questions = parse_asked_package(data)
    for d_name, qtype in questions:
        if qtype in GLOBAL_CACHE:
            if d_name in GLOBAL_CACHE[qtype]:
                for addr in GLOBAL_CACHE[qtype][d_name]:
                    create_rrecord(d_name, qtype, addr, GLOBAL_CACHE[qtype][d_name][addr] - time.time())
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(data, (SERVER, PORT))
                data = sock.recv(512)
                [print(line) for line in hexdump.dumpgen(data)]
                # answers = parse_answer_package(data)






if __name__ == "__main__":
    start()