import socket

HOST = "127.0.0.1"
PORT = 5000


def start_server():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)

    print("serwer działa...")

    conn, addr = s.accept()
    print("połączono:", addr)

    conn.send(b"hello worker")
    data = conn.recv(1024)
    print("odpowiedź:", data.decode())

    conn.close()
    s.close()


if __name__ == "__main__":
    start_server()
