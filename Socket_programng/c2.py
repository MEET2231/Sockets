import socket
import threading

# Server configuration
HOST = '192.168.6.119'  # localhost
PORT = 55555
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Dictionary to hold client connections and their nicknames
clients = {}


def broadcast(message):
    for client_sock in clients:
        client_sock.send(message)


def handle_client(client, nickname):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = list(clients.keys())[list(clients.values()).index(nickname)]
            del clients[index]
            client.close()
            broadcast(f'{nickname} left the chat.'.encode(FORMAT))
            break


def start_server():
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        print(f"New connection from {addr}")
        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        clients[client] = nickname
        broadcast(f"{nickname} joined the chat!".encode(FORMAT))
        thread = threading.Thread(target=handle_client, args=(client, nickname))
        thread.start()


if __name__ == "__main__":
    start_server()
