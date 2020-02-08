import socket
# import msvcrt
import json
from pynput import mouse

HOST = "34.87.91.61"
# HOST = "127.0.0.1"
PORT = 8000

def bale(obj):
    payload = json.dumps(obj)
    length = len(payload)
    header = length.to_bytes(2, byteorder='big')
    packet = header + bytes(payload, encoding="utf8")
    return packet

def recv_from(sock):
    payload_length = int.from_bytes(sock.recv(2), byteorder='big')
    payload = sock.recv(payload_length)
    data = json.loads(str(payload, encoding="utf8"))
    return data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

receiver_addr = recv_from(s)
print(f"Got receiver_addr {receiver_addr} ")
s.close()

sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.bind(("", 8001))
sender.listen(1)
receiver_conn, receiver_addr_ = sender.accept()
print(f"Receiver {receiver_addr} connected")

def on_move(x, y):
    # print(f"{x}, {y}")
    # print(length)
    # print(len(bytes([length])))
    packet = bale((x, y))
    receiver_conn.sendall(packet)

with mouse.Listener(on_move=on_move) as mouse_listener:
    mouse_listener.join()

# while True:
#     key = msvcrt.getch()
#     if ord(key) == 27: # Esc
#         break
#     else:
#         #print(ord(key))
#         pass

#     s.sendall(key)

#     reply = s.recv(1024)
#     #print(f"Reply: {reply}")

receiver_conn.sendall(bale(-1))
receiver_conn.close()