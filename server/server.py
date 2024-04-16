import socket
from threading import Thread

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"

# initialize dictionary to store client sockets and their corresponding usernames
clients = {}

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            remove_client(client_socket)
            break
        else:
            username, message = msg.split(separator_token)
            message_with_username = f"{username}: {message}"
            print(message_with_username)
            broadcast(message_with_username)

def broadcast(message):
    for client_socket in clients:
        client_socket.send(message.encode())

def remove_client(client_socket):
    if client_socket in clients:
        del clients[client_socket]
    client_socket.close()

while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    
    username = client_socket.recv(1024).decode()
    if username in clients.values():
        print(f"[!] Username '{username}' already exists. Disconnecting client.")
        client_socket.send("Username already exists. Please choose a different one.".encode())
        client_socket.close()
        continue
    
    clients[client_socket] = username
    
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()
