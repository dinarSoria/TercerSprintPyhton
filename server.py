import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []

private_chats = {}  # Diccionario para almacenar los chats privados

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message.startswith('/priv'):
                parts = message.split(' ')
                if len(parts) > 2:
                    recipient = parts[1]
                    if recipient in usernames:
                        content = ' '.join(parts[2:])
                        sender_username = usernames[clients.index(client)]
                        private_message = f"(Private) {sender_username}: {content}"
                        recipient_client = clients[usernames.index(recipient)]
                        recipient_client.send(private_message.encode('utf-8'))
                        client.send(private_message.encode('utf-8'))  # También se envía al remitente
                    else:
                        client.send("User not found".encode('utf-8'))
                else:
                    client.send("Invalid command. Usage: /priv <username> <message>".encode('utf-8'))
            elif message == '/exit':
                if client in private_chats:
                    del private_chats[client]
                    client.send("You exited the private chat".encode('utf-8'))
                else:
                    client.send("You are not in a private chat".encode('utf-8'))
            else:
                broadcast(message.encode('utf-8'), client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            if client in private_chats:
                del private_chats[client]
            client.close()
            break

def accept_connections():
    while True:
        client, address = server.accept()
        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')
        clients.append(client)
        usernames.append(username)
        print(f"{username} is connected with {str(address)}")
        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
