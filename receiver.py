import socket
import time
import json
from lkcp import KcpObj
from pynput import mouse

def kcp_callback(uid, data):
    s.sendto(data, uid_addr[uid])

def recv_udp(sock):
    try:
        data, udp_addr = sock.recvfrom(65535)
        uid_addr[1] = udp_addr
        return data
    except Exception as e:
        pass
    return None

HOST = "34.87.91.61"
# HOST = "127.0.0.1"
PORT = 8000

def recv_from(sock):
    payload_length = int.from_bytes(sock.recv(2), byteorder='big')
    payload = sock.recv(payload_length)
    data = json.loads(str(payload, encoding="utf8"))
    return data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print(f"Server {HOST}:{PORT} connected")
sender_addr = recv_from(s)
print(f"Got sender_addr {sender_addr}")
s.close()

sender_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_conn.connect((sender_addr[0], 8001))
print(f"Sender {sender_addr} connected")

mouse_controller = mouse.Controller()

while True:
    # print(sender_payload_length)
    # print(f"Request is: {request}")
    # print(f"Connected by: {addr}")
    data = recv_from(sender_conn)
    try:
        mouse_controller.position = data
    except:
        pass
    # print(data)

    #conn.sendall(bytes(reply, encoding="utf8"))

    if data == -1:
        break

s.close()