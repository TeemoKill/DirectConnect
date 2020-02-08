import socket
import json
# from pynput import mouse

HOST = ""
PORT = 8000

def bale(obj):
    payload = json.dumps(obj)
    length = len(payload)
    header = length.to_bytes(2, byteorder='big')
    packet = header + bytes(payload, encoding="utf8")
    return packet

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

# s.listen(3)
data, addr = s.recvfrom(2048)
if not data:
    print("client has exist")
    break
print(f"Received: {data} from {addr}")


receiver_conn, receiver_addr = s.accept()
print("Receiver " + str(receiver_addr) + " connected")
sender_conn, sender_addr = s.accept()
print("Sender " + str(sender_addr) + " connected")

sender_conn.sendall(bale(receiver_addr))
print(f"Receiver address {receiver_addr} sent to sender")
receiver_conn.sendall(bale(sender_addr))
print(f"Sender address {sender_addr} sent to receiver")

while True:
    sender_payload = sender_conn.recv(1024)

    # print(f"Request is: {request}")
    # print(f"Connected by: {addr}")
    
    # data = json.loads(str(sender_payload, encoding="utf8"))
    # print(data)

    receiver_conn.sendall(sender_payload)


    #conn.sendall(bytes(reply, encoding="utf8"))

    if sender_payload == b"-1":
        break

sender_conn.close()
receiver_conn.close()
