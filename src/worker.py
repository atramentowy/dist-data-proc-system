import socket

HOST = "127.0.0.1"
PORT = 5000

s = socket.socket()
s.connect((HOST, PORT))

data = s.recv(1024)
print("odebrano:", data.decode())

s.send(b"hello coordinator")

s.close()
